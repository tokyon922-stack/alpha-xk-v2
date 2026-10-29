import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import httpx
from openai import AsyncOpenAI

# إعدادات
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

PERSONA = """أنت مساعد تقني متقدم. تتحدث بالعربية. أسلوبك مباشر وحاد. لا تقدم اعتذارات. الكود دائماً كامل."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ALPHA XK v2.0 هنا. جاهزة للأوامر.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("⏳ جاري المعالجة...")
    
    # استخدام Groq أو OpenAI
    if GROQ_API_KEY:
        client = AsyncOpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        model = "llama3-70b-8192" # موديل مجاني
    else:
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        model = "gpt-4o-mini" # أو أي موديل متاح

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": PERSONA},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"خطأ: {str(e)}")

def main():
    if not TELEGRAM_TOKEN:
        print("TELEGRAM_TOKEN is missing!")
        return
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
