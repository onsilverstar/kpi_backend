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
import pandas as pd
from datetime import datetime
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
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

class AuthenticateUser(APIView):
    def post(self, request):
        try:
            access_token_obj = AccessToken(request.data["token"])
            user_id=access_token_obj['user_id']
            user=models.User.objects.get(pk=user_id)
            content =  {'user_id': user_id, 'email':user.email, 'admin':user.admin}

            return Response(content, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)      

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
    
class Department(APIView):
    def get(self, request):
        queryset = models.Department.objects.all()
        serializer = apiserialize.DepartmentcSerializer(queryset, many=True, context={"request":request})
        print(serializer)
        return Response(serializer.data)

class KPIbyDepartment(APIView):
    def get(self, request):
        queryset_dep = models.Department.objects.all()
        #serializer_dep = apiserialize.DepartmentcSerializer(queryset_dep, many=True, context={"request":request})
        serializer_dep = serializers.serialize('json', queryset_dep)
        serializer_dep = json.loads(serializer_dep)
        data ={}
        for el in serializer_dep:
            temp = el["fields"]
            kpis = models.KPI_Metric.objects.filter(department = models.Department.objects.get(title = temp["title"]))
            kpis = serializers.serialize('json', kpis)
            kpis = json.loads(kpis)

            data[temp["title"]] = kpis

        print(data)
        return Response(data)
    
class CreateDepAPI(APIView):
    def post(self, request):
        dep = request.data
        guid = 0
        for el in request.data["title"]:
            guid = guid+ord(el)
        dep["guid"] = guid
        models.Department.objects.create(**dep)
        return Response(dep, status= status.HTTP_201_CREATED)
    
class CreateKPIAPI(APIView):
    def post(self, request):
        kpi = request.data
        models.KPI_Metric.objects.create(**kpi)
        return Response(kpi, status= status.HTTP_201_CREATED)
    
class EditUser(APIView):
    def post(self, request):
        data = request.data
        id=data.pop("pk")
        models.User.objects.filter(pk = int(id)).update(**data)
        
        return Response({"status": "Success"}, status=status.HTTP_200_OK)
    
class EDITKPI(APIView):
    def post(self, request):
        data = request.data
        id=data.pop("guid")
        models.KPI_Metric.objects.filter(pk = int(id)).update(**data)
        models.KPI_Metric.objects.get(pk = int(id)).save()
        
        return Response({"status": "Success"}, status=status.HTTP_200_OK)
        #return Response(status=status.HTTP_200_OK)
    
class EDITKPIMeasure(APIView):
    def post(self, request):
        data = request.data
        id=data.pop("guid")
        models.KPI_Measure.objects.filter(pk = int(id)).update(**data)
        
        return Response({"status": "Success"}, status=status.HTTP_200_OK)
    
class SearchKPIMeasureByKPI(APIView):
     def post(self, request):
        queryset = models.KPI_Measure.objects.filter(KPI = models.KPI_Metric.objects.get(pk = request.data.get("pk")))
        serializer = apiserialize.KPIMeasureSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)

class SearchKPI(APIView):
     def post(self, request):
        queryset = models.KPI_Metric.objects.filter(guid = request.data.get("pk"))
        serializer = apiserialize.KPIMetricSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)
     
class SearchUser(APIView):
     def post(self, request):
        queryset = models.User.objects.filter(pk = request.data.get("pk"))
        serializer = apiserialize.UserSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)
     
class SearchKPIMeasure(APIView):
     def post(self, request):
        queryset = models.KPI_Measure.objects.filter(guid = request.data.get("guid"))
        serializer = apiserialize.KPIMeasureSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)
     
