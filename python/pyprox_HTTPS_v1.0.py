#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PyProx HTTPS v1.0"""

__version__ = "1.0"


import base64
import logging
import random
import socket
import threading
import time
from pathlib import Path

import dns.message
import dns.rdatatype
import requests
import yaml

BASE_DIR = Path(__file__).resolve().parent
STATIC = BASE_DIR / Path("static")
RELATED_FILES = STATIC / Path(f"v{__version__}")

CONFIGS_PATH = RELATED_FILES / Path("configs")
LOGS_PATH = RELATED_FILES / Path("logs")

DNS_CONFIG_PATH = CONFIGS_PATH / Path("DNS.yaml")
MAIN_CONFIG_PATH = CONFIGS_PATH / Path("config.yaml")

with open(DNS_CONFIG_PATH, "r") as file:
    DNS_CONFIGS = yaml.safe_load(file)

with open(MAIN_CONFIG_PATH, "r") as file:
    MAIN_CONFIGS = yaml.safe_load(file)


# ** Main Configs **
## -- Service --
listen_PORT = MAIN_CONFIGS["service"]["port"]
listen_HOST = MAIN_CONFIGS["service"]["host"]
allow_insecure = MAIN_CONFIGS["service"]["allow_insecure"]
## -- Fragment --
num_fragment = MAIN_CONFIGS["fragment"]["num"]
fragment_sleep = MAIN_CONFIGS["fragment"]["sleep"]
## -- Logging --
log_every_N_sec = MAIN_CONFIGS["logging"]["every_N_sec"]
log_file_name = MAIN_CONFIGS["logging"]["filename"]
LOG_FILE_PATH = LOGS_PATH / Path(log_file_name)
logging_format = MAIN_CONFIGS["logging"]["format"]
logging.basicConfig(level=logging.INFO, format=logging_format)
## -- Socket --
socket_timeout = MAIN_CONFIGS["socket"]["timeout"]
first_time_sleep = MAIN_CONFIGS["socket"]["first_time_sleep"]
accept_time_sleep = MAIN_CONFIGS["socket"]["accept_time_sleep"]

# ** DNS Configs **
## -- DNS URL --
DNS_url = DNS_CONFIGS["DNS_url"]
## -- Offline DNS --
offline_DNS = {}

for item in [
    dns_pack[1] for dns_pack in DNS_CONFIGS["offline_DNS"].items() if dns_pack[1]
]:
    offline_DNS.update(item)

# ** Global Vars **
DNS_cache = {}  # resolved domains
IP_DL_traffic = {}  # download usage for each ip
IP_UL_traffic = {}  # upload usage for each ip


class DNS_over_Fragment:
    def __init__(self):
        self.url = DNS_url
        self.req = requests.session()
        self.fragment_proxy = {"https": f"http://{listen_HOST}:" + str(listen_PORT)}

    def query(self, server_name):
        offline_ip = offline_DNS.get(server_name, None)
        if offline_ip is not None:
            print("offline DNS -->", server_name, offline_ip)
            return offline_ip

        cache_ip = DNS_cache.get(server_name, None)
        if cache_ip is not None:
            print("cached DNS -->", server_name, cache_ip)
            return cache_ip

        quary_params = {
            # 'name': server_name,    # no need for this when using dns wire-format , cause 400 err on some server
            "type": "A",
            "ct": "application/dns-message",
        }

        print("online DNS Query", server_name)
        try:
            query_message = dns.message.make_query(server_name, "A")
            query_wire = query_message.to_wire()
            query_base64 = base64.urlsafe_b64encode(query_wire).decode("utf-8")
            query_base64 = query_base64.replace(
                "=", ""
            )  # remove base64 padding to append in url

            query_url = self.url + query_base64
            ans = self.req.get(
                query_url,
                params=quary_params,
                headers={"accept": "application/dns-message"},
                proxies=self.fragment_proxy,
            )

            # Parse the response as a DNS packet
            if (
                ans.status_code == 200
                and ans.headers.get("content-type") == "application/dns-message"
            ):
                answer_msg = dns.message.from_wire(ans.content)

                resolved_ip = None
                for x in answer_msg.answer:
                    if x.rdtype == dns.rdatatype.A:
                        resolved_ip = x[0].address  # pick first ip in DNS answer
                        DNS_cache[server_name] = resolved_ip
                        print("################# DNS Cache is : ####################")
                        print(
                            DNS_cache
                        )  # print DNS cache , it usefull to track all resolved IPs , to be used later.
                        print("#####################################################")
                        break

                print(f"online DNS --> Resolved {server_name} to {resolved_ip}")
                return resolved_ip
            else:
                print(f"Error: {ans.status_code} {ans.reason}")
        except Exception as e:
            print(repr(e))


