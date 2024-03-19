# Generated by Django 4.2.7 on 2024-03-01 02:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_bot_avatar_alter_bot_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='name',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='bot',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 1, 2, 52, 50, 498776)),
        ),
        migrations.AlterField(
            model_name='chat',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 1, 2, 52, 50, 499972)),
        ),
        migrations.AlterField(
            model_name='file',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 1, 2, 52, 50, 500961)),
        ),
        migrations.AlterField(
            model_name='folder',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 1, 2, 52, 50, 498080)),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 1, 2, 52, 50, 500499)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 1, 2, 52, 50, 495957)),
        ),
    ]
