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
    queryset = DailyReward.objects.all()
    serializer_class = DailyRewardSerializer

    def get(self, request, *args, **kwargs):
        # Assuming the user's tgID is passed in the request data
        tgID = request.data.get('tgID')
        user = UserDetails.objects.filter(tgID=tgID).first()

        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.now().date()
        last_reward = DailyReward.objects.filter(user=user).order_by('-last_claimed').first()

        if last_reward and last_reward.last_claimed == today:
            return Response({"detail": "Daily reward already claimed for today."}, status=status.HTTP_400_BAD_REQUEST)

        # Logic for calculating amount gained (this can be customized)
        amount_gained = 100  # Example fixed amount or could be random or based on logic

        # Create or update the daily reward
        daily_reward = DailyReward.objects.create(
            user=user,
            oldAmount=user.position,
            amountGained=amount_gained,
            trackEachDayCount=(last_reward.trackEachDayCount + 1) if last_reward else 1,
            last_claimed=today,
            tgID=user.tgID
        )

        # Update user’s position (energy level)
        user.position += amount_gained
        user.save()

        serializer = self.get_serializer(daily_reward)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


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