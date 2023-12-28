from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from app.bot import serializers
from app import models
from rest_framework.authtoken.models import Token
from rest_framework import status, exceptions
from rest_framework.serializers import Serializer

from app.helpers import upload_file


@swagger_auto_schema(tags=['file'], method='post', request_body=serializers.FolderSerializer)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_folder(request):
    folder_serializer = serializers.FolderSerializer(data=request.data)
    if folder_serializer.is_valid():
        folder_serializer.save()
    else:
        return Response(data=folder_serializer.errors, status=400)
    return Response(status=200)


@swagger_auto_schema(tags=['file'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_folder(request, folder_id):
    folder = models.Folder.objects.get(pk=folder_id)
    folder_serializer = serializers.FolderSerializer(data=request.data)
    if folder_serializer.is_valid():
        folder_serializer.update(folder, validated_data=folder_serializer.validated_data)
    else:
        return Response(data=folder_serializer.errors, status=400)
    return Response(status=200)


@swagger_auto_schema(tags=['file'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_folder(request, folder_id):
    try:
        folder = models.Folder.objects.get(pk=folder_id)
        folder.delete()
    except:
        return Response(data="Folder not found", status=404)
    return Response(status=200)


@swagger_auto_schema(tags=['file'], method='post', request_body=serializers.FileCreationSerializer)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_file(request):
    file_serializer = serializers.FileCreationSerializer(data=request.data)
    if file_serializer.is_valid():
        file = file_serializer.save()
        file_uploaded = upload_file(request.data['file'])
        file.__dict__.update({'url': file_uploaded})
        file.save()
    else:
        return Response(data=file_serializer.errors, status=400)

    return Response(status=200)


@swagger_auto_schema(tags=['file'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_file(request, file_id):
    try:
        file = models.File.objects.get(pk=file_id)
    except:
        return Response(data='File not Found', status=404)

    file_serializer = serializers.FileUpdateSerializer(data=request.data)
    if file_serializer.is_valid():
        file_serializer.update(file, validated_data=file_serializer.validated_data)
        if request.data['file'] is not None:
            file_uploaded = upload_file(request.data['file'])
            file.__dict__.update({'url': file_uploaded})
            file.save()
    else:
        return Response(data=file_serializer.errors, status=400)


@swagger_auto_schema(tags=['file'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_file(request, file_id):
    try:
        file = models.File.objects.get(pk=file_id)
        file.delete()
    except:
        return Response(data='File not Found', status=404)


# Bot


@swagger_auto_schema(tags=['bot'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def create_bot(request):
    bot_serializer = serializers.BotCreationSerializer(data=request.data)
    if bot_serializer.is_valid():
        bot = bot_serializer.save()
        file_uploaded = upload_file(request.data['file'])
        bot.__dict__.update({'avatar': file_uploaded})
        bot.save()

    else:
        return Response(data=bot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(tags=['bot'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_bot(request, bot_id):
    bot = models.Bot.objects.get(pk=bot_id)
    bot_serializer = serializers.BotUpdateSerializer(data=request.data)
    if bot_serializer.is_valid():
        bot_serializer.update(bot, validated_data=bot_serializer.validated_data)
        if request.data['file'] is not None:
            file_uploaded = upload_file(request.data['file'])
            bot.__dict__.update({'url': file_uploaded})
            bot.save()

    else:
        return Response(data=bot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)
