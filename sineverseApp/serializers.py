
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError


from django.utils import timezone

# ============ DAILY REWARD SERIALIZER ===================
# class ClaimRewardSerializer(serializers.Serializer):
#     tgID = serializers.CharField()

#     def validate(self, data):
#         try:
#             user = UserDetails.objects.get(tgID=data['tgID'])
#         except UserDetails.DoesNotExist:
#             raise serializers.ValidationError("User not found")

#         if not user.can_claim_reward():
#             raise serializers.ValidationError("Reward already claimed today")

#         return data

#     def update(self, instance, validated_data):

#         instance.last_claimed = timezone.now().date()
#         instance.reward_earned += 5000 
#         instance.save()
        
#         RewardHistory.objects.create(
#             user=instance,
#             amount_earned=5000,
#             claimed_date=timezone.now().date()
#         )

#         return instance


# class RewardHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RewardHistory
#         fields = ['amount_earned', 'claimed_date']



class WalletAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAddress
        fields = '__all__'


class ListOfInvitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfInvites
        fields = '__all__'


class SilverCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SilverCoin
        fields = ['amount']


class GoldCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldCoin
        fields = ['amount']

# ============ USER DETAILS SERIALIZER =============
class UserDetailsSerializer(serializers.ModelSerializer):
    # ============ ALL RELATED NAMES MODELS ==========
    silver_coin = SilverCoinSerializer(required=False, read_only=True)
    gold_coin = GoldCoinSerializer(read_only=True, required=False)
    wallet_address = WalletAddressSerializer(required=False, read_only=True)
    list_invites = ListOfInvitesSerializer(many=True, required=False, read_only=True)
    # reward_history = RewardHistorySerializer(many=True, read_only=True, required=False)

    referral_code = serializers.CharField(read_only=True)
    referred_by_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserDetails
        fields = '__all__'

    def create(self, validated_data):
        tgID = validated_data.get('tgID')
        if UserDetails.objects.filter(tgID=tgID).exists():
            raise ValidationError(f"User with tgID {tgID} already exists.")
        
        referred_by_code = validated_data.pop('referred_by_code', None)
        user = UserDetails.objects.create(**validated_data)

        if referred_by_code:
            try:
                referring_user = UserDetails.objects.get(referral_code=referred_by_code)
                user.referred_by = referring_user
                user.save() 
                
                referring_user.earned_energy += 2000  # Increase the referring user's energy
                referring_user.save()
            except UserDetails.DoesNotExist:
                pass

        user.save()
        return user
    

    
class ConvertCoinsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate(self, data):
        user = UserDetails.objects.get(id=data['user_id'])
        if user.silver_coin.amount < data['amount']:
            raise serializers.ValidationError("Not enough silver coins.")
        return data

class SocialTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = [
            'tgID', 
            'telegram_group_joined', 
            'telegram_channel_joined', 
            'x_page_followed', 
            'x_earned',
            'telegram_channel_earned', 
            'telegram_group_earned', 
        ]



from rest_framework import serializers
from .models import UserDetails

class ReferralSerializer(serializers.Serializer):
    referral_code = serializers.CharField(max_length=10)
    referee_id = serializers.IntegerField()

    def validate(self, data):
        try:
            inviter = UserDetails.objects.get(referral_code=data['referral_code'])
        except UserDetails.DoesNotExist:
            raise serializers.ValidationError("Invalid referral code.")

        try:
            referee = UserDetails.objects.get(pk=data['referee_id'])
        except UserDetails.DoesNotExist:
            raise serializers.ValidationError("Referee does not exist.")
        
        if referee.referred_by is not None:
            raise serializers.ValidationError("Referee has already been referred by someone.")
        
        return data



