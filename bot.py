from telegram.ext import ApplicationBuilder
import os

TOKEN = os.getenv("8279748377:AAFnf8irohjfmRn3tYyrYf9sqNgIUiGrPIA")

application = ApplicationBuilder().token(TOKEN).build()

# TODO: your handlers here...

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8443))
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://telegram-quiz-bot-pbts.onrender.com/{TOKEN}"
    )
