import json
import requests

# Define your bot token and endpoint
bot_token = '7459191551:AAGc8AEtA7fbRzFbFlGGgu4JlOtg8FYBl5c'
web_app_url = "https://t.me/sinversexyz_bot/sinverse"
welcome_message = "Welcome to Sinversexyz"#RESPONSE MESSAGE


# Define the URL to set the webhook
#webhook_url = f"https://api.telegram.org/bot7459191551:AAGc8AEtA7fbRzFbFlGGgu4JlOtg8FYBl5c/setWebhook?url=https://sineverseproject.onrender.com/api/v1/telegram_bot/" #replace  bot_token and this script enpoint url

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
    encoded_keyboard = json.dumps(keyboard)
    image_path = "image.jpg"
    send_message_with_image(chat_id, welcome_message, image_path, encoded_keyboard)

# Get the incoming message data
def process_update(update):
    chat_id = update['message']['chat']['id']
    username = update['message']['from']['username']

    if 'text' in update['message'] and update['message']['text'].startswith('/start'):
        send_start_webapp_button_with_referer(chat_id, username)
        send_message(chat_id, "Start Working . . ")
    else:
        send_message(chat_id, "Invalid command \n/start")



# Main entry point for the webhook
def webhook(request):
    update = request.get_json()
    process_update(update)
    return "OK"


#call webhook(request) where request is the POST request data

