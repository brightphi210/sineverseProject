# Generated by Django 5.0.6 on 2024-08-15 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0008_userdetails_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreward',
            name='tID',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
