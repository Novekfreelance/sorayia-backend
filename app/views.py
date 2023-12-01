from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

#Auth


@swagger_auto_schema(tags=['auth'], method='post',)
@api_view(['POST'])
def login():
    return Response()


@swagger_auto_schema(tags=['auth'], method='post',)
@api_view(['POST'])
def register():
    pass


@swagger_auto_schema(tags=['auth'], method='post', security=[{"Bearer": []}], )
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout():
    pass



