# main.py
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN
from handlers import start, handle_message, search_music_movie, button_callback, help_command, song_command
from db_manager import init_db

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    init_db()  # Initialize database

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search_music_movie))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("song", song_command))

    # Message handler (for general text messages)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Callback query handler (for inline keyboard buttons)
    application.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot started polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
