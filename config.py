import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
RADIO_JAVAN_ACCESS_KEY = os.getenv("RADIO_JAVAN_ACCESS_KEY")
MUSIC_API_BASE_URL = os.getenv("MUSIC_API_BASE_URL", "https://api.example.com/music")
MOVIE_API_BASE_URL = os.getenv("MOVIE_API_BASE_URL", "https://api.example.com/movies")
