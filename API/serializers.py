from rest_framework import serializers

from API.models import Employee, Bug


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


class DeleteEmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=[])

    class Meta:
        model = Employee
        fields = 'id'


class BugSerializer(serializers.ModelSerializer):
    reporter = serializers.CharField(source='reporter.username', read_only=True)
    solver = serializers.CharField(source='solver.username', read_only=True)

    class Meta:
        model = Bug
        fields = ('id', 'title', 'description', 'status', 'created_at', 'reporter', 'solver')


class ReportBugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = ('title', 'description')


class UpdateBugSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=[])

    class Meta:
        model = Bug
        fields = ('id', 'title', 'description')
