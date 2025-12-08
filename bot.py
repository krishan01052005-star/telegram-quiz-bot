from telegram.ext import ApplicationBuilder
import os

TOKEN = os.getenv("TOKEN")

application = ApplicationBuilder().token(TOKEN).build()

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8443))

    application.run_web_app(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://telegram-quiz-bot-pbts.onrender.com/{TOKEN}"
    )

