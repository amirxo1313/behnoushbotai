# handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ai_responses import get_ai_response, get_joke, get_supportive_message, search_music
import requests
from config import MUSIC_API_BASE_URL, MOVIE_API_BASE_URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message and initializes user data."""
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    
    await update.message.reply_text(
        f"سلام بهنوش عزیزم! 😊 من BehnoushBotAI هستم، دوست هوشمند تو.\n"
        "اینجا می‌تونی آهنگ و فیلم‌های ایرانی رو پیدا کنی و با من گپ بزنی.\n"
        "هر وقت دلت گرفت یا خواستی یه جوک بشنوی، من اینجام تا حالت رو بهتر کنم.\n"
        "چیزی هست که بخوای برات انجام بدم بهنوش جان؟"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles general text messages and routes them to AI or search."""
    user_message = update.message.text
    user_id = update.effective_user.id
    
    if "جوک" in user_message or "خنده" in user_message:
        joke = get_joke()
        await update.message.reply_text(f"بهنوش جان، اینم یه جوک برات: {joke}")
    elif "حالم خوب نیست" in user_message or "غمگینم" in user_message or "افسرده" in user_message or "ناراحتم" in user_message:
        support_message = get_supportive_message()
        await update.message.reply_text(f"بهنوش عزیزم، {support_message}")
    elif "موسیقی" in user_message or "آهنگ" in user_message or "فیلم" in user_message or "ترانه" in user_message:
        await update.message.reply_text("بهنوش جان، می‌تونی اسم آهنگ، خواننده یا فیلم مورد نظرت رو بگی تا برات جستجو کنم.")
    else:
        ai_response = get_ai_response(user_message, user_id)
        await update.message.reply_text(f"بهنوش جان، {ai_response}")

async def search_music_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initiates a search for music or movies."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("بهنوش جان، لطفا بعد از دستور /search اسم آهنگ، خواننده یا فیلم مورد نظرت رو بنویس.")
        return

    await update.message.reply_text(f"بهنوش عزیزم، در حال جستجو برای '{query}' هستم...")

    try:
        response = requests.get(f"{MUSIC_API_BASE_URL}/search", params={"query": query})
        response.raise_for_status()
        data = response.json()

        music_results = data.get('music', [])
        movie_results = data.get('movies', [])

        if not music_results and not movie_results:
            await update.message.reply_text(f"بهنوش جان، متاسفانه نتیجه‌ای برای '{query}' پیدا نکردم. می‌تونی یه چیز دیگه امتحان کنی؟")
            return

        response_text = "بهنوش عزیزم، نتایج جستجو برای تو:\n\n"
        keyboard = []

        if music_results:
            response_text += "🎵 **موسیقی‌ها:**\n"
            for i, music in enumerate(music_results[:3]):
                title = music.get('title', 'Unknown Title')
                artist = music.get('artist', 'Unknown Artist')
                music_id = music.get('id')
                
                response_text += f"{i+1}. {title} - {artist}\n"
                keyboard.append([
                    InlineKeyboardButton(f"پخش {title}", callback_data=f"play_music_{music_id}"),
                    InlineKeyboardButton(f"دانلود {title}", callback_data=f"download_music_{music_id}")
                ])
            response_text += "\n"

        if movie_results:
            response_text += "🎬 **فیلم‌ها:**\n"
            for i, movie in enumerate(movie_results[:2]):
                title = movie.get('title', 'Unknown Title')
                director = movie.get('director', 'Unknown Director')
                movie_id = movie.get('id')
                
                response_text += f"{i+1}. {title} - {director}\n"
                keyboard.append([
                    InlineKeyboardButton(f"پخش {title}", callback_data=f"play_movie_{movie_id}"),
                    InlineKeyboardButton(f"دانلود {title}", callback_data=f"download_movie_{movie_id}")
                ])
            response_text += "\n"
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(response_text, reply_markup=reply_markup, parse_mode='Markdown')

    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"بهنوش جان، متاسفانه در حال حاضر نمی‌تونم جستجو رو انجام بدم. لطفا بعدا امتحان کن. (خطا: {e})")
    except Exception as e:
        await update.message.reply_text(f"بهنوش جان، یک خطای غیرمنتظره در حین جستجو رخ داد. لطفا دوباره امتحان کن. (خطا: {e})")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles inline keyboard button presses."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id

    if data.startswith("play_music_"):
        music_id = data.replace("play_music_", "")
        await query.edit_message_text(f"بهنوش جان، در حال آماده‌سازی پخش آنلاین موسیقی با ID: {music_id} هستم. امیدوارم لذت ببری! 🎶")
    elif data.startswith("download_music_"):
        music_id = data.replace("download_music_", "")
        await query.edit_message_text(f"بهنوش عزیزم، لینک دانلود موسیقی با ID: {music_id} به زودی برایت ارسال می‌شود. 📥")
    elif data.startswith("play_movie_"):
        movie_id = data.replace("play_movie_", "")
        await query.edit_message_text(f"بهنوش جان، در حال آماده‌سازی پخش آنلاین فیلم با ID: {movie_id} هستم. یه پاپ‌کورن آماده کن! 🍿")
    elif data.startswith("download_movie_"):
        movie_id = data.replace("download_movie_", "")
        await query.edit_message_text(f"بهنوش عزیزم، لینک دانلود فیلم با ID: {movie_id} به زودی برایت ارسال می‌شود. 🎬")

# =========== قسمت جدید (دستورات help و song) ===========

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "دستورات ربات:\n"
        "/start - شروع\n"
        "/help - راهنما\n"
        "/search [نام آهنگ/فیلم] - جستجوی آهنگ یا فیلم\n"
        "/song [نام آهنگ] - جستجوی فقط آهنگ\n"
        "همچنین می‌توانی هر وقت دوست داشتی با من صحبت کنی یا جوک بخواهی! 😊"
    )

async def song_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("لطفاً بعد از دستور /song نام آهنگ را وارد کن.")
        return
    response = search_music(query)
    await update.message.reply_text(response)
