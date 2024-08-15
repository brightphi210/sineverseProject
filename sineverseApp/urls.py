from django.urls import path
from .views import *


urlpatterns = [
    path('user_details/', UserDetailView.as_view(), name='user_details'),
    path('user_details/update/<str:pk>/', UserDetailsUpdateView.as_view(), name='user_update'),
    path('mine_boost/', BoostMineView.as_view(), name='mine_boost'),
    path('mine_boost/update/<str:pk>/', BoostMineUpdateView.as_view(), name='mine_update'),
    path('purchase_mine/', PurchaseMineView.as_view(), name='purchase_mine'),
    path('daily_reward/', DailyRewardView.as_view(), name='daily_reward'),
    path('daily_reward/update/<str:pk>/', DailyRewardView.as_view(), name='daily_reward'),


    # =================== WALLET ADDRESS ==================
    path('wallet_address/', WalletAddressView.as_view(), name='wallet_address'),
    path('wallet_address/update/<str:pk>/', WalletAddressUpdateView.as_view(), name='wallet_address_update'),
]