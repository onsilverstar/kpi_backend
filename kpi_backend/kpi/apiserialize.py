from.models import User, KPI_Metric, KPI_Measure, Department
from rest_framework import serializers
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk","first_name", "last_name", "email", "admin")
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

class DepartmentcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    

   
