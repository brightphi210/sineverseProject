from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist  # Import for exception handling

from django.utils import timezone
# Create your models here.
class UserDetails(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    tgID = models.CharField(max_length=255, blank=True, null=True)
    tgUsername = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.URLField(max_length=255, blank=True, null=True)
    position = models.IntegerField(default=0)
    maxEnergyLevel = models.IntegerField(default=2000)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    earned_energy = models.IntegerField(default=0)
    reward_earned = models.IntegerField(default=0)
    last_claimed = models.DateField(blank=True, null=True)

    telegram_group_joined = models.BooleanField(default=False)
    telegram_channel_joined = models.BooleanField(default=False)
    x_page_followed = models.BooleanField(default=False)
    x_earned = models.IntegerField(default=0)
    telegram_channel_earned = models.IntegerField(default=0)
    telegram_group_earned = models.IntegerField(default=0)

    def __str__(self):
        return f"This is user {self.name}"
    

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        # Generates a unique referral code (e.g., using a hash or random string)
        import random, string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # def can_claim_reward(self):
    #     if self.last_claimed is None:
    #         return True
    #     return self.last_claimed < timezone.now().date()

    def claim_reward(self, day):
        try:
            reward = DailyReward.objects.get(day=day)
        except DailyReward.DoesNotExist:
            raise ValueError("Invalid reward day.")
        
        if reward.is_claimed:
            raise ValueError("Reward for this day has already been claimed.")
        
        today = timezone.now().date()
        
        # If any day before this day is unclaimed, remove all claims
        if self.last_claimed and day > (self.last_claimed.day + 1):
            RewardHistory.objects.filter(user=self).delete()
            self.silver_coin.amount = 0
            self.save()
        
        # Claim reward for this day
        self.silver_coin.amount += reward.amount
        reward.is_claimed = True
        reward.save()
        
        RewardHistory.objects.create(user=self, reward=reward)
        self.last_claimed = timezone.now().date()
        self.save()
    
    def convert_silver_to_gold(self):
        
        try:
            silver_coin = SilverCoin.objects.get(user=self)
        except ObjectDoesNotExist:
            raise ValueError("SilverCoin record does not exist for this user.")
        
        try:
            gold_coin = GoldCoin.objects.get(user=self)
        except ObjectDoesNotExist:
            # Create a new GoldCoin record if it does not exist
            gold_coin = GoldCoin(user=self, amount=0)
        
        if silver_coin.amount >= 25000000:
            gold_conversion = silver_coin.amount // 25000000
            gold_coin.amount += gold_conversion
            silver_coin.amount -= gold_conversion * 25000000
            
            silver_coin.save()
            gold_coin.save()
        else:
            raise ValueError("Not enough silver coins to convert to gold.")

class SilverCoin(models.Model):
    user = models.OneToOneField(UserDetails, related_name='silver_coin', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"User {self.amount} silver coins."
    
class GoldCoin(models.Model):
    user = models.OneToOneField(UserDetails, related_name='gold_coin', on_delete=models.CASCADE, null=True , blank=True)
    amount = models.IntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return f"User {self.amount} gold coins."


# class DailyReward(models.Model):
#     user = models.OneToOneField(UserDetails, related_name='daily_reward', on_delete=models.CASCADE, blank=True, null=True)
#     oldAmount = models.IntegerField(default=0)
#     amountGained = models.IntegerField(default=0)
#     trackEachDayCount = models.IntegerField(default=0)
#     last_claimed = models.DateField(auto_now_add=True)
#     tgID = models.CharField(blank=True, null=True, max_length=255)

#     def _str__(self):
#         return f"User {self.user.name} gained {self.amountGained} gold points on {self.last_claimed}."
    

# class RewardHistory(models.Model):
#     user = models.ForeignKey(UserDetails, related_name='reward_history', on_delete=models.CASCADE)
#     amount_earned  = models.IntegerField()
#     claimed_date  = models.DateField(default=timezone.now)

#     def __str__(self):
#         return f"{self.user.name} claimed {self.amount_earned} points on {self.claimed_date}"



class DailyReward(models.Model):
    day = models.IntegerField(unique=True, null=True, blank=True)  # 1 to 9
    amount = models.IntegerField(null=True, blank=True)
    is_claimed = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return f"Day {self.day} Reward: {self.amount} silver coins"
    
    @classmethod
    def initialize_rewards(cls):
        # Initialize rewards for each day
        rewards = [
            (1, 1000),
            (2, 2500),
            (3, 5000),
            (4, 15000),
            (5, 25000),
            (6, 100000),
            (7, 500000),
            (8, 1000000),
            (9, 5000000),
            # Add other days
        ]
        for day, amount in rewards:
            cls.objects.get_or_create(day=day, defaults={'amount': amount})

class RewardHistory(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True, blank=True)
    reward = models.ForeignKey(DailyReward, on_delete=models.CASCADE, null=True, blank=True)
    claimed_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} claimed Day {self.reward.day} reward"




class WalletAddress(models.Model):
    user = models.OneToOneField(UserDetails, related_name='wallet_address', on_delete=models.CASCADE, blank=True, null=True)
    walletAddress = models.CharField(max_length=255, blank=True, null=True)
    isConnected = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"User {self.user.name} has their wallet address: {self.walletAddress}."
    

class ListOfInvites(models.Model):
    user = models.ForeignKey(UserDetails, related_name='invites', on_delete=models.CASCADE, blank=True, null=True)
    invitesName = models.CharField(max_length=255, blank=True, null=True)
    inviteCoinBalance = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"User {self.user.name} invited {self.invitesName} with a code {self.inviteCode} and balance {self.inviteCoinBalance}."
