
from rest_framework import serializers
from .models import *



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
        fields = ['walletAddress', 'isConnected']

# ============ USER DETAILS SERIALIZER =============
class UserDetailsSerializer(serializers.ModelSerializer):
    # ============ ALL RELATED NAMES MODELS ==========
    mine_boost = MineBoostSerializer(many=True)
    daily_reward = DailyRewardSerializer(many=True)
    wallet_address = WalletAddressSerializer()


    class Meta:
        model = UserDetails
        fields = '__all__'