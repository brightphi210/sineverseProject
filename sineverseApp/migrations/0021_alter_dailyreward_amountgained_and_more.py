# Generated by Django 5.0.6 on 2024-08-19 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0020_alter_userdetails_maxenergylevel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreward',
            name='amountGained',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dailyreward',
            name='oldAmount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dailyreward',
            name='trackEachDayCount',
            field=models.IntegerField(default=0),
        ),
    ]
