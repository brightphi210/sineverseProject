from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from . models import *
from . serializers import *
# Create your views here.



# ==================== USER DETAILS GET AND CREATE =================
class UserDetailView(generics.ListCreateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer

    def perform_create(self, serializer):
        referral_code = self.request.query_params.get('referrer_code')
        serializer.save(referred_by_code=referral_code)


# =============== USER DETAILS UPDATE ===================
class UserDetailsUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    lookup_field = 'pk'

    def update_user(self, serializer):
        instance = serializer.save()
        return instance



class GoldCoinsView(generics.UpdateAPIView):
    queryset = GoldCoin.objects.all()
    serializer_class = GoldCoinSerializer

    lookup_field = 'tgID'

    def update(self, request, *args, **kwargs):
        user_tgID = kwargs.get('tgID')
        try:
            user_details = UserDetails.objects.get(tgID=user_tgID)
        except UserDetails.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        gold_coin, created = GoldCoin.objects.get_or_create(user=user_details)

        serializer = self.get_serializer(gold_coin, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GoldCoinsViewUpdate(generics.RetrieveUpdateAPIView):
    queryset = GoldCoin.objects.all()
    serializer_class = GoldCoinSerializer
    lookup_field = 'pk'


class SilverCoinsView(generics.UpdateAPIView):
    queryset = SilverCoin.objects.all()
    serializer_class = SilverCoinSerializer 
    lookup_field = 'tgID'

    def update(self, request, *args, **kwargs):
        user_tgID = kwargs.get('tgID')
        try:
            user_details = UserDetails.objects.get(tgID=user_tgID)
        except UserDetails.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        silver_coin, created = SilverCoin.objects.get_or_create(user=user_details)

        serializer = self.get_serializer(silver_coin, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SilverCoinsViewUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = SilverCoin.objects.all()
    serializer_class = SilverCoinSerializer  


from django.utils import timezone

# ============ DAILY REWARD =================
class DailyRewardView(generics.ListCreateAPIView):
    pass

class ClaimRewardView(generics.UpdateAPIView):
    serializer_class = ClaimRewardSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserDetails.objects.get(tgID=serializer.validated_data['tgID'])
        serializer.update(user, serializer.validated_data)
        return Response({"message": "Reward claimed successfully!"}, status=status.HTTP_200_OK)



class RewardHistoryView(generics.ListAPIView):
    serializer_class = RewardHistorySerializer

    def get_queryset(self):
        user_tgID = self.request.query_params.get('tgID')
        try:
            user = UserDetails.objects.get(tgID=user_tgID)
        except UserDetails.DoesNotExist:
            return RewardHistory.objects.none()
        return RewardHistory.objects.filter(user=user).order_by('-claimed_date')

    


class WalletAddressView(generics.ListCreateAPIView):
    queryset = WalletAddress.objects.all()
    serializer_class = WalletAddressSerializer

    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            return Response({
                'message' : 'wallet address was created successfully',
            },
                status= status.HTTP_201_CREATED
            )
        

class WalletAddressUpdateView(generics.RetrieveUpdateAPIView):
    queryset = WalletAddress.objects.all()
    serializer_class = WalletAddressSerializer
    lookup_field = 'pk'

    def update_wallet(self, serializers):
        instance = serializers
        return instance
    

class ListOfInvitesView(generics.ListCreateAPIView):
    queryset = ListOfInvites.objects.all()
    serializer_class = ListOfInvitesSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({
                'message' : 'invite was created successfully',
            },
                status= status.HTTP_201_CREATED
            )
        
        else:
            return Response({
                'message' : 'invite creation failed',
            },
                status= status.HTTP_401_UNAUTHORIZED
            )
        

from rest_framework.exceptions import NotFound

class PerformTaskView(generics.UpdateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = SocialTaskSerializer

    def get_object(self):
        tgID = self.request.data.get('tgID')
        try:
            user = UserDetails.objects.get(tgID=tgID)  # Change 'id' to 'tgID'
        except UserDetails.DoesNotExist:
            raise NotFound({"message": "User not found"})
        return user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        task_type = request.data.get('task_type')

        if task_type == 'telegram_group' and not user.telegram_group_joined:
            user.telegram_group_joined = True
            user.telegram_group_earned += 20000
        elif task_type == 'telegram_channel' and not user.telegram_channel_joined:
            user.telegram_channel_joined = True
            user.telegram_channel_earned += 20000
        elif task_type == 'x_page_followed' and not user.x_page_followed:
            user.x_page_followed = True
            user.x_earned += 20000
        else:
            return Response(
                {"message": "Task already completed or invalid task type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.save()
        return Response(SocialTaskSerializer(user).data, status=status.HTTP_200_OK)



import json
import requests
import os
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Define your bot token and endpoint
bot_token = '7459191551:AAGc8AEtA7fbRzFbFlGGgu4JlOtg8FYBl5c'
web_app_url = "https://t.me/sinversexyz_bot/sinverse"
welcome_message = """ Welcome to Sinverse, the first R-Rated mafia metaverse built on the blockchain. 🎮 Tap your way to the top of the leaderboard and be among the 1,000 lucky players 🎯 invited to the SinVerse maiden lottery event! 🎟 Dare to win! 💰
"""
endpoint = "https://sineverseproject.onrender.com/api/v1/"


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

def send_message_with_image(chat_id, message, image_name, encoded_keyboard):
    api_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the image
    image_path = os.path.join(script_dir, image_name)

    with open(image_path, 'rb') as photo:
        # The 'files' parameter is specifically for file data (like images)
        files = {'photo': photo}

        # The 'data' parameter is for other form data
        data = {
            'chat_id': chat_id,
            'caption': message,
            'reply_markup': encoded_keyboard
        }

        # Sending the POST request with both data and files
        response = requests.post(api_url, data=data, files=files)
    return response.json()

def send_start_webapp_button_with_referer(chat_id, username):
    keyboard = {
        'inline_keyboard': [[
            {'text': 'Launch Sinersexyz 💰', 'url': web_app_url}
        ]]
    }
    encoded_keyboard = json.dumps(keyboard)
    image_path = "image.jpg"
    send_message_with_image(chat_id, welcome_message, image_path, encoded_keyboard)

# Get the incoming message data
def process_update(update):
    chat_id = update['message']['chat']['id']
    username = update['message']['from']['username']

    # Check if the update contains a message with text and starts with '/start'
    if 'message' in update and 'text' in update['message'] and update['message']['text'].startswith('/start'):
        # Extract the ref_code from the message
        start_command = update['message']['text'].split(' ', 1)

        if len(start_command) > 1:
            ref_code = start_command[1]

            # Prepare data for the API request
            data = {
                'ref_code': ref_code,
                'invited_id': username
            }
            url = f'{endpoint}/add_invite.php'

            # Send the POST request to the API
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=json.dumps(data))

            # Decode the JSON response
            response_data = response.json()

            # Check the response status
            if response_data.get('status') == 'success':
                # Send the welcome message with the inline keyboard
                send_start_webapp_button_with_referer(chat_id, username)
            else:
                # Handle error by sending a message to the user
                send_message(chat_id, f"{response_data.get('message', 'Error')} /start")
        else:
            send_start_webapp_button_with_referer(chat_id, username)
    else:
        # Handle the case where the text does not start with '/start'
        send_message(chat_id, "Invalid command\n/start")

@api_view(['POST'])
def telegram_webhook(request):
    update = request.data
    # update = request.get_json()
    process_update(update)
    return JsonResponse({"status": "ok"}, status=200)


# def webhook():
#     update = request.get_json()
#     process_update(update)


#     return "OK"

# @api_view(['POST'])
# def telegram_webhook(request):
#     update = request.data
#     process_update(update)
#     return JsonResponse({"status": "ok"}, status=200)