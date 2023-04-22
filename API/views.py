from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models import Employee, EmployeeSession, Bug, Tester
from API.serializers import EmployeeSerializer, LoginEmployeeSerializer, CreateEmployeeSerializer, \
    UpdateEmployeeSerializer, BugSerializer


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
        employee_session = EmployeeSession(employee=employee, session=self.request.session.session_key)
        employee_session.save()
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
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'administrator':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreateEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        employee_type = serializer.data.get('type')
        employee = Employee(username=username, password=password, type=employee_type)
        employee.save()
        return Response({'msg': 'account created successfully'}, status=status.HTTP_201_CREATED)


class UpdateEmployeeView(APIView):
    def patch(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'administrator':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        print(request.data)
        serializer = UpdateEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        employee_id = serializer.data.get('id')
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        employee_type = serializer.data.get('type')
        print(serializer.data)
        queryset = Employee.objects.filter(id=employee_id)
        if not queryset.exists():
            return Response({'error': 'employee not found'}, status=status.HTTP_404_NOT_FOUND)
        employee = queryset[0]
        employee.username = username
        employee.password = password
        employee.type = employee_type
        employee.save(update_fields=['username', 'password', 'type'])
        return Response({'msg': 'account updated successfully'}, status=status.HTTP_200_OK)


class DeleteEmployeeView(APIView):
    def delete(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'administrator':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        employee_id = request.data.get('id')
        if not employee_id:
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Employee.objects.filter(id=employee_id)
        if not queryset.exists():
            return Response({'error': 'employee not found'}, status=status.HTTP_404_NOT_FOUND)
        employee = queryset[0]
        employee.delete()
        return Response({'msg': 'account deleted successfully'}, status=status.HTTP_200_OK)


class GetAllBugsView(APIView):
    def get(self, request):
        queryset = Bug.objects.all()
        serialized = BugSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class GetTesterBugsView(APIView):
    def get(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists():
            return Response({'error': 'employee not found'}, status=status.HTTP_404_NOT_FOUND)
        employee = queryset[0].employee
        if employee.type != 'tester':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        bugs = employee.reported_bugs.all()
        serialized = BugSerializer(bugs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


