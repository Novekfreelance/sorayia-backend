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
