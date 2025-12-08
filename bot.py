import os
from telegram.ext import ApplicationBuilder, CommandHandler
from flask import Flask, request

TOKEN = os.getenv("8279748377:AAFnf8irohjfmRn3tYyrYf9sqNgIUiGrPIA")
print("TOKEN FROM ENV:", TOKEN)

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN missing in Render Environment Variables!")

app = Flask(__name__)

async def start(update, context):
    await update.message.reply_text("Bot is alive! 🚀")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    # Start webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
        webhook_url=f"{os.getenv('RENDER_EXTERNAL_URL')}/webhook"
    )

@app.post("/webhook")
def webhook():
    request_json = request.get_json(force=True)
    app.application.update_queue.put_nowait(request_json)
    return "OK", 200

if __name__ == "__main__":
    main()
