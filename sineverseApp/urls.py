from django.urls import path
from .views import *


urlpatterns = [
    path('user_details', UserDetailView.as_view(), name='user_details'),
    path('user_details/update/<str:pk>/', UserDetailsUpdateView.as_view(), name='user_update'),
    
    
    path('gold_coin/<str:tgID>/', GoldCoinsView.as_view(), name='gold_coin'),
    path('silver_coin/<str:tgID>/', SilverCoinsView.as_view(), name='silver_coin'),
    path('claim_reward/', ClaimRewardView.as_view(), name='claim-reward'),

    # =================== WALLET ADDRESS ==================
    path('wallet_address/', WalletAddressView.as_view(), name='wallet_address'),
    path('wallet_address/update/<str:pk>/', WalletAddressUpdateView.as_view(), name='wallet_address_update'),
    path('list_invites/', ListOfInvitesView.as_view(), name='list_invites'),

    # path('perform_task/', PerformTaskView.as_view(), name='perform_task'),
    path('social_task/', PerformTaskView.as_view(), name='perform-task'),
    path('telegram_bot/', telegram_webhook, name='telegram-bot-endpoint'),

    path('referral/', ReferralView.as_view(), name='referral'),

]