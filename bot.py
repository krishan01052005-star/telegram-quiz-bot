from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import os

# Load token from environment variable
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN env not found!")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Online! 🚀")

# App build
application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8443))
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://telegram-quiz-bot-pbts.onrender.com/{TOKEN}"
    )