class ThreadedServer(object):
    def __init__(self, host, port):
        self.DoH = DNS_over_Fragment()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(
            128
        )  # up to 128 concurrent unaccepted socket queued , the more is refused untill accepting those.

        while True:
            client_sock, _ = self.sock.accept()
            client_sock.settimeout(socket_timeout)

            time.sleep(accept_time_sleep)  # avoid server crash on flooding request
            thread_up = threading.Thread(target=self.my_upstream, args=(client_sock,))
            thread_up.daemon = True  # avoid memory leak by telling os its belong to main program , its not a separate program , so gc collect it when thread finish
            thread_up.start()

    def handle_client_request(self, client_socket):
        # Receive the CONNECT request from the client
        data = client_socket.recv(16384)

        if data[:7] == b"CONNECT":
            server_name, server_port = self.extract_servername_and_port(data)
        elif (data[:3] == b"GET") or (data[:4] == b"POST"):
            q_line = str(data).split("\r\n")
            q_url = q_line[0].split()[1]
            q_url = q_url.replace("http://", "https://")
            print("redirect http to HTTPS", q_url)
            response_data = (
                "HTTP/1.1 302 Found\r\nLocation: "
                + q_url
                + "\r\nProxy-agent: MyProxy/1.0\r\n\r\n"
            )
            client_socket.sendall(response_data.encode())
            client_socket.close()
            return None
        else:
            print("Unknown Method", str(data[:10]))
            response_data = (
                b"HTTP/1.1 400 Bad Request\r\nProxy-agent: MyProxy/1.0\r\n\r\n"
            )
            client_socket.sendall(response_data)
            client_socket.close()
            return None

        print(server_name, "-->", server_port)

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.settimeout(socket_timeout)
            server_socket.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_NODELAY, 1
            )  # force localhost kernel to send TCP packet immediately (idea: @free_the_internet)

            try:
                socket.inet_aton(server_name)
                # print('legal IP')
                server_IP = server_name
            except socket.error:
                # print('Not IP , its domain , try to resolve it')
                server_IP = self.DoH.query(server_name)

            server_socket.connect((server_IP, server_port))
            # Send HTTP 200 OK
            response_data = b"HTTP/1.1 200 Connection established\r\nProxy-agent: MyProxy/1.0\r\n\r\n"
            client_socket.sendall(response_data)
            return server_socket
        except Exception as e:
            print(repr(e))
            # Send HTTP ERR 502
            response_data = (
                b"HTTP/1.1 502 Bad Gateway\r\nProxy-agent: MyProxy/1.0\r\n\r\n"
            )
            client_socket.sendall(response_data)
            client_socket.close()
            server_socket.close()
            return None

    def my_upstream(self, client_sock):
        first_flag = True
        backend_sock = self.handle_client_request(client_sock)

        if backend_sock is None:
            client_sock.close()
            return False

        this_ip = backend_sock.getpeername()[0]
        if this_ip not in IP_UL_traffic:
            IP_UL_traffic[this_ip] = 0

        while True:
            try:
                if first_flag is True:
                    first_flag = False

                    time.sleep(
                        first_time_sleep
                    )  # speed control + waiting for packet to fully recieve
                    data = client_sock.recv(16384)
                    # print('len data -> ',str(len(data)))
                    # print('user talk :')

                    if data:
                        thread_down = threading.Thread(
                            target=self.my_downstream, args=(backend_sock, client_sock)
                        )
                        thread_down.daemon = True
                        thread_down.start()
                        # backend_sock.sendall(data)
                        send_data_in_fragment(data, backend_sock)
                        IP_UL_traffic[this_ip] = IP_UL_traffic[this_ip] + len(data)

                    else:
                        raise Exception("cli syn close")

                else:
                    data = client_sock.recv(16384)
                    if data:
                        backend_sock.sendall(data)
                        IP_UL_traffic[this_ip] = IP_UL_traffic[this_ip] + len(data)
                    else:
                        raise Exception("cli pipe close")

            except Exception as _:
                # print('upstream : '+ repr(e) )
                time.sleep(2)  # wait two second for another thread to flush
                client_sock.close()
                backend_sock.close()
                return False

    def my_downstream(self, backend_sock, client_sock):
        this_ip = backend_sock.getpeername()[0]
        if this_ip not in IP_DL_traffic:
            IP_DL_traffic[this_ip] = 0

        first_flag = True
        while True:
            try:
                if first_flag is True:
                    first_flag = False
                    data = backend_sock.recv(16384)
                    if data:
                        client_sock.sendall(data)
                        IP_DL_traffic[this_ip] = IP_DL_traffic[this_ip] + len(data)
                    else:
                        raise Exception("backend pipe close at first")

                else:
                    data = backend_sock.recv(16384)
                    if data:
                        client_sock.sendall(data)
                        IP_DL_traffic[this_ip] = IP_DL_traffic[this_ip] + len(data)
                    else:
                        raise Exception("backend pipe close")

            except Exception as _:
                # print('downstream '+backend_name +' : '+ repr(e))
                time.sleep(2)  # wait two second for another thread to flush
                backend_sock.close()
                client_sock.close()
                return False

    def extract_servername_and_port(self, data):
        host_and_port = str(data).split()[1]
        host, port = host_and_port.split(":")
        return (host, int(port))


