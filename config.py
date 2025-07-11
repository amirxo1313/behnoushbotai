# config.py
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # توکن ربات تلگرام خود را از BotFather دریافت کرده و در اینجا قرار دهید.
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # کلید API اوپن‌ای‌آی خود را در اینجا قرار دهید.
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # کلید API جیمنای خود را در اینجا قرار دهید.
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))  # آیدی عددی تلگرام خود را در اینجا قرار دهید.

# آدرس‌های وب‌سرویس‌های موسیقی و فیلم ایرانی
MUSIC_API_BASE_URL = os.getenv('MUSIC_API_BASE_URL', "https://api.example.com/music")  # آدرس واقعی وب‌سرویس موسیقی
MOVIE_API_BASE_URL = os.getenv('MOVIE_API_BASE_URL', "https://api.example.com/movies")  # آدرس واقعی وب‌سرویس فیلم
