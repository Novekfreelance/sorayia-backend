import uuid

from rest_framework.serializers import ModelSerializer, ValidationError
from app import models
from rest_framework import serializers


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'user',
        )
        model = models.Folder

        extra_kwargs = {
            'name': {'required': True, },
            'user': {'required': True, }
        }


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = (
            'name',
            'url'
        )


class FileCreationSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=True)

    class Meta:
        model = models.File
        fields = (
            'name',
            'folder',
            'file'
        )

        extra_kwargs = {
            'name': {'required': True, },
            'folder': {'required': True, },
            'file': {'required': True, },
        }


class FileUpdateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = models.File
        fields = (
            'name',
            'file'
        )


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bot
        fields = (
            'name',
            'model',
            'description',
            'user'
        )

        extra_kwargs = {
            'name': {'required': True, },
            'model': {'required': True, },
            'description': {'required': True, },
            'user': {'required': True}
        }


class BotCreationSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = models.Bot
        fields = (
            'name',
            'file',
            'model',
            'description',
            'user'
        )

        extra_kwargs = {
            'name': {'required': True, },
            'file': {'required': True, },
            'model': {'required': True, },
            'description': {'required': True},
            'user': {'required': True}
        }

    def validate(self, data):
        print(data)
        return data


class BotUpdateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = models.Bot
        fields = (
            'name',
            'file',
            'model',
            'description',
        )

        extra_kwargs = {
            'name': {'required': True, },
            'file': {'required': False, },
            'model': {'required': True, },
            'description': {'required': True},
        }


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = ('user', 'bot')

        extra_kwargs = {
            'user': {'required': True, },
            'bot': {'required': True, },
        }


class ChatCreationSerializer(ChatSerializer):
    pass


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = (
            'chat',
            'model',
            'content',
            'type',
            'user',
            'bot'
        )


class MessageCreationSerializer(MessageSerializer):
    class Meta:
        extra_kwargs = {
            'chat': {'required': True, },
            'model': {'required': True, },
            'content': {'required': True},
            'type': {'required': True},
            'user': {'required': True},
            'bot': {'required': True}
        }
