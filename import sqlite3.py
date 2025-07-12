import sqlite3

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
        conn.commit()
        await update.message.reply_text(f"خوش آمدی {name}!")
    except sqlite3.IntegrityError:
        await update.message.reply_text("شما قبلاً ثبت شده‌اید!")
    finally:
        conn.close()