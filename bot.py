import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables from .env file
load_dotenv()

# Get API Keys from Environment Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your AI bot. Ask me anything.")

# Function to handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = get_gemini_ai_response(user_message)
    update.message.reply_text(response)

# Function to call Google Gemini AI API
def get_gemini_ai_response(user_input):
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": user_input}]}
        ]
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: {response_data.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        return f"API request failed: {str(e)}"

# Main function to run the bot
def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

# Run the bot
if __name__ == '__main__':
    main()