from django.urls import path
from .auth import views as auth_views

urlpatterns = [
    # Auth
    path('login', auth_views.login, name='login'),
    path('register', auth_views.register, name='register'),
    path('logout', auth_views.logout, name='logout'),
    path('forgot-password', auth_views.forgot_password, name='forgot-password'),
    path('change-password', auth_views.change_password, name='change-password')
    #
]
