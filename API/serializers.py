from rest_framework import serializers
from API.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'username', 'type')

    @staticmethod
    def get_type(obj):
        return obj.get_type_display()


class LoginEmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[])

    class Meta:
        model = Employee
        fields = ('username', 'password')


class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('username', 'password', 'type')
