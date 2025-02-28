import os
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables (Set these in Render)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Google Gemini API URL
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"

# Logging setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to get a response from Google Gemini API
def get_gemini_response(user_message):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"role": "user", "parts": [{"text": user_message}]}]}
    
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response_json = response.json()
        
        if "candidates" in response_json:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        return "Sorry, I couldn't generate a response."
    
    except Exception as e:
        return f"Error: {str(e)}"

# /start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your AI chatbot. Ask me anything.")

# Handle user messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    bot_response = get_gemini_response(user_message)
    update.message.reply_text(bot_response)

# Main function to start the bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
