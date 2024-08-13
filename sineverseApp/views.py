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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response(
                {'message': 'User created successfully'}, 
                status.HTTP_201_CREATED
            )
        else:
            return Response({'message': 'User creation failed'}, status.HTTP_401_UNAUTHORIZED)
        


# =============== USER DETAILS UPDATE ===================
class UserDetailsUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    lookup_field = 'pk'

    def update_user(self, serializer):
        instance = serializer.save()
        return instance




# ============= BOOST MINE ====================
class BoostMineView(generics.ListCreateAPIView):
    queryset = MineBoost.objects.all()
    serializer_class = MineBoostSerializer

    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response(
                {'message': 'Boost created successfully'},
                status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': 'Boost creation failed'}, 
                status.HTTP_401_UNAUTHORIZED
            )
        

# =============== BOOST MINE UPDATE ====================
class BoostMineUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MineBoost.objects.all()
    serializer_class = MineBoostSerializer
    lookup_field = 'pk'

    def update_mine(self, serializer):
        instance = serializer
        return instance
    

from django.utils import timezone
# ============= PURCHASE MINE ==================
class PurchaseMineView(generics.ListCreateAPIView):
    queryset = PurchaseMine.objects.all()
    serializer_class = PurchaseMineSerializer


# ============ DAILY REWARD =================
class DailyRewardView(generics.ListCreateAPIView):
    queryset = DailyReward.objects.all()
    serializer_class = DailyRewardSerializer

    def create(self, request, *args, **kwargs):
        user_details = DailyReward.objects.get(user=request.user)
        today = timezone.now().date()
        reward, created = DailyReward.objects.get_or_create(user=user_details)
        if reward.last_claimed == today:
            return Response(
                {"message": "Reward already claimed today."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            reward.last_claimed = today
            reward.trackEachDayCount += 1
            oldAmount = reward.amountGained
            reward.amountGained = reward.amountGained + oldAmount
            reward.save()
            return Response(
                {
                    "message": "Reward claimed successfully.", 
                    "amountGained": reward.amountGained
                },
                status=status.HTTP_201_CREATED
            )
