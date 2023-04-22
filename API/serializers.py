from rest_framework import serializers

from API.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'username', 'type')


class LoginEmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[])

    class Meta:
        model = Employee
        fields = ('username', 'password')


class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('username', 'password', 'type')


class UpdateEmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=[])
    username = serializers.CharField(validators=[])

    class Meta:
        model = Employee
        fields = ('id', 'username', 'password', 'type')
