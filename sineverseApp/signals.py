from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserDetails, GoldCoin

@receiver(post_save, sender=UserDetails)
def create_wallet_address(sender, instance, created, **kwargs):
    if created:
        GoldCoin.objects.create(user_details=instance)