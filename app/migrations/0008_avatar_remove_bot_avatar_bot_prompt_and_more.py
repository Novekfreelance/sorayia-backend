# Generated by Django 4.2.7 on 2024-02-12 21:31

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_bot_avatar_alter_bot_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=30)),
                ('url', models.TextField(default='')),
            ],
        ),
        migrations.RemoveField(
            model_name='bot',
            name='avatar',
        ),
        migrations.AddField(
            model_name='bot',
            name='prompt',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='bot',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 12, 21, 31, 35, 37419)),
        ),
        migrations.AlterField(
            model_name='chat',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 12, 21, 31, 35, 38516)),
        ),
        migrations.AlterField(
            model_name='file',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 12, 21, 31, 35, 39678)),
        ),
        migrations.AlterField(
            model_name='folder',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 12, 21, 31, 35, 36672)),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 12, 21, 31, 35, 39165)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 12, 21, 31, 35, 19922)),
        ),
    ]