# Generated by Django 3.1.7 on 2021-04-07 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_playerrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='other_total_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]
