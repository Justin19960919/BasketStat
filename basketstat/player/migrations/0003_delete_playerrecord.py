# Generated by Django 3.1.7 on 2021-04-01 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_player_belongsto'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PlayerRecord',
        ),
    ]
