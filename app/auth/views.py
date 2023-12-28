from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
from django.forms import model_to_dict
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from app.auth import serializers
from app import models
from rest_framework.authtoken.models import Token
from rest_framework import status, exceptions
from rest_framework.serializers import Serializer


# Create your views here.

# Auth


@swagger_auto_schema(tags=['auth'], method='post', request_body=serializers.UserAuth)
@api_view(['POST'])
def login(request):
    user_auth_serializer = serializers.UserAuth(data=request.data)
    if user_auth_serializer.is_valid():
        user = models.User.objects.filter(email=request.data['email']).first()
        if user is None:
            return Response(data={'error': 'email or password incorrect'}, status=400)
        if check_password(request.data['password'], user.password):
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                auth_data = {
                    'token': token.key,
                    'type': 'Token',
                    'user': model_to_dict(user, exclude=('password',))
                }
                return Response(data=auth_data, status=200)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='user is inactive')
        else:
            return Response(data={'error': 'email or password incorrect'}, status=400)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(tags=['auth'], method='post', request_body=serializers.UserCreationSerializer,)
@api_view(['POST'])
def register(request):
    user_creation_serializer = serializers.UserCreationSerializer(data=request.data)
    if user_creation_serializer.is_valid():
        user_creation_serializer.validated_data["password"] = make_password(
            user_creation_serializer.validated_data.get("password"))
        user = user_creation_serializer.save()
        current_site = 'https://sorayia-front-end.onrender.com'

        try:
            message = render_to_string(
                "app/EmailConfirmation.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(user.pk.bytes)
                }
            )

            email = user_creation_serializer.validated_data.get('email')

            mail_subject = "Confirmation d'email"

            mail = EmailMessage(mail_subject, message, to=[email])

            mail.content_subtype = 'html'

            mail.send()
        except:
            exceptions.APIException()
    else:
        return Response(user_creation_serializer.errors, status=400)
    return Response(status=200)


@swagger_auto_schema(tags=['auth'], method='post')
@api_view(['POST'])
def validate_email(request):
    user_id = urlsafe_base64_decode(request.data['id'])
    user = models.User.objects.get(pk=user_id)
    user.__dict__.update({'is_active': True})
    user.save()

    return Response(status=200)


@swagger_auto_schema(tags=['auth'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    token = Token.objects.get(key=request.auth)
    token.delete()
    return Response(status=200)


@swagger_auto_schema(tags=['auth'], method='post', request_body=Serializer(data={"email": ""}))
@api_view(['POST'])
def forgot_password(request):
    user = models.User.objects.filter(email=request.data['email']).first()
    if user:
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(tags=['auth'], method='post')
@api_view(['POST'])
def change_password(request):
    user = models.User.objects.get(pk=request.data['id'])
    user_password = request.data['password']
    new_password = request.data['new_password']

    if check_password(user_password, user.password):
        user.__dict__.update({'password': make_password(new_password)})
        user.save()

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
