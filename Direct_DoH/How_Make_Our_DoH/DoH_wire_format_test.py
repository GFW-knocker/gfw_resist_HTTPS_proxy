#!/usr/bin/env python3

import dns.message   #  --> pip install dnspython
import dns.rdatatype
import requests      #  --> pip install requests
import base64


# DNS_url = 'https://your.site:8443/mygoogle/dns-query?dns='
# DNS_url = 'https://your.site:8443/mycloudflare/dns-query?dns='

# DNS_url = 'https://8.8.8.8/dns-query?dns='
# DNS_url = 'https://8.8.4.4/dns-query?dns='
DNS_url = 'https://1.1.1.1/dns-query?dns='
# DNS_url = 'https://dns.electrotm.org/dns-query?dns='

query = 'youtube.com'

allow_insecure = True   # set true to allow certificate domain mismatch 


class DNS_over_Fragment:
    def __init__(self):
        self.url = DNS_url
        self.req = requests.session()              
        
    
    def query(self,server_name):

        quary_params = {
            # 'name': server_name,   # no need for this when using dns wire-format , cause 400 err on some server
            'type': 'A',
            'ct': 'application/dns-message',
            }
        

        print(f'online DNS Query',server_name)        
        try:
            query_message = dns.message.make_query(server_name,'A')
            query_wire = query_message.to_wire()
            query_base64 = base64.urlsafe_b64encode(query_wire).decode('utf-8')
            query_base64 = query_base64.replace('=','')    # remove base64 padding to append in url            

            query_url = self.url + query_base64
            ans = self.req.get( query_url , params=quary_params , headers={'accept': 'application/dns-message'} , verify=(not allow_insecure) )

            # Parse the response as a DNS packet
            if ans.status_code == 200 and ans.headers.get('content-type') == 'application/dns-message':
                answer_msg = dns.message.from_wire(ans.content)

                resolved_ip = None
                for x in answer_msg.answer:
                    if (x.rdtype == dns.rdatatype.A):
                        resolved_ip = x[0].address    # pick first ip in DNS answer                    
                        break
                
                print(f'online DNS --> Resolved {server_name} to {resolved_ip}')                
                return resolved_ip
            else:
                print(f'Error: {ans.status_code} {ans.reason}')
        except Exception as e:
            print(repr(e))
        



if (__name__ == "__main__"):
    DoH = DNS_over_Fragment()
    DoH.query(query)



    
