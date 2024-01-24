from uuid import UUID

from django.forms import model_to_dict
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

from app import helpers


@swagger_auto_schema(tags=['file'], method='post', request_body=serializers.FolderSerializer)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_folder(request):
    folder_serializer = serializers.FolderSerializer(data=request.data)
    if folder_serializer.is_valid():
        folder = folder_serializer.save(user=request.user)
    else:
        return Response(data=folder_serializer.errors, status=400)
    return Response(data=folder, status=200)


@swagger_auto_schema(tags=['file'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_folder(request, folder_id):
    folder = models.Folder.objects.get(pk=folder_id)
    folder_serializer = serializers.FolderSerializer(data=request.data)
    if folder_serializer.is_valid():
        folder=folder_serializer.update(folder, validated_data=folder_serializer.validated_data)
    else:
        return Response(data=folder_serializer.errors, status=400)
    return Response(data=model_to_dict(folder), status=200)


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


@swagger_auto_schema(tags=['file'], method='get')
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_folders(request):
    folders = models.Folder.objects.filter(user=request.user)
    return Response(data={"data": [model_to_dict(folder) for folder in folders]}, status=200)


@swagger_auto_schema(tags=['file'], method='post', request_body=serializers.FileCreationSerializer)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_file(request):
    file_serializer = serializers.FileCreationSerializer(data=request.data)
    if file_serializer.is_valid():
        folder = models.Folder.objects.get(pk=request.data['folder'])
        file_uploaded = helpers.upload_file(request.data['file'], folder.name)
        file_serializer.validated_data.pop('file')
        file = file_serializer.save(url=file_uploaded)
    else:
        return Response(data=file_serializer.errors, status=400)

    return Response(data=model_to_dict(file), status=200)


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
            helpers.delete_file_remote(file.url)
            file_uploaded = helpers.upload_file(request.data['file'])
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
@permission_classes([IsAuthenticated])
def create_bot(request):
    request_data = request.data
    bot_serializer = serializers.BotCreationSerializer(data=request_data)
    if bot_serializer.is_valid():
        file_uploaded = helpers.upload_file(request.data['file'], "avatar")
        bot_serializer.validated_data.pop('file')
        bot = bot_serializer.save(avatar=file_uploaded, user=request.user)
    else:
        return Response(data=bot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=model_to_dict(bot), status=status.HTTP_200_OK)


@swagger_auto_schema(tags=['bot'], method='put')
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_bot(request, bot_id):
    bot = models.Bot.objects.get(pk=bot_id)
    bot_serializer = serializers.BotUpdateSerializer(data=request.data)
    if bot_serializer.is_valid():
        bot_serializer.update(bot, validated_data=bot_serializer.validated_data)
        bot_serializer.validated_data.pop('file', None)
        if request.data.get('file') is not None:
            file_uploaded = helpers.upload_file(request.data['file'], "avatar")
            bot_serializer.validated_data['avatar'] = file_uploaded
            bot_serializer.update(bot, bot_serializer.validated_data)
        else:
            bot_serializer.update(bot, bot_serializer.validated_data)

    else:
        return Response(data=bot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=model_to_dict(bot), status=status.HTTP_200_OK)


# Converse

@swagger_auto_schema(tags=['bot'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_chat(request):
    request_data = request.data
    chat_serializer = serializers.ChatCreationSerializer(data=request_data)
    if chat_serializer.is_valid():
        chat = chat_serializer.save(user=request.user)
        return Response(data=model_to_dict(chat), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(tags=['bot'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_chat(request):
    chat_id = request.data['id']
    chat = models.Chat.objects.get(id=chat_id)
    messages = models.Message.objects.filter(chat_id=chat_id)

    response = {
        'chat': model_to_dict(chat),
        "messages": [model_to_dict(message) for message in messages]
    }

    return Response(response, status=200)


@swagger_auto_schema(tags=['bot'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_message(request):
    message_serializer = serializers.MessageCreationSerializer(data=request.data)
    bot = models.Bot.objects.get(pk=request.data['bot'])
    if message_serializer.is_valid():
        message_serializer.save(user=request.user)
        previous_messages = []
        previous_object = models.Message.objects.filter(chat__id=request.data['chat'])
        for message in previous_object:
            previous_messages.append({'type': message.model, 'message': message.content})
        print(previous_messages)
        gpt_response = helpers.send_gpt(
            context=bot.description,
            model=bot.model,
            human_prompt='{"read", "ty"}',
            human_input=request.data['content'],
            previous_messages=previous_messages
        )

        gpt_message = models.Message.objects.create(
            chat_id=request.data['chat'],
            bot_id=bot.pk,
            model='system',
            type='text',
            content=gpt_response,
            user_id=request.user.pk
        )
        gpt_message.save()

        return Response(model_to_dict(gpt_message), status=status.HTTP_200_OK)
    else:
        return Response(message_serializer.errors, status=status.HTTP_200_OK)
