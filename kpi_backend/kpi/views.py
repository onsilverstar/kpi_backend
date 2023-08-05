import os
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from django.core import serializers
from django.http import response, Http404, HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .utils import get_tokens_for_user
from . import models
from . import apiserialize
from.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authtoken.models import Token
import jwt
import json

# Create your views here.

class CreateUserAPI(APIView):
    # permission_classes = ("AllowAny",)
    # queryset = apiserialize.User.objects.get_or_create()
    # serializer_class = apiserialize.UserSeralizer

    def post(self, request):
        user = request.data
        serializer = apiserialize.UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.create(request.data)
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        print(apiserialize.UserSerializer(user))
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)