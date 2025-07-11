# config.py
import os

# توکن ربات تلگرام خود را از BotFather دریافت کرده و در اینجا قرار دهید.
TELEGRAM_BOT_TOKEN = "8136898238:AAHRrQ-87-9zYy946cnLnmXtLhnzlrmJDDg"  

# کلید API اوپن‌ای‌آی خود را در اینجا قرار دهید.
OPENAI_API_KEY = "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"  

# کلید API جیمنای خود را در اینجا قرار دهید.
GEMINI_API_KEY = "AIzaSyC3dlsPFTT9WeSQiXhlFNViuB8CMdhVttA"  # کلید API جیمنای

# آیدی عددی تلگرام خود را در اینجا قرار دهید.
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))  # می‌توانید آیدی خود را به صورت عددی در اینجا قرار دهید.

# اطلاعات وب‌سرویس رادیو جوان
RADIO_JAVAN_ACCESS_KEY = "720466:3bb9f3a71ee015a604dd23af3f92c426"  # توکن دسترسی وب‌سرویس رادیو جوان

# آدرس‌های وب‌سرویس‌های موسیقی و فیلم ایرانی (در صورت نیاز)
MUSIC_API_BASE_URL = os.getenv('MUSIC_API_BASE_URL', "https://api.example.com/music")  # آدرس واقعی وب‌سرویس موسیقی
MOVIE_API_BASE_URL = os.getenv('MOVIE_API_BASE_URL', "https://api.example.com/movies")  # آدرس واقعی وب‌سرویس فیلم
