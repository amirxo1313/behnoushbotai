# ai_responses.py
import openai
import google.generativeai as genai
from config import OPENAI_API_KEY, GEMINI_API_KEY, RADIO_JAVAN_ACCESS_KEY
import requests

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

def get_ai_response(user_message: str, user_id: int) -> str:
    """Generates a general AI response using OpenAI or Gemini, personalized for Behnoush."""
    # Use OpenAI for general conversation
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"کاربر: {user_message}\nربات (با لحن مهربان و دوستانه، به فارسی و با خطاب 'بهنوش جان' اگر نام کاربر بهنوش است):",
            max_tokens=100,
            temperature=0.7,
            stop=["\n"]
        )
        ai_text = response.choices[0].text.strip()
        return ai_text

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "بهنوش جان، متاسفانه الان نمی‌تونم بهت پاسخ بدم. یه مشکل کوچیک پیش اومده. 😔"

def search_music(query: str) -> str:
    """Search for music using Radio Javan API."""
    API_URL = "https://api.ineo-team.ir/rj.php"
    params = {
        'accessKey': RADIO_JAVAN_ACCESS_KEY,
        'action': 'search',
        'query': query
    }
    
    try:
        response = requests.post(API_URL, data=params)
        result = response.json()
        
        if result['status_code'] == 200:
            music_results = result['result']
            if music_results:
                response_text = "نتایج جستجو:\n"
                for i, music in enumerate(music_results[:3]):  # Limit to 3 results
                    title = music.get('title', 'Unknown Title')
                    artist = music.get('artist', 'Unknown Artist')
                    response_text += f"{i + 1}. {title} - {artist}\n"
                return response_text
            else:
                return "متاسفانه هیچ نتیجه‌ای پیدا نشد."
        else:
            return "بهنوش جان، متاسفانه در جستجو مشکلی پیش آمده است."

    except Exception as e:
        print(f"Radio Javan API Error: {e}")
        return "بهنوش جان، متاسفانه در حال حاضر نمی‌تونم بهت کمک کنم. لطفا بعدا امتحان کن."

def get_joke() -> str:
    """Generates a joke using OpenAI or a predefined list."""
    jokes = [
        "چرا کامپیوتر آهسته کار می‌کرد؟ چون رم کامپیوتر خوابش میومد!",
        "آقا یه تمساح چطوری تابستون رو می‌گذرونه؟ با کولر کروکودیلی!",
        "می‌دونی چرا دانشجوها ساندویچ دوست دارند؟ چون یه روز یه استاد گفت: هر کی تکلیفش رو نده ساندویچ میشه!",
        "بهنوش جان، می‌دونی چرا لک‌لک‌ها موقع خواب یه پاشون رو بالا نگه می‌دارن؟ چون اگه هر دو پاشون رو بذارن زمین، می‌افتن! 😂"
    ]
    
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="یه جوک کوتاه و بامزه به فارسی بگو:",
            max_tokens=50,
            temperature=0.8
        )
        joke = response.choices[0].text.strip()
        return joke
    except Exception as e:
        print(f"OpenAI Joke Error: {e}")
        import random
        return random.choice(jokes)

def get_supportive_message() -> str:
    """Generates a supportive message using Gemini or a predefined list."""
    supportive_messages = [
        "تو خیلی قوی‌تر از این حرفایی! می‌دونم می‌تونی از پس هر چیزی بربیای.",
        "بدونی که هر روز یه قدم به بهتر شدن نزدیک‌تر میشی؟ من همیشه اینجا هستم برات.",
        "زندگی مثل یه جعبه شکلاته، شاید بعضی مواقع مزه‌اش رو نفهمی اما هنوز شکلات‌های خوشمزه زیادی مونده!",
        "یادت باشه بهنوش جان، بعد از هر سختی، آسانی هست. من بهت ایمان دارم! 💖",
        "بهنوش عزیزم، لبخند تو قشنگ‌ترین چیزیه که می‌تونم ببینم. امیدوارم زودتر حالت خوب بشه."
    ]
    
    try:
        response = gemini_model.generate_content(
            "یک پیام کوتاه، مثبت و امیدبخش به فارسی برای کسی که کمی ناراحت است، با خطاب 'بهنوش جان' بنویس:",
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                max_output_tokens=80,
            )
        )
        message = response.text.strip()
        return message
    except Exception as e:
        print(f"Gemini Supportive Message Error: {e}")
        import random
        return random.choice(supportive_messages)
