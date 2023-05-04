# آپدیت 14-2-1402
- برای گوشی از پوشه اندروید استفاده کنید
- با نت ایرانسل بهتر جواب میگیرید
# یوتیوب آزاد شد - بدون سرور - برای تمام اپراتورها مخصوصا ایرانسل
با این  "تیزافزار"  میتوانید فیلترینگ یوتیوب را بدون هیچگونه سروری دور بزنید<br>
رو ایرانسل تضمینی جواب میده ، مابقی اپراتورها بگیرنگیر داره فعلا<br>
اگر روی نت شما ویدئو ها load نشد دو سه بار refresh صفحه بزنید و چند لحظه صبر کنید<br>
بخشی از مشکلات بخاطر محدودیت CORS در سرورهای گوگل میباشد<br> 
بزودی مجموعه آیپی های تمیز گوگل را اضافه خواهیم کرد<br>
این محصول آزمایشی بوده و کارکرد اصلی آن تحقیق روی فیلترینگ میباشد<br><br>
نحوه اجرا :
- پکیج های dnspython و requests را با دستور pip در cmd روی پایتون نصب کنید
- اسکریپ pyprox_HTTPS را اجرا کنید
- مرورگر خود را روی پروکسی HTTPS 127.0.0.1:4500 تنظیم کنید
- یا از v2ray فایل کانفیگ custom را import کنید
- اگر روی گوشی هستید باید برنامه pycode را از داخل v2ray مستثنی کنید 
- یوتیوب را باز کنید.



# gfw_resist_HTTPS_proxy
- HTTPS proxy in single python script<br>
- Armed with <a href="https://github.com/GFW-knocker/gfw_resist_tls_proxy">Fragment technology</a><br>
- Equipped with Offline DNS Resolver<br>
- plus DNS-over-HTTPS (DoH)<br>
- plus IP Quality Analyzer<br>

# Directly bypass SNI and DNS filtering
- without any VPS or server<br>
- bypass SNI filtering using <a href="https://github.com/GFW-knocker/gfw_resist_tls_proxy">Fragment</a><br>
- bypass DNS filtering using DoH and offline DNS<br>

# swiss army to injure GFW
- for developers want to expriment around GFW<br>
<img src="/asset/swiss_army.png?raw=true" width="200" ><br>

# the structure
<img src="/asset/slide2.png?raw=true" width="600" ><br>

# how to run:
1. install these python package if you dont have<br>
<img src="/asset/install_packages.png?raw=true" width="500" ><br>
2. set up your browser to use HTTPS proxy<br>
<img src="/asset/firefox_proxy.png?raw=true" width="500" ><br><br>
 OR setup v2ray by importing custom config<br>
<img src="/asset/v2ray_custom.png?raw=true" width="500" ><br><br>
3. run python<br>
<code>python pyprox_HTTPS_v1.0.py</code><br>
4. surf the web & youtube<br>

# do Research on GFW
1. adjust parameters<br>
<img src="/asset/customize_params.png?raw=true"  ><br>
2. add your domain:ip to offline DNS to directly connect to it<br>
<img src="/asset/offline_DNS.png?raw=true"  ><br>
3. watch the log<br>
<img src="/asset/IP_Log.png?raw=true"  ><br>

# Acknowledgement
1. helping on DNS & DoH related things<br>
<a href="https://github.com/msasanmh/SecureDNSClient">SecureDNSClient</a> by <a href="https://github.com/msasanmh">msasanmh</a><br>
<a href="https://github.com/amirhosseinds">amirhosseinds</a><br>
<a href="https://github.com/J-Saeedi">J-Saeedi</a><br>
<a href="https://github.com/alidxdydz">alidxdydz</a><br>

2. helping on youtube related things<br>
<a href="https://github.com/Ehsanfarahi22">Ehsanfarahi22</a><br>
<a href="https://github.com/FarhadiAlireza">FarhadiAlireza</a><br>
<a href="https://github.com/free-the-internet">free-the-internet</a><br>

3. & my lovely friends for everything<br>
<a href="https://t.me/ircfspace">IRCF.space</a><br>
<a href="https://twitter.com/isegaro">Segaro</a><br>







