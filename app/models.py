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


class Bot(models.Model):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(null=False, blank=False, max_length=30)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    model = models.CharField(null=False, blank=False, max_length=20)
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, default=datetime.datetime.utcnow())
    update_at = models.DateTimeField(null=True, blank=True)


class Chat(models.Model):
    pass


class Message(models.Model):
    pass


class Folder(models.Model):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

class FolderBot(models.Model):
    pass

class Files(models.Model):
    pass
