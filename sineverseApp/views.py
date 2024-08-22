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
        user = UserDetails.objects.get(id=serializer.validated_data['tgID'])
        serializer.update(user, serializer.validated_data)
        return Response({"message": "Reward claimed successfully!"}, status=status.HTTP_200_OK)
    


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
        

class PerformTaskView(generics.UpdateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = SocialTaskSerializer

    def get_object(self):
        tgID = self.request.data.get('tgID')
        try:
            user = UserDetails.objects.get(id=tgID)
        except UserDetails.DoesNotExist:
            user = UserDetails.objects.create(id=tgID)
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
