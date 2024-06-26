"""
URL configuration for SorayiaAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from SorayiaAPI.routing import websocket_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="Sorayia-API",
        default_version='v1.0',
        description="API for sorayia app",
        terms_of_service="https://www.sorayia.com/terms/",
        contact=openapi.Contact(email="contact@sorayia.com"),
        license=openapi.License(name="MIT licence"),
    ),
    public=True,
)

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += websocket_urlpatterns
