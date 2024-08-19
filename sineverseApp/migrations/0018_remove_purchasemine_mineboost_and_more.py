# Generated by Django 5.0.6 on 2024-08-19 14:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0017_alter_userdetails_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasemine',
            name='mineBoost',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='goldPoint',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='level',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='miningPoint',
        ),
        migrations.AddField(
            model_name='userdetails',
            name='maxEnergyLevel',
            field=models.IntegerField(blank=True, default=2000, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='position',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.CreateModel(
            name='GoldCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gold_coin', to='sineverseApp.userdetails')),
            ],
        ),
        migrations.CreateModel(
            name='SilverCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='silver_coin', to='sineverseApp.userdetails')),
            ],
        ),
        migrations.DeleteModel(
            name='MineBoost',
        ),
        migrations.DeleteModel(
            name='PurchaseMine',
        ),
    ]
