from django.urls import path
from .views import *


urlpatterns = [
    path('user_details/', UserDetailView.as_view(), name='user_details'),
    path('user_details/update/<str:pk>/', UserDetailsUpdateView.as_view(), name='user_update'),
    path('mine_boost/', BoostMineView.as_view(), name='mine_boost'),
    path('mine_boost/update/<str:pk>/', BoostMineUpdateView.as_view(), name='mine_update'),
    path('purchase_mine/', PurchaseMineView.as_view(), name='purchase_mine'),
    path('daily_reward/', DailyRewardView.as_view(), name='daily_reward'),
]