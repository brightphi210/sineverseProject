
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError



# ============ MINE BOOST =============
class MineBoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MineBoost
        fields = '__all__'


# ================ PURCHASE SERIALISER =============
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseMine
        fields = '__all__'


# ============ DAILY REWARD SERIALIZER ===================
class DailyRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReward
        fields = '__all__'


class PurchaseMineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseMine
        fields = '__all__'    


class WalletAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAddress
        fields = '__all__'


class ListOfInvitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfInvites
        fields = '__all__'

# ============ USER DETAILS SERIALIZER =============
class UserDetailsSerializer(serializers.ModelSerializer):
    # ============ ALL RELATED NAMES MODELS ==========
    mine_boost = MineBoostSerializer(many=True, required=False)
    daily_reward = DailyRewardSerializer(many=True, required=False)
    wallet_address = WalletAddressSerializer(required=False)

    class Meta:
        model = UserDetails
        fields = '__all__'

    def create(self, validated_data):
        tgID = validated_data.get('tgID')
        if UserDetails.objects.filter(tgID=tgID).exists():
            raise ValidationError(f"User with tgID {tgID} already exists.")
        return super().create(validated_data)