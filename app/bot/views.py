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
        folder_response = model_to_dict(folder, exclude=('user',))
        folder_response['user'] = model_to_dict(folder.user, exclude=('password',))
    else:
        return Response(data=folder_serializer.errors, status=400)
    return Response(data=folder_response, status=200)


@swagger_auto_schema(tags=['file'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_folder(request):
    try:
        folder_id = request.data.get('folder_id')
        folder = models.Folder.objects.get(pk=folder_id)
    except:
        return Response(data={"error": "Folder not found"}, status=404)
    folder_serializer = serializers.FolderSerializer(data=request.data)
    if folder_serializer.is_valid():
        folder = folder_serializer.update(folder, validated_data=folder_serializer.validated_data)
    else:
        return Response(data=folder_serializer.errors, status=400)
    return Response(data=model_to_dict(folder), status=200)


@swagger_auto_schema(tags=['file'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_folder(request):
    try:
        folder_id = request.data.get('folder_id')
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


@swagger_auto_schema(tags=['avatar'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_avatar(request):
    avatar_serializer = serializers.AvatarSerializer(data=request.data)
    if avatar_serializer.is_valid():
        avatar = avatar_serializer.save()
        return Response(status=200, data=model_to_dict(avatar))
    return Response(data=avatar_serializer.errors, status=400)


@swagger_auto_schema(tags=['avatar'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_avatar(request):
    try:
        avatar_id = request.data.get('avatar_id')
        avatar = models.Avatar.objects.get(pk=avatar_id)
    except:
        return Response(data={"error": "Avatar not found"}, status=404)
    avatar_serializer = serializers.AvatarSerializer(data=request.data)
    if avatar_serializer.is_valid():
        avatar = avatar_serializer.update(avatar, avatar_serializer.validated_data)
        return Response(data=model_to_dict(avatar), status=200)
    return Response(status=400, data=avatar_serializer.errors)


@swagger_auto_schema(tags=['avatar'], method='post')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_avatar(request):
    try:
        avatar = models.Avatar.objects.get(pk=request.data.get('avatar_id'))
    except:
        return Response(data={"error": "Avatar not found"})

    avatar.delete()

    return Response(status=200, data={'data': 'avatar_deleted'})


@swagger_auto_schema(tags=['avatar'], method='get')
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_avatars(request):
    avatars = models.Avatar.objects.all()
    return Response(data=[model_to_dict(data) for data in avatars], status=200)


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
        file = file_serializer.save(url=file_uploaded.get('public_url'), type=file_uploaded.get('type'))
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
            file_uploaded = helpers.upload_file(request.data['file'], file.folder.name)
            file.__dict__.update({'url': file_uploaded.get('public_url'), 'type': file_uploaded.get('type')})
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
        # file_uploaded = helpers.upload_file(request.data['file'], "avatar")
        # bot_serializer.validated_data.pop('file')
        bot = bot_serializer.save(user=request.user)

        folders_id = request.data['folders']
        print(folders_id)
        bot.folders.add(*folders_id)

        files_list = []
        for folder_id in folders_id:
            folder = models.Folder.objects.prefetch_related('file_set').get(pk=folder_id)
            files_list.extend(folder.file_set.all())
        response = helpers.make_split_doc(files_list)
        print(response)

        bot.__dict__.update({'split_url': response.get('public_url', None)})
        bot.save()
        bot_response = model_to_dict(bot, exclude=('folders',))
        bot_response['folders'] = [model_to_dict(folder_object) for folder_object in bot.folders.all()]
    else:
        return Response(data=bot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=bot_response, status=status.HTTP_200_OK)


@swagger_auto_schema(tags=['bot'], method='get')
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_bots(request):
    bots = models.Bot.objects.filter(user=request.user)
    bots_all = []
    for bot in bots:
        bot_response = model_to_dict(bot, exclude=('folders',))
        bot_response['folders'] = [model_to_dict(folder_object) for folder_object in bot.folders.all()]
        bots_all.append(bot_response)
    return Response(data={"data": bots_all}, status=200)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def associate_folder(request):
    folders_id = request.data['folders']
    folders_bot = models.Folder.objects.filter()
    files_list = []
    for folder_id in folders_id:
        folder = models.Folder.objects.prefetch_related('file_set').get(pk=folder_id)
        files_list.extend(folder.file_set.all())


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
    print(bot.description)
    if message_serializer.is_valid():
        message_serializer.save(user=request.user)
        previous_messages = []
        previous_object = models.Message.objects.filter(chat__id=request.data['chat'])
        for message in previous_object:
            previous_messages.append({'type': message.model, 'message': message.content})
        print(previous_messages)
        files_list = []
        for folder in bot.folders.all():
            # folder = models.Folder.objects.prefetch_related('file_set').get(pk=folder_id)
            files_list.extend(folder.file_set.all())
        response_splits = helpers.load_list_from_url(bot.split_url)

        gpt_response = helpers.send_gpt(
            context=bot.description,
            model=bot.model,
            human_prompt='{"question": "chat_history"}',
            human_input=request.data['content'],
            previous_messages=previous_messages,
            splits=response_splits
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
