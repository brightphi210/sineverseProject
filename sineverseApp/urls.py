from django.urls import path
from .views import *


urlpatterns = [
    path('user_details', UserDetailView.as_view(), name='user_details'),
    path('user_details/update/<str:pk>/', UserDetailsUpdateView.as_view(), name='user_update'),
    
    
    path('gold_coin/<str:tgID>/', GoldCoinsView.as_view(), name='gold_coin'),
    # path('gold_coin/update/<str:pk>/', GoldCoinsViewUpdate.as_view(), name='gold_coin'),

    path('silver_coin/<str:tgID>/', SilverCoinsView.as_view(), name='silver_coin'),
    # path('silver_coin/update/<str:pk>/', SilverCoinsViewUpdate.as_view(), name='gold_coin'),
    
    # path('daily_reward/', DailyRewardView.as_view(), name='daily_reward'),
    # path('daily_reward/update/<str:pk>/', DailyRewardView.as_view(), name='daily_reward'),
    path('claim_reward/', ClaimRewardView.as_view(), name='claim-reward'),


    # =================== WALLET ADDRESS ==================
    path('wallet_address/', WalletAddressView.as_view(), name='wallet_address'),
    path('wallet_address/update/<str:pk>/', WalletAddressUpdateView.as_view(), name='wallet_address_update'),

    path('list_invites/', ListOfInvitesView.as_view(), name='list_invites'),

]