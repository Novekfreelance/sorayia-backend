from rest_framework.serializers import ModelSerializer, ValidationError
from app import models
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'username',
            'email',
            'type',
        )


class UserCreationSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'username',
            'email',
            'password',
        )

        extra_kwargs = {
            'username': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False},
        }

        optional_fields = ['type', ]

    def validate_email(self, value):
        user_with_email = models.User.objects.filter(email=value).first()
        if user_with_email:
            raise ValidationError(detail='user with this email already exits')
        return value


class UserAuth(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'email',
            'password'
        )

        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False},
        }