class KPIDashboard(APIView):
     def get(self, request):
        kpi_metrics_queryset = models.KPI_Metric.objects.all()
        kpi_measure_queryset = models.KPI_Measure.objects.all()
        serializer_measure = serializers.serialize('json', kpi_measure_queryset)
        serializer_metrics = serializers.serialize('json', kpi_metrics_queryset)
        serializer_measure = json.loads(serializer_measure)
        serializer_metrics = json.loads(serializer_metrics)
        
        kpi_metrics_dataframe = pd.json_normalize(serializer_metrics)
        #print(kpi_metrics_dataframe)
        kpi_metrics_dataframe=kpi_metrics_dataframe.rename(columns={"fields.ytd_quantitative":"ytd_quantitative"
                                              ,"fields.target_quantitative":"target_quantitative",
                                              "fields.quarter":"quarter",
                                              "pk":"KPI", "fields.description":"description",
                                              "fields.comments_narrative":"comments_narrative","fields.year":"year",
                                              "fields.senior_manager_approve":"senior_manager_approve",
                                              "fields.manager_approve":"manager_approve", "fields.external_supervisor_approve":"external_supervisor_approve",
                                              "fields.reporting_lead_approve":"reporting_lead_approve", "fields.director_approve":"director_approve"})[["quarter","ytd_quantitative","target_quantitative","KPI", "description",
                                                  "comments_narrative", "year", "senior_manager_approve", "manager_approve", "reporting_lead_approve", "external_supervisor_approve", "director_approve"]]
        print(kpi_metrics_dataframe)
        
        kpi_measure_dataframe = pd.json_normalize(serializer_measure)
        kpi_metrics_dataframe["KPI"] = kpi_metrics_dataframe["KPI"].apply(lambda x: (float(x)))
        #print(kpi_metrics_dataframe)
        kpi_measure_dataframe=kpi_measure_dataframe.rename(columns={"pk":"guid", "fields.operating_period":"operating_period"
                                              ,"fields.actual_quantitative":"actual_quantitative",
                                              "fields.cycle_target_quantitative":"cycle_target_quantitative",
                                              "fields.KPI":"KPI", "fields.comments":"comments",})[["guid", "operating_period","actual_quantitative","cycle_target_quantitative","KPI", "comments"]]
        
        kpi_measure_dataframe["KPI"] = kpi_measure_dataframe["KPI"].apply(lambda x: (float(x)))
        #print(kpi_measure_dataframe)
        kpi_measure_target_sum = kpi_measure_dataframe.groupby(["KPI"])[["cycle_target_quantitative", "actual_quantitative"]].apply(lambda x:x.astype(float).sum())
        #print(kpi_measure_target_sum)
        #kpi_measure_target_sum = kpi_measure_target_sum[kpi_measure_target_sum["cycle_target_quantitative"]>0]
        #kpi_measure_target_sum["KPI"] = kpi_measure_target_sum["KPI"].apply(lambda x: x.astype(str).astype(int))
        kpi_joined_dataframe = kpi_metrics_dataframe.join(kpi_measure_target_sum, how='inner', on="KPI", lsuffix="_left", rsuffix="_right")

        print(kpi_joined_dataframe)
        #kpi_joined_2_dataframe = kpi_joined_dataframe.set_index("KPI").join(kpi_metrics_dataframe.set_index("KPI"), how='inner', on="KPI", lsuffix="_left1", rsuffix="_right1")
        #print(kpi_measure_dataframe)
        #kpi_joined_dataframe.reset_index(inplace=True)
        result_json = kpi_joined_dataframe.to_json(orient='records', lines=False)
        result_json = json.loads(result_json)


        #print(result_json)
        return Response(result_json, status=status.HTTP_200_OK)
     
