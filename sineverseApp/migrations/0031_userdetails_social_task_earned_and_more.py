# Generated by Django 5.0.6 on 2024-08-22 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0030_alter_userdetails_last_claimed'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='social_task_earned',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='telegram_channel_joined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='telegram_group_joined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='x_page_followed',
            field=models.BooleanField(default=False),
        ),
    ]
