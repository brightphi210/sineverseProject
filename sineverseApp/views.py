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


# =============== USER DETAILS UPDATE ===================
class UserDetailsUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    lookup_field = 'pk'

    def update_user(self, serializer):
        instance = serializer.save()
        return instance



class GoldCoinsView(generics.ListAPIView):
    queryset = GoldCoin.objects.all()
    serializer_class = GoldCoinSerializer


class SilverCoinsView(generics.ListAPIView):
    queryset = SilverCoin.objects.all()
    serializer_class = SilverCoinSerializer   


from django.utils import timezone

# ============ DAILY REWARD =================
class DailyRewardView(generics.ListCreateAPIView):
    queryset = DailyReward.objects.all()
    serializer_class = DailyRewardSerializer

    def create(self, request, *args, **kwargs):
        tgID = request.data.get('tgID')

        if not tgID:
            return Response(
                {"message": "tgID Required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = UserDetails.objects.get(tgID=tgID)
        except UserDetails.DoesNotExist:
            return Response(
                {"message": "User not found with given tgID."},
                status=status.HTTP_404_NOT_FOUND
            )

        today = timezone.now().date()
        reward, created = DailyReward.objects.get_or_create(user=user)

        if reward.last_claimed == today:
            return Response(
                {"message": "Reward already claimed today."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            reward.last_claimed = today
            reward.trackEachDayCount += 1
            oldAmount = reward.oldAmount
            reward.amountGained += oldAmount

            reward.save()
            return Response(
                {
                    "message": "Reward claimed successfully.", 
                    "amountGained": reward.amountGained,
                    "trackEachDayCount": reward.trackEachDayCount
                },
                status=status.HTTP_201_CREATED
            )

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