#!/usr/bin/env python3

import requests      #  --> pip install requests
import json



# DNS_url = 'https://your.site:8443/mygoogle/resolve?name='
# DNS_url = 'https://your.site:8443/mycloudflare/dns-query?name='

DNS_url = 'https://8.8.8.8/resolve?name='
# DNS_url = 'https://8.8.4.4/resolve?name='
# DNS_url = 'https://1.1.1.1/dns-query?name='

query = 'youtube.com' 


allow_insecure = True # set true to allow certificate domain mismatch 


class DNS_over_Fragment:
    def __init__(self):
        self.url = DNS_url
        self.req = requests.session()              
        
    
    def query(self,server_name):

        quary_params = {
            'name': server_name,
            'type': 'A',
            'ct': 'application/dns-json',
            }
        

        print(f'online DNS Query',server_name)        
        try:

            query_url = self.url + server_name
            ans = self.req.get( query_url , params=quary_params , headers={'accept': 'application/dns-json'} , verify=(not allow_insecure) )            

            # Parse the response as a DNS packet
            if (ans.status_code == 200):
                answer_msg = json.loads(ans.content)
                
                # resolved_ip = answer_msg['Answer'][0]['data']
                resolved_ip = None
                
                for x in answer_msg['Answer']:
                    if (x['type'] == 1):
                        resolved_ip = x['data']    # pick first ip in DNS answer                    
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


