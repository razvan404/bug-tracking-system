from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models import Employee, EmployeeSession
from API.serializers import EmployeeSerializer, LoginEmployeeSerializer, CreateEmployeeSerializer


class LoginEmployeeView(APIView):
    def post(self, request):
        serializer = LoginEmployeeSerializer(data=request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data.get('username')
        password = serializer.data.get('password')
        queryset = Employee.objects.filter(username=username, password=password)

        if not queryset.exists():
            return Response({'error': 'employee not found'}, status=status.HTTP_404_NOT_FOUND)

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        employee = queryset[0]
        EmployeeSession.objects.create(employee=employee, session=self.request.session.session_key)
        return Response({}, status=status.HTTP_200_OK)


class GetEmployeeView(APIView):
    def get(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists():
            return Response({'error': 'employee not found'}, status=status.HTTP_404_NOT_FOUND)
        employee = queryset[0].employee
        serialized = EmployeeSerializer(employee)
        return Response(serialized.data, status=status.HTTP_200_OK)


class LogoutEmployeeView(APIView):
    def delete(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists():
            return Response({'error': 'employee not logged in'}, status=status.HTTP_404_NOT_FOUND)
        employee_session = queryset[0]
        employee_session.delete()
        return Response({}, status=status.HTTP_200_OK)


class GetAllEmployeesView(APIView):
    def get(self, request):
        queryset = Employee.objects.all()
        serialized = EmployeeSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class CreateEmployeeView(APIView):
    def put(self, request):
        serializer = CreateEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({}, status=status.HTTP_200_OK)
