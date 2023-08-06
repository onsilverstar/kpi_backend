from.models import User, KPI_Metric, KPI_Measure
from rest_framework import serializers
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class KPIMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI_Metric
        fields = '__all__'

class KPIMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI_Measure
        fields = '__all__'

    

   
