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

class Users(APIView):
    def get(self, request):
        queryset = models.User.objects.all()
        serializer = apiserialize.UserSerializer(queryset, many=True, context={"request":request})
        print(serializer)
        return Response(serializer.data)
    
class KPIMeasure(APIView):
    def get(self, request):
        queryset = models.KPI_Measure.objects.all()
        serializer = apiserialize.KPIMeasureSerializer(queryset, many=True, context={"request":request})
        print(serializer)
        return Response(serializer.data)

class KPIMetric(APIView):
    def get(self, request):
        queryset = models.KPI_Metric.objects.all()
        serializer = apiserialize.KPIMetricSerializer(queryset, many=True, context={"request":request})
        print(serializer)
        return Response(serializer.data)
    
class EditUser(APIView):
    def post(self, request):
        data = request.data
        object_to_edit = models.User.objects.get(guid = data["guid"])
        update_data = json.loads(data["update_data"])

        for element_key in update_data.keys():
            object_to_edit.element_key = update_data[element_key]
        object_to_edit.save()
        print(object_to_edit.values())
        return Response({"status": data["status"]}, status=status.HTTP_200_OK)
    
class EDITKPI(APIView):
    def post(self, request):
        data = request.data
        object_to_edit = models.KPI_Metric.objects.get(guid = data["guid"])
        update_data = json.loads(data["update_data"])

        for element_key in update_data.keys():
            object_to_edit.element_key = update_data[element_key]
        object_to_edit.save()
        print(object_to_edit.values())
        return Response({"status": data["status"]}, status=status.HTTP_200_OK)
    
class EDITKPIMeasure(APIView):
    def post(self, request):
        data = request.data
        object_to_edit = models.KPI_Measure.objects.get(guid = data["guid"])
        update_data = json.loads(data["update_data"])

        for element_key in update_data.keys():
            object_to_edit.element_key = update_data[element_key]
        object_to_edit.save()
        print(object_to_edit.values())
        return Response({"status": data["status"]}, status=status.HTTP_200_OK)
    
class SearchKPIMeasureByKPI(APIView):
     def post(self, request):
        queryset = models.KPI_Measure.objects.filter(KPI = models.KPI_Metric.objects.get(guid = request.data.get("guid")))
        serializer = apiserialize.ProductSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)
    