from django.urls import path
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
    path('update_foler/{folder_id}', bot_views.update_folder, name='update-folder'),
    path('delete_folder/{folder_id}', bot_views.delete_folder, name='delete-folder'),
    path('create_file', bot_views.create_file, name='create-file'),
    path('update_file/{file_id}', bot_views.update_file, name='update-file'),
    path('delete_file/{file_id}', bot_views.delete_file, name='delete-file'),

    # Bot
    path('create_bot', bot_views.create_bot, name='create-bot'),
    path('update_bot/{bot_id}', bot_views.update_bot, name='update-bot')
]
