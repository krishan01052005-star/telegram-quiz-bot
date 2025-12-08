from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
import os

TOKEN = os.getenv("8279748377:AAFnf8irohjfmRn3tYyrYf9sqNgIUiGrPIA")  # ENV variable se token lo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is Running! 🎯")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    PORT = int(os.environ.get("PORT", 8443))
    
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://telegram-quiz-bot-pbts.onrender.com/{TOKEN}"
    )

if __name__ == "__main__":
    main()

