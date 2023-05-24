# how to make your DoH server
1. install nginx<br>
<code>apt install nginx-light</code>
2. add these line in file
<code> /etc/nginx/sites-available/default </code><br>
<code>
# cloudflare HTTPS port [ 443 , 2053 , 2083 , 2087 , 2096 , 8443 ]
server {
  listen 8443 ssl default_server;	
  ssl_certificate    /root/my_cert/your_cert.pem;
  ssl_certificate_key    /root/my_cert/your_cert.key;	
  location /mycloudflare/ {
    proxy_pass https://cloudflare-dns.com:443/;
  }
  location /mygoogle/ {
    proxy_pass https://dns.google:443/;
  }	
}
</code>

3. reload nginx<br>
<code>systemctl daemon-reload</code><br>
<code>systemctl restart nginx</code><br>

4. use your DoH<br>
<code>Json Format:
DNS_url = 'https://your.site:8443/mygoogle/resolve?name='
DNS_url = 'https://your.site:8443/mycloudflare/dns-query?name='
Wire Format:
DNS_url = 'https://your.site:8443/mygoogle/dns-query?dns='
DNS_url = 'https://your.site:8443/mycloudflare/dns-query?dns='</code>

5. you can put your.site behind cloudflare but ensure that your.domain is resolved to clean ip 

# Additional Tutorial:
1. we have two DNS query standard<br>
<code>JSON format:
https://dns.google/resolve?name=yahoo.com
https://cloudflare-dns.com/dns-query?name=yahoo.com
WIRE format:
https://dns.google/dns-query?dns=B64encode
https://cloudflare-dns.com/dns-query?dns=B64encode</code>
2. test your server with curl<br>
<code>curl -H "accept: application/dns-json" https://your.site:8443/mygoogle/resolve?name=yahoo.com
  curl -H "accept: application/dns-json" https://your.site:8443/mycloudflare/dns-query?name=yahoo.com</code>



