# Generated by Django 5.0.6 on 2024-08-23 19:08

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0034_delete_dailyrewardhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='RewardHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_earned', models.IntegerField()),
                ('claimed_date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reward_history', to='sineverseApp.userdetails')),
            ],
        ),
    ]
