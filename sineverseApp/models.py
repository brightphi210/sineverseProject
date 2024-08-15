from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    tgID = models.CharField(max_length=255, blank=True, null=True)
    tgUsername = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='images')
    miningPoint = models.IntegerField(blank=True, null=True)
    goldPoint = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    LEVELS = (
        ('Level 1', 'Level 1'),
        ('Level 2', 'Level 2'),
        ('Level 3', 'Level 3'),
    )
    level = models.CharField(choices=LEVELS, max_length=255, blank=True, null=True)

    def __str__(self):
        return f"This is user {self.name}"


class MineBoost(models.Model):
    user = models.ForeignKey(UserDetails, related_name='mine_boost', on_delete=models.CASCADE, blank=True, null=True)
    MINELEVELS = (
        ('Super Mine', 'Super Mine'),
        ('Silver Mine', 'Silver Mine'),
        ('Gold Mine', 'Gold Mine'),
    )

    superDescription = models.CharField(max_length=255, blank=True, null=True)
    silverDescription = models.CharField(max_length=255, blank=True, null=True)
    goldDescription = models.CharField(max_length=255, blank=True, null=True)
    mineBoostLevel = models.CharField(max_length=255, choices=MINELEVELS, blank=True, null=True)

    def __str__(self):
        return f"User {self.user.name} purchased {self.mineBoostLevel}  gold points."
    


class PurchaseMine(models.Model):
    mineBoost = models.ForeignKey(MineBoost, on_delete=models.CASCADE, null=True, blank=True)
    amountToPurchased = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"User {self.mineBoost.user.name} purchased {self.amountToPurchased} gold points from {self.mineBoost.mineBoostLevel} mine."


class DailyReward(models.Model):
    user = models.ForeignKey(UserDetails, related_name='daily_reward', on_delete=models.CASCADE, blank=True, null=True)
    oldAmount = models.IntegerField(default=0, blank=True, null=True)
    amountGained = models.IntegerField(default=0, blank=True, null=True)
    trackEachDayCount = models.IntegerField(default=0, null=True, blank=True)
    last_claimed = models.DateField(blank=True, null=True)
    tgID = models.CharField(blank=True, null=True, max_length=255)

    def _str__(self):
        return f"User {self.user.name} gained {self.amountGained} gold points on {self.laste_claimed}."
    


class WalletAddress(models.Model):
    user = models.ForeignKey(UserDetails, related_name='wallet_address', on_delete=models.CASCADE)
    walletAddress = models.CharField(max_length=255, blank=True, null=True)
    isConnected = models.BooleanField(default=False, blank=True, null=True)


    def __str__(self):
        return f"User {self.user.name} has their wallet address: {self.walletAddress}."
    

class ListInvites(models.Model):
    user = models.ForeignKey(UserDetails, related_name='invites', on_delete=models.CASCADE)
    inviteCode = models.CharField(max_length=255, blank=True, null=True)
    invitesName = models.CharField(max_length=255, blank=True, null=True)
    inviteCoinBalance = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"User {self.user.name} invited {self.invitesName} with a code {self.inviteCode} and balance {self.inviteCoinBalance}."
