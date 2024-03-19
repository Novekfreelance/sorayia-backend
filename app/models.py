import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from . import managers
import uuid

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=30, null=False, blank=False, default='', unique=True)
    type = models.CharField(null=False, blank=False, max_length=10, default='free')
    credits_plan = models.PositiveIntegerField(null=False, blank=False, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=False)
    created_at = models.DateTimeField(null=False, blank=False, default=datetime.datetime.utcnow())
    update_at = models.DateTimeField(null=True, blank=True)

    # email = models.EmailField(blank=False, null=False, unique=True)

    objects = managers.UserManager()


class Folder(models.Model):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=False, blank=False, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=False, blank=False, default=datetime.datetime.utcnow())
    update_at = models.DateTimeField(null=True, blank=True)


class Avatar(models.Model):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(null=False, blank=False, max_length=30, default='')
    url = models.TextField(null=False, blank=False, default='')


class Bot(models.Model):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(null=False, blank=False, max_length=30, default='')
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model = models.CharField(null=False, blank=False, max_length=50)
    prompt = models.TextField(null=False, blank=False, default='')
    description = models.TextField(null=False, blank=False, default='')
    split_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False, default=datetime.datetime.utcnow())
    update_at = models.DateTimeField(null=True, blank=True)
    folders = models.ManyToManyField(Folder)


class Chat(models.Model):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(null=True, blank=False, max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=False, blank=False, default=datetime.datetime.utcnow())
    update_at = models.DateTimeField(null=True, blank=True)
    messages = models.ManyToManyField('Message', related_name='chat_messages')


class Message(models.Model):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    model = models.CharField(max_length=10, null=False, blank=False, default='system')
    content = models.TextField(null=False, blank=False, default='')
    type = models.CharField(max_length=10,null=False, blank=False, default='text')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(null=False, blank=False, default=datetime.datetime.utcnow())
    update_at = models.DateTimeField(null=True, blank=True)


class File(models.Model):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=False, blank=False,)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    url = models.TextField(null=False, blank=False)
    type = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False, default=datetime.datetime.utcnow())
    update_at = models.DateTimeField(null=True, blank=True)


class Contact(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)
