# Generated by Django 5.0.6 on 2024-08-12 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sineverseApp', '0002_rename_telegramid_usedetails_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UseDetails',
            new_name='UserDetails',
        ),
    ]
