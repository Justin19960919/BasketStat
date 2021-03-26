# Generated by Django 3.1.7 on 2021-03-24 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_game_gameurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='author',
            field=models.CharField(default='Put Author here', max_length=10),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(default='Put Content here', max_length=1000),
        ),
        migrations.AlterField(
            model_name='game',
            name='gameUrl',
            field=models.URLField(blank=True),
        ),
    ]
