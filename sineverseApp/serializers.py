
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError



# ============ DAILY REWARD SERIALIZER ===================
class DailyRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReward
        fields = '__all__'



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
        fields = '__all__'


class GoldCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldCoin
        fields = '__all__'

# ============ USER DETAILS SERIALIZER =============
class UserDetailsSerializer(serializers.ModelSerializer):
    # ============ ALL RELATED NAMES MODELS ==========
    daily_reward = DailyRewardSerializer(required=False, read_only=True)
    silver_coin = SilverCoinSerializer(required=False, read_only=True)
    gold_coin = GoldCoinSerializer(read_only=True, required=False)
    wallet_address = WalletAddressSerializer(required=False, read_only=True)
    list_invites = ListOfInvitesSerializer(many=True, required=False, read_only=True)

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
                referring_user.earned_energy += 2000  # Increase the referring user's energy
                referring_user.save()
            except UserDetails.DoesNotExist:
                pass

        user.save()
        return user
    
