from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
import os
TOKEN = os.getenv("BOT_TOKEN")
print("TOKEN FROM ENV:", TOKEN)
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN missing in Render Environment Variables!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot: I'm alive! 🚀")

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

