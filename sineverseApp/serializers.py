
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
    list_invites = ListOfInvitesSerializer(many=True, required=False, read_only=True)
    silver_coin = SilverCoinSerializer(required=False, read_only=True)
    gold_coin = GoldCoinSerializer(required=False, read_only=True)
    wallet_address = WalletAddressSerializer(required=False, read_only=True)

    class Meta:
        model = UserDetails
        fields = '__all__'

    def create(self, validated_data):
        tgID = validated_data.get('tgID')
        if UserDetails.objects.filter(tgID=tgID).exists():
            raise ValidationError(f"User with tgID {tgID} already exists.")
        return super().create(validated_data)