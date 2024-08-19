from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(UserDetails)
admin.site.register(GoldCoin)
admin.site.register(SilverCoin)
admin.site.register(DailyReward)
admin.site.register(WalletAddress)
admin.site.register(ListOfInvites)