def merge_all_dicts():
    full_DNS = {**DNS_cache, **offline_DNS}  # merge two dict , need python 3.5 or up
    inv_DNS = {
        v: k for k, v in full_DNS.items()
    }  # inverse mapping to look for domain given ip
    stats = {}
    for ip in IP_DL_traffic:
        up = round(IP_UL_traffic[ip] / (1024.0), 3)
        down = round(IP_DL_traffic[ip] / (1024.0), 3)
        host = inv_DNS.get(ip, "?")
        if (up > down) and (down < 1.0):  # download below 1KB
            maybe_filter = "maybe"
        else:
            maybe_filter = "-------"

        su = f"UL={up} KB:"
        sd = f"DL={down} KB:"
        sf = f"filtered={maybe_filter}:"
        sh = f"Host={host}:"
        stats[ip] = ":" + su + sd + sf + sh
    return stats


# only run in separate thread
def log_writer():
    with open(LOG_FILE_PATH, "w") as f:
        while True:
            time.sleep(log_every_N_sec)
            all_stats_info = merge_all_dicts()
            f.seek(0)
            f.write("\n########### new DNS resolved : ##############\n")
            f.write(str(DNS_cache).replace(",", ",\n"))
            f.write("\n#############################################\n")
            f.write("\n########### ALL INFO : ######################\n")
            f.write(
                str(all_stats_info)
                .replace("'", "")
                .replace(",", "\n")
                .replace(":", "\t")
            )
            f.write("\n#############################################\n")
            f.flush()
            f.truncate()
            print("info file writed to", f.name)


def start_log_writer():
    thread_log = threading.Thread(target=log_writer, args=())
    thread_log.daemon = True
    thread_log.start()


def send_data_in_fragment(data, sock):
    L_data = len(data)
    indices = random.sample(range(1, L_data - 1), num_fragment - 1)
    indices.sort()
    # print('indices=',indices)

    i_pre = 0
    for i in indices:
        fragment_data = data[i_pre:i]
        i_pre = i
        # print('send ',len(fragment_data),' bytes')

        # sock.send(fragment_data)
        sock.sendall(fragment_data)

        time.sleep(fragment_sleep)

    fragment_data = data[i_pre:L_data]
    sock.sendall(fragment_data)
    print("----------finish------------")


if __name__ == "__main__":
    start_log_writer()
    print(f"Now listening at: {listen_HOST}:" + str(listen_PORT))
    ThreadedServer(listen_HOST, listen_PORT).listen()