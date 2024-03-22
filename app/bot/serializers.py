import uuid

from rest_framework.serializers import ModelSerializer, ValidationError
from app import models
from rest_framework import serializers
from app.auth.serializers import UserSerializer


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
    avatar = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    folders = serializers.SerializerMethodField()

    class Meta:
        model = models.Bot
        fields = (
            'id',
            'name',
            'model',
            'description',
            'prompt',
            'avatar',
            'user',
            'folders'
        )

    def get_avatar(self, obj):
        if obj.avatar:
            return AvatarSerializer(obj.avatar).data
        return None

    def get_user(self, obj):
        if obj.user:
            return UserSerializer(obj.user).data
        return None

    def get_folders(self, obj):
        if obj.folders:
            return [FolderSerializer(folder).data for folder in obj.folders.all()]


class BotCreationSerializer(serializers.ModelSerializer):
    # file = serializers.FileField(write_only=True)
    avatar = serializers.PrimaryKeyRelatedField(queryset=models.Avatar.objects.all())

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
    avatar = serializers.PrimaryKeyRelatedField(queryset=models.Avatar.objects.all())

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
        model = models.Avatar
        fields = ('id', 'name', 'url')


class AvatarCreationSerializer(AvatarSerializer):
    pass


class AvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Avatar
        fields = ('name', 'url')

        extra_kwargs = {
            'name': {'required': False, },
            'url': {'required': False, }
        }


class ChatSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    bot = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = models.Chat
        fields = ('id', 'bot', 'name', 'user', 'bot', 'messages')

    def get_user(self, obj):
        if obj.user:
            return UserSerializer(obj.user).data
        return None

    def get_bot(self, obj):
        if obj.bot:
            return BotSerializer(obj.bot).data
        return None

    def get_messages(self, obj):
        if obj.messages:
            return [MessageSerializer(message).data for message in obj.messages.all()]
        return None


class ChatCreationSerializer(serializers.ModelSerializer):
    bot = serializers.PrimaryKeyRelatedField(queryset=models.Bot.objects.all())

    class Meta:
        model = models.Chat
        fields = ('bot', 'name')

        extra_kwargs = {
            'bot': {'required': True},
            'name': {'required': True}
        }


class ChatUpdateSerializer(serializers.ModelSerializer):
    # bot = serializers.PrimaryKeyRelatedField(queryset=models.Bot.objects.all())

    class Meta:
        model = models.Chat
        fields = (
            # 'bot',
            'name',)

        extra_kwargs = {
            # 'bot': {'required': False},
            'name': {'required': False}
        }


class MessageSerializer(serializers.ModelSerializer):
    # chat = serializers.SerializerMethodField()
    bot = serializers.SerializerMethodField()

    class Meta:
        model = models.Message
        fields = (
            'id',
            'chat',
            'model',
            'content',
            'type',
            'bot'
        )

    def get_bot(self, obj):
        if obj.bot:
            return BotSerializer(obj.bot).data
        return None


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


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = ('username', 'email', 'message')
