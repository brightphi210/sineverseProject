# Generated by Django 5.0.6 on 2024-08-19 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0021_alter_dailyreward_amountgained_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreward',
            name='last_claimed',
            field=models.DateField(auto_now_add=True),
        ),
    ]
