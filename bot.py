import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8279748377:AAFnf8irohjfmRn3tYyrYf9sqNgIUiGrPIA")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN missing in Render Environment Variables!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is live on Render! 🚀")

def main():
    print("TOKEN FROM ENV:", TOKEN)
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    print("Bot is starting... 🔥")
    application.run_polling()

if __name__ == "__main__":
    main()
