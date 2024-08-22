import json
import requests

# Define your bot token and endpoint
bot_token = '7459191551:AAGc8AEtA7fbRzFbFlGGgu4JlOtg8FYBl5c'
web_app_url = "https://t.me/sinversexyz_bot/sinverse"
welcome_message = ""#RESPONSE MESSAGE
endpoint = "" #this particlar script endpoint

# Define the URL to set the webhook
webhook_url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={endpoint}" #replace  bot_token and this script enpoint url

def send_message(chat_id, message):
    api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(api_url, json=data)
    return response.json()

def send_message_with_image(chat_id, message, image_path, encoded_keyboard):
    api_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    with open(image_path, 'rb') as photo:
        data = {
            'chat_id': chat_id,
            'caption': message,
            'photo': photo,
            'reply_markup': encoded_keyboard
        }
        response = requests.post(api_url, files=data)
    return response.json()

def send_start_webapp_button_with_referer(chat_id, username):
    keyboard = {
        'inline_keyboard': [[
            {'text': 'Launch XMeme 💰', 'url': web_app_url}
        ]]
    }
