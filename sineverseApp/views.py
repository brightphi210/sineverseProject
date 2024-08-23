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
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Define your bot token and endpoint
bot_token = '7459191551:AAGc8AEtA7fbRzFbFlGGgu4JlOtg8FYBl5c'
web_app_url = "https://t.me/sinversexyz_bot/sinverse"
welcome_message = "Welcome to Sinversexyz"

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
        send_message(chat_id, response)
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

def process_update(update):
    chat_id = update['message']['chat']['id']
    username = update['message']['from']['username']

    if 'text' in update['message'] and update['message']['text'].startswith('/start'):
        send_start_webapp_button_with_referer(chat_id, username)
    else:
        send_message(chat_id, "Invalid command \n/start")




@api_view(['POST'])
def telegram_webhook(request):
    update = request.data
    process_update(update)
    return JsonResponse({"status": "ok"}, status=200)


import requests

bot_token = '7459191551:AAGc8AEtA7fbRzFbFlGGgu4JlOtg8FYBl5c'
webhook_url = "https://sineverseproject.onrender.com/api/v1/telegram_bot/"
set_webhook_url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}"

response = requests.get(set_webhook_url)
print(response.json())