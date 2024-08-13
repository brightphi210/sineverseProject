from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
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
        return f"User {self.user.name} purchased {self.mineBoostLevel} for {self.amountToPurchased} gold points."
    


class PurchaseMine(models.Model):
    mineBoost = models.ForeignKey(MineBoost, on_delete=models.CASCADE, null=True, blank=True)
    amountToPurchased = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"User {self.mineBoost.user.name} purchased {self.amountToPurchased} gold points from {self.mineBoost.mineBoostLevel} mine."


class DailyReward(models.Model):
    user = models.ForeignKey(UserDetails, related_name='daily_reward', on_delete=models.CASCADE, blank=True, null=True)
    amountGained = models.IntegerField(blank=True, null=True)
    trackEachDayCount = models.IntegerField(default=0, null=True, blank=True)
    last_claimed = models.DateField(blank=True, null=True)

    def _str__(self):
        return f"User {self.user.name} gained {self.amountGained} gold points on {self.laste_claimed}."