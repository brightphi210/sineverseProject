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

    def can_claim_reward(self):
        if self.last_claimed is None:
            return True
        return self.last_claimed < timezone.now().date()
    


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


class DailyReward(models.Model):
    user = models.OneToOneField(UserDetails, related_name='daily_reward', on_delete=models.CASCADE, blank=True, null=True)
    oldAmount = models.IntegerField(default=0)
    amountGained = models.IntegerField(default=0)
    trackEachDayCount = models.IntegerField(default=0)
    last_claimed = models.DateField(auto_now_add=True)
    tgID = models.CharField(blank=True, null=True, max_length=255)

    def _str__(self):
        return f"User {self.user.name} gained {self.amountGained} gold points on {self.last_claimed}."
    

class RewardHistory(models.Model):
    user = models.ForeignKey(UserDetails, related_name='reward_history', on_delete=models.CASCADE)
    amount_earned  = models.IntegerField()
    claimed_date  = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name} claimed {self.amount_earned} points on {self.claimed_date}"


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
