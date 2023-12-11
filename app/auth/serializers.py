from rest_framework.serializers import ModelSerializer, ValidationError
from app import models
from rest_framework import serializers


class UserSerializer(ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'type',
        )


class UserCreationSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
            'phone',
        )

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