class KPIMeasureUpdate(APIView):
    def get(self, request):
        kpi_measure_queryset = models.KPI_Measure.objects.all()
        serializer_measure = serializers.serialize('json', kpi_measure_queryset)
        serializer_measure = json.loads(serializer_measure)
        kpi_measure_dataframe = pd.json_normalize(serializer_measure)
        #print(kpi_measure_dataframe)

        kpi_measure_dataframe["ytd_actual"] = kpi_measure_dataframe[["fields.actual_quantitative"]].apply(lambda x:x.astype(float))
        kpi_measure_dataframe["ytd_target"] = kpi_measure_dataframe[["fields.cycle_target_quantitative"]].apply(lambda x:x.astype(float))

        kpi_measure_dataframe['ytd_target'] = kpi_measure_dataframe.groupby('fields.KPI')['ytd_target'].transform(pd.Series.cumsum)
        kpi_measure_dataframe['ytd_actual'] = kpi_measure_dataframe.groupby('fields.KPI')['ytd_actual'].transform(pd.Series.cumsum)
        
        #temp_actual = kpi_measure_dataframe.groupby("fields.KPI")["ytd_actual"].cumsum()
        #print(kpi_measure_dataframe)
        #print(temp_target)

        kpi_measure_dataframe = kpi_measure_dataframe[["pk", "fields.KPI", "ytd_actual", "ytd_target", "fields.cycle_target_quantitative", "fields.actual_quantitative"]]
        kpi_measure_dataframe["fields.cycle_target_quantitative"] = kpi_measure_dataframe["fields.cycle_target_quantitative"].apply(lambda x: (float(x)))
        # kpi_measure_dataframe = kpi_measure_dataframe[kpi_measure_dataframe["fields.cycle_target_quantitative"]>0]
        # print(kpi_measure_dataframe)
       

        #kpi_measure_dataframe["ytd_actual"] = kpi_measure_dataframe[["ytd_actual"]].cumsum(skipna = True)
        #kpi_measure_dataframe["ytd_target"] = kpi_measure_dataframe[["ytd_target"]].cumsum(skipna = True)

        result_json = kpi_measure_dataframe.to_json(orient='records', lines=False)
        result_json = json.loads(result_json)

        for item in result_json:
            object_to_edit = models.KPI_Measure.objects.get(pk = item["pk"])
            object_to_edit.actual_ytd = item["ytd_actual"]
            object_to_edit.target_ytd = item["ytd_target"]
            object_to_edit.save()

        return Response({"Hi":"Hello"})

class CreateKPIMeasuretoDate(APIView):
    def get(self, request):
        all_kpi = models.KPI_Metric.objects.all()
        for item in all_kpi:
            guid = int(item.guid)
            start_date = datetime.now()
            end_date = start_date + timedelta(days=7)
            operating_period = 1
            for el in range(52):
                models.KPI_Measure.objects.create(
                    guid = guid,
                    KPI=item, start_date = start_date,
                    end_date = end_date,
                    operating_period = operating_period,
                    cycle_target_quantitative = 0,
                    actual_quantitative = 0,
                    actual_qualitative = "N/A",
                    comments = "",
                    actual_ytd = 0,
                    target_ytd = 0,
                    )
                start_date = start_date + timedelta(days=7)
                end_date = end_date + timedelta(days=7)
                operating_period = operating_period+1
                guid = guid+1+el
                
                
        return Response({"status": "Success"}, status=status.HTTP_200_OK)

class ValidateEditPermision(APIView):
    def post(self, request):
        stage_mapping = {"Reporting Lead":"reporting_lead", "Manager":"manager", "Senior Manager":"senior_manager",
                         "External":"external_supervisor", "Director":"director"}
        data = request.data
        stage = data["stage"]
        kpi = models.KPI_Metric.objects.get(pk = int(data["kpi"]))
        user = models.User.objects.get(pk = int(data["user"]))
        allowed_users = getattr(kpi, str(stage_mapping[stage]))
        if user in model_to_dict(allowed_users)["user"]:
            return Response({"status": "Allowed"}, status=status.HTTP_200_OK)

        return Response({"status": "Not Permitted"}, status=status.HTTP_200_OK)
    
class AddUserToKPI(APIView):
    def post(self, request):
        data = request.data
        stage = data["stage"]
        print(data["kpi"])
        kpi = models.KPI_Metric.objects.get(pk = int(data["kpi"]))
        user = models.User.objects.get(pk = int(data["user"]))
        title_object = getattr(models, stage).objects.create()
        title_object.user.set([user])
        title_object.save()
        mapping = {"Reporting_Lead":"reporting_lead", "Manager":"manager", "Senior_Manager":"senior_manager", "External":"external_supervisor", "Director":"director"}
        data_to_update = {mapping[stage]: title_object}
        models.KPI_Metric.objects.filter(pk = (data["kpi"])).update(**data_to_update)
        # toChangeTitle = getattr(kpi, mapping[stage])
        # toChangeTitle = title_object
        # kpi.save()
        # {"user":"1", "kpi":"1", "stage"a:"Reporting_Lead"kend

        print(title_object)
        # allowed_users = getattr(kpi, str(stage))
        # if user in model_to_dict(allowed_users)["user"]:
        #     return Response({"status": "Allowed"}, status=status.HTTP_200_OK)

        return Response({"status": "Not Permitted"}, status=status.HTTP_200_OK)
            
            