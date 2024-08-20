# Generated by Django 5.0.6 on 2024-08-20 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0025_alter_goldcoin_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreward',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='daily_reward', to='sineverseApp.userdetails'),
        ),
        migrations.AlterField(
            model_name='silvercoin',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='silver_coin', to='sineverseApp.userdetails'),
        ),
        migrations.AlterField(
            model_name='walletaddress',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wallet_address', to='sineverseApp.userdetails'),
        ),
    ]
