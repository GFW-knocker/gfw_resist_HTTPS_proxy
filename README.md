# آپدیت 22-3-1402
- یوتیوب ، گوگل پلی ، اینستاگرام ، واتساپ و توییتر به صورت مستقیم آزاد شد
- از نسخه pyprox_HTTPS_v3.0.py استفاده کنید
- مقدار num_fragment : برای همراه اول 80 الی 150 ،  برای ایرانسل 10 تا 40 
- برای استفاده از DNS خود cloudflare باید ip تمیز کلودفلر را جلوی cludflare-dns.com قرار دهید در قسمت offline DNS  
- با مشاهده فایل log تولید شده میتوانید دامنه و ایپی های فیلترشده را استخراج و در قسمت offline DNS با ایپی سالم اگر دارید جایگزین کنید.
- برای تست واتساپ یا گوگل پلی میتوانید با nekobox ، ترافیک گوشی را با پروتکل http روی پایتون هدایت کنید
- این کد صرفا اثبات ادعا است و ممکنه ایپی ها روی نت شما فیلتر باشد.
- انتشار اپ اندرویدی توسط یکی از دوستان به زودی.

 
# آپدیت 3-3-1402
- نسخه Direct_DoH تمام ip ها را از DoH میگیرد و محدودیت های comment و ... برطرف میشود (فقط روی برخی نت ها جواب میدهد چون برخی ip های گوگل برخی جاها فیلتر است)
- برای گوشی از پوشه اندروید استفاده کنید
- روی گوشی از اپلیکیشن nekobox یا matsuri استفاده کنید
- نسخه اصلی رو اکثر نت ها اوکیه ، رو ایرانسل بهتر


# یوتیوب و توییتر آزاد شد - بدون سرور
با این  "تیزافزار"  میتوانید فیلترینگ یوتیوب و توییتر را بدون هیچگونه سروری دور بزنید<br>
رو ایرانسل تضمینی جواب میده ، مابقی اپراتورها بگیرنگیر داره فعلا<br>
اگر روی نت شما ویدئو ها load نشد دو سه بار refresh صفحه بزنید و چند لحظه صبر کنید<br>
بخشی از مشکلات بخاطر محدودیت CORS در سرورهای گوگل میباشد<br> 
بزودی مجموعه آیپی های تمیز گوگل را اضافه خواهیم کرد<br>
این محصول آزمایشی بوده و کارکرد اصلی آن تحقیق روی فیلترینگ میباشد<br><br>
نحوه اجرا :
- پکیج های dnspython و requests را با دستور pip در cmd روی پایتون نصب کنید
- اسکریپ pyprox_HTTPS را اجرا کنید
- مرورگر خود را روی پروکسی HTTPS 127.0.0.1:4500 تنظیم کنید
- یا از v2rayN فایل کانفیگ custom را import کنید
- یا از nekobox ، matsuri ، nekoray یک کانفیگ دستی از نوع HTTP با آدرس 127.0.0.1 و پورت 4500 درست کنید ([راهنمایی](https://github.com/GFW-knocker/gfw_resist_HTTPS_proxy/tree/main/Android))
- اگر روی گوشی و vpn mode هستید باید برنامه python را از داخل v2ray مستثنی کنید 
- یوتیوب را باز کنید.
- این <a href="https://www.youtube.com/watch?v=EhegyoV3LOE">آموزش ویدئویی </a> مراحل توسط دوستمون <a href="https://github.com/gfwsidehustle">gfwsidehustle</a>  



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
<a href="https://github.com/Ehsanfarahi22/Bypassing-SNI-based-HTTPS-Filtering">a Fork</a> by <a href="https://github.com/Ehsanfarahi22">Ehsanfarahi22</a><br>
<a href="https://github.com/FarhadiAlireza">FarhadiAlireza</a><br>
<a href="https://github.com/free-the-internet">free-the-internet</a><br>
<a href="https://github.com/alirezafazeli8">FazeliTech</a><br>

3. & my lovely friends for everything<br>
<a href="https://t.me/ircfspace">IRCF.space</a><br>
<a href="https://twitter.com/isegaro">Segaro</a><br>







