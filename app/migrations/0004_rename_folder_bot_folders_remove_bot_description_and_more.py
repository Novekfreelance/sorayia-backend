# Generated by Django 4.2.7 on 2024-01-30 18:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_chat_created_at_chat_update_at_file_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bot',
            old_name='folder',
            new_name='folders',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='description',
        ),
        migrations.AddField(
            model_name='file',
            name='type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bot',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 30, 18, 26, 54, 220216)),
        ),
        migrations.AlterField(
            model_name='chat',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 30, 18, 26, 54, 221279)),
        ),
        migrations.AlterField(
            model_name='file',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 30, 18, 26, 54, 222213)),
        ),
        migrations.AlterField(
            model_name='folder',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 30, 18, 26, 54, 219801)),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 30, 18, 26, 54, 221739)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 30, 18, 26, 54, 217959)),
        ),
    ]