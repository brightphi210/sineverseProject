# Generated by Django 5.0.6 on 2024-08-15 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0012_dailyreward_oldamount'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('walletAddress', models.CharField(blank=True, max_length=255, null=True)),
                ('isConnected', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wallet_address', to='sineverseApp.userdetails')),
            ],
        ),
    ]
