# Generated by Django 5.0.6 on 2024-08-24 23:08

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0035_rewardhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyreward',
            name='amountGained',
        ),
        migrations.RemoveField(
            model_name='dailyreward',
            name='last_claimed',
        ),
        migrations.RemoveField(
            model_name='dailyreward',
            name='oldAmount',
        ),
        migrations.RemoveField(
            model_name='dailyreward',
            name='tgID',
        ),
        migrations.RemoveField(
            model_name='dailyreward',
            name='trackEachDayCount',
        ),
        migrations.RemoveField(
            model_name='dailyreward',
            name='user',
        ),
        migrations.RemoveField(
            model_name='rewardhistory',
            name='amount_earned',
        ),
        migrations.RemoveField(
            model_name='rewardhistory',
            name='claimed_date',
        ),
        migrations.AddField(
            model_name='dailyreward',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dailyreward',
            name='day',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='dailyreward',
            name='is_claimed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='rewardhistory',
            name='claimed_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='rewardhistory',
            name='reward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sineverseApp.dailyreward'),
        ),
        migrations.AlterField(
            model_name='rewardhistory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sineverseApp.userdetails'),
        ),
    ]
