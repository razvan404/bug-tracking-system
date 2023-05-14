from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models import EmployeeSession
from API.serializers import *
from API.service import Service, UnauthorizedException, NotFoundException


class EmployeeCredentialsView(APIView):
    def post(self, request):
        # Login
        serializer = LoginEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data.get('username')
        password = serializer.data.get('password')
        try:
            employee = Service.find_employee(username=username, password=password)
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
            Service.create_session(employee=employee, session=self.request.session.session_key)
            return Response({}, status=status.HTTP_200_OK)
        except NotFoundException:
            return Response({'error': 'employee not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        # Find by session
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        try:
            employee = Service.find_employee(session=self.request.session.session_key)
            serialized = EmployeeSerializer(employee)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except NotFoundException:
            return Response({'error': 'employee not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        # Logout
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        try:
            Service.delete_session(session=self.request.session.session_key)
            return Response({}, status=status.HTTP_200_OK)
        except NotFoundException:
            return Response({'error': 'employee not logged in'}, status=status.HTTP_404_NOT_FOUND)


class AdminEmployeesView(APIView):
    def get(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        try:
            employees = Service.find_all_employees(session=self.request.session.session_key)
            serialized = EmployeeSerializer(employees, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except UnauthorizedException:
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # Create Employee
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = CreateEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        employee_type = serializer.data.get('type')

        try:
            Service.create_employee(session=self.request.session.session_key, employee_username=username,
                                    employee_password=password, employee_type=employee_type)
            return Response({'msg': 'account created successfully'}, status=status.HTTP_201_CREATED)
        except UnauthorizedException:
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    # Update Employee
    def put(self, request, employee_id: int):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = UpdateEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        employee_type = serializer.data.get('type')

        try:
            Service.update_employee(session=self.request.session.session_key, employee_id=employee_id,
                                    employee_username=username, employee_password=password,
                                    employee_type=employee_type)
            return Response({'msg': 'account updated successfully'}, status=status.HTTP_200_OK)
        except UnauthorizedException:
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except NotFoundException:
            return Response({'error': 'employee not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, employee_id: int):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        if not employee_id:
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Service.delete_employee(session=self.request.session.session_key, employee_id=employee_id)
            return Response({'msg': 'account deleted successfully'}, status=status.HTTP_200_OK)
        except UnauthorizedException:
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except NotFoundException:
            return Response({'error': 'employee not found'}, status=status.HTTP_404_NOT_FOUND)


class BugsView(APIView):
    def get(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists():
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = Bug.objects.all()
        serialized = BugSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class TesterBugsView(APIView):
    def get(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'tester':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        tester = queryset[0].employee
        bugs = tester.reported_bugs.all()
        serialized = BugSerializer(bugs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'tester':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        tester = queryset[0].employee
        serializer = BugDetailsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        title = serializer.data.get('title')
        description = serializer.data.get('description')
        bug = Bug(title=title, description=description, reporter=tester)
        bug.save()
        return Response({'msg': 'bug reported successfully'}, status=status.HTTP_201_CREATED)

    def patch(self, request, bug_id: int):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'tester':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = BugDetailsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        title = serializer.data.get('title')
        description = serializer.data.get('description')
        queryset = Bug.objects.filter(id=bug_id)
        if not queryset.exists():
            return Response({'error': 'bug not found'}, status=status.HTTP_404_NOT_FOUND)
        bug = queryset[0]
        if bug.status != 'unassigned':
            return Response({'error': 'bug already assigned'}, status=status.HTTP_400_BAD_REQUEST)
        bug.title = title
        bug.description = description
        bug.save(update_fields=['title', 'description'])
        return Response({'msg': 'bug updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, bug_id: int):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'tester':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = Bug.objects.filter(id=bug_id)
        if not queryset.exists():
            return Response({'error': 'bug not found'}, status=status.HTTP_404_NOT_FOUND)
        bug = queryset[0]
        if bug.status != 'unassigned':
            return Response({'error': 'bug already assigned'}, status=status.HTTP_400_BAD_REQUEST)
        bug.delete()
        return Response({'msg': 'bug deleted successfully'}, status=status.HTTP_200_OK)


class AssignBugView(APIView):
    def patch(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'programmer':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        programmer = queryset[0].employee
        bug_id = request.data.get('id')
        if not bug_id:
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Bug.objects.filter(id=bug_id)
        if not queryset.exists():
            return Response({'error': 'bug not found'}, status=status.HTTP_404_NOT_FOUND)
        bug = queryset[0]
        if bug.status != 'unassigned':
            return Response({'error': 'bug already assigned'}, status=status.HTTP_400_BAD_REQUEST)
        bug.status = 'assigned'
        bug.assigned_to = programmer
        bug.save(update_fields=['status', 'assigned_to'])
        return Response({'msg': 'bug assigned successfully'}, status=status.HTTP_200_OK)


class GetProgrammerBugsView(APIView):
    def get(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'programmer':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        programmer = queryset[0].employee
        bugs = programmer.bugs_to_solve.all()
        serialized = BugSerializer(bugs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class MarkBugAsFixedView(APIView):
    def patch(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'programmer':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        programmer = queryset[0].employee
        bug_id = request.data.get('id')
        if not bug_id:
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = programmer.bugs_to_solve.filter(id=bug_id)
        if not queryset.exists():
            return Response({'error': 'bug not found'}, status=status.HTTP_404_NOT_FOUND)
        bug = queryset[0]
        bug.status = 'fixed'
        bug.assigned_to = None
        bug.solved_by = programmer
        bug.save(update_fields=['status', 'assigned_to', 'solved_by'])
        return Response({'msg': 'bug marked as fixed successfully'}, status=status.HTTP_200_OK)


class MarkBugAsUnassignedView(APIView):
    def patch(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        queryset = EmployeeSession.objects.filter(session=self.request.session.session_key)
        if not queryset.exists() or queryset[0].employee.type != 'programmer':
            return Response({'error': 'user unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        programmer = queryset[0].employee
        bug_id = request.data.get('id')
        if not bug_id:
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = programmer.bugs_to_solve.filter(id=bug_id)
        if not queryset.exists():
            return Response({'error': 'bug not found'}, status=status.HTTP_404_NOT_FOUND)
        bug = queryset[0]
        bug.status = 'unassigned'
        bug.assigned_to = None
        bug.save(update_fields=['status', 'assigned_to'])
        return Response({'msg': 'bug marked as unassigned successfully'}, status=status.HTTP_200_OK)
