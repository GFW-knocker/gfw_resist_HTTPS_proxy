# Direct DNS-Over-Https (DoH)

# چیه این ؟
- مستقیم تمام ip ها را از DNS over HTTPS  (DoH) میگیرد بدون دخل و تصرف
- مقدار DNS_url را باید گزینه ای بگذارید که ایپی اش مسدود نباشد. مثلا سرور گوگل 8.8.8.8 روی یک نت مسدود و روی نت دیگر باز است
- اگر ip هایی که DoH برمیگرداند روی نت شما فیلتر نباشد ، سایت بالا خواهد آمد و محدودیت های comment و live و ... برطرف میشود
- تعداد فرگمنت را بین 10 تا 100 امتحان کنید و زمان فرگمنت بین 0.001 تا 0.01
- کافیست اسکریپت Direct_DoH.py را اجرا کنید مشابه توضیحات صفحه اول  
