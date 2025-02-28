import telebot
import google.generativeai as genai
import os

# Load API keys from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot API Token
GENAI_API_KEY = os.getenv("GENAI_API_KEY")  # Google Gemini API Key

# Initialize the bot and Gemini AI
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
genai.configure(api_key=GENAI_API_KEY)

# Configure the AI model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

convo = model.start_chat(history=[])


# Start and Help Command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! This bot is made by Dayanand Gawade @dayanand_gawade")


# Text Message Handler
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    bot.send_chat_action(message.chat.id, "typing")  # Show typing action
    convo.send_message(message.text)
    response = convo.last.text
    bot.reply_to(message, response)


# Image Message Handler
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_chat_action(message.chat.id, "typing")  # Show typing action
    bot.reply_to(message, "I see you sent an image! Currently, I can only process text.")


# Run the bot
bot.infinity_polling()