import uuid

from rest_framework.serializers import ModelSerializer, ValidationError
from app import models
from rest_framework import serializers


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            # 'user'
        )
        model = models.Folder

        extra_kwargs = {
            'name': {'required': True, },
            # 'user': {'required': True, }
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
            'prompt',
            'avatar',
            'user'
        )

        extra_kwargs = {
            'name': {'required': True, },
            'model': {'required': True, },
            'description': {'required': True, },
            'prompt': {'required': True, },
            'avatar': {'required': True},
            'user': {'required': True}
        }


class BotCreationSerializer(serializers.ModelSerializer):
    # file = serializers.FileField(write_only=True)

    class Meta:
        model = models.Bot
        fields = (
            'name',
            # 'file',
            'model',
            'avatar',
            'prompt',
            'description',
        )

        extra_kwargs = {
            'name': {'required': True, },
            'prompt': {'required': True, },
            'model': {'required': True, },
            'avatar': {'required': True},
            'description': {'required': True},
        }

    def validate(self, data):
        print(data)
        return data


class BotUpdateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = models.Bot
        fields = (
            'name',
            'file',
            'model',
            'prompt',
            'avatar',
            'description',
        )

        extra_kwargs = {
            'name': {'required': False, },
            'file': {'required': False, },
            'model': {'required': False, },
            'prompt': {'required': False},
            'avatar': {'required': False},
            'description': {'required': False},
        }


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Avatar,
        fields = ('name', 'url')


class AvatarCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Avatar,
        fields = ('name', 'url')

        extra_kwargs = {
            'name': {'required': True, },
            'url': {'required': True}
        }


class AvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Avatar,
        fields = ('name', 'url')

        extra_kwargs = {
            'name': {'required': False, },
            'url': {'required': False, }
        }

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = ('bot',)

        extra_kwargs = {
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
            'bot'
        )


class MessageCreationSerializer(MessageSerializer):
    class Meta:
        model = models.Message
        fields = (
            'chat',
            'model',
            'content',
            'type',
            'bot'
        )
        extra_kwargs = {
            'chat': {'required': True, },
            'model': {'required': True, },
            'content': {'required': True},
            'type': {'required': True},
            'bot': {'required': True}
        }
