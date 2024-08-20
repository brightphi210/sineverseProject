from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    tgID = models.CharField(max_length=255, blank=True, null=True)
    tgUsername = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.URLField(max_length=255, blank=True, null=True)
    position = models.IntegerField(default=0)
    maxEnergyLevel = models.IntegerField(default=2000)

    def __str__(self):
        return f"This is user {self.name}"


class SilverCoin(models.Model):
    user = models.OneToOneField(UserDetails, related_name='silver_coin', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"User {self.user.name} has {self.amount} silver coins."
    
class GoldCoin(models.Model):
    user = models.OneToOneField(UserDetails, related_name='gold_coin', on_delete=models.CASCADE, null=True , blank=True)
    amount = models.IntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return f"User {self.user.name} has {self.amount} gold coins."


class DailyReward(models.Model):
    user = models.OneToOneField(UserDetails, related_name='daily_reward', on_delete=models.CASCADE, blank=True, null=True)
    oldAmount = models.IntegerField(default=0)
    amountGained = models.IntegerField(default=0)
    trackEachDayCount = models.IntegerField(default=0)
    last_claimed = models.DateField(auto_now_add=True)
    tgID = models.CharField(blank=True, null=True, max_length=255)

    def _str__(self):
        return f"User {self.user.name} gained {self.amountGained} gold points on {self.last_claimed}."
    


class WalletAddress(models.Model):
    user = models.OneToOneField(UserDetails, related_name='wallet_address', on_delete=models.CASCADE, blank=True, null=True)
    walletAddress = models.CharField(max_length=255, blank=True, null=True)
    isConnected = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"User {self.user.name} has their wallet address: {self.walletAddress}."
    

class ListOfInvites(models.Model):
    user = models.ForeignKey(UserDetails, related_name='invites', on_delete=models.CASCADE, blank=True, null=True)
    inviteCode = models.CharField(max_length=255, blank=True, null=True)
    invitesName = models.CharField(max_length=255, blank=True, null=True)
    inviteCoinBalance = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"User {self.user.name} invited {self.invitesName} with a code {self.inviteCode} and balance {self.inviteCoinBalance}."
