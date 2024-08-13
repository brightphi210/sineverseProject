
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

# ============ USER DETAILS SERIALIZER =============
class UserDetailsSerializer(serializers.ModelSerializer):
    # ============ ALL RELATED NAMES MODELS ==========
    mine_boost = MineBoostSerializer(many=True)
    daily_reward = DailyRewardSerializer(many=True)


    class Meta:
        model = UserDetails
        fields = '__all__'