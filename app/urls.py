from django.urls import path

from . import consumers
from .auth import views as auth_views
from .bot import views as bot_views

urlpatterns = [
    # Auth
    path('login', auth_views.login, name='login'),
    path('register', auth_views.register, name='register'),
    path('logout', auth_views.logout, name='logout'),
    path('forgot_password', auth_views.forgot_password, name='forgot-password'),
    path('change_password', auth_views.change_password, name='change-password'),
    path('validate_email', auth_views.validate_email, name='validate-email'),

    # File
    path('create_folder', bot_views.create_folder, name='create-folder'),
    path('update_folder', bot_views.update_folder, name='update-folder'),
    path('delete_folder', bot_views.delete_folder, name='delete-folder'),
    path('get_folders', bot_views.get_folders, name='get-folders'),

    path('create_file', bot_views.create_file, name='create-file'),
    path('update_file/{file_id}', bot_views.update_file, name='update-file'),
    path('delete_file/{file_id}', bot_views.delete_file, name='delete-file'),

    # Bot
    path('create_bot', bot_views.create_bot, name='create-bot'),
    path('update_bot/<bot_id>', bot_views.update_bot, name='update-bot'),
    path('get_bots', bot_views.get_bots, name='get-bots'),

    # Converse
    path('create_chat', bot_views.create_chat, name='create-chat'),
    path('get_chat/<pk>', bot_views.get_chat, name='get-chat'),
    path('send_message', bot_views.send_message, name='send-message'),

    # Avatar
    path('create_avatar', bot_views.create_avatar, name='create-avatar'),
    path('update_avatar', bot_views.update_avatar, name='update-avatar'),
    path('delete_avatar', bot_views.delete_avatar, name='delete'),
    path('get_avatars', bot_views.get_avatars, name='get-avatars'),
]

