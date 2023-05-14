from django.urls import path
from API.views import *

urlpatterns = [
    path('employee-credentials', EmployeeCredentialsView.as_view()),
    path('admin-employees', AdminEmployeesView.as_view()),
    path('admin-employees/<int:employee_id>', AdminEmployeesView.as_view()),
    path('bugs', BugsView.as_view()),
    path('tester-bugs', TesterBugsView.as_view()),
    path('tester-bugs/<int:bug_id>', TesterBugsView.as_view()),
    path('get-programmer-bugs', GetProgrammerBugsView.as_view()),
    path('mark-bug-as-fixed', MarkBugAsFixedView.as_view()),
    path('mark-bug-as-unassigned', MarkBugAsUnassignedView.as_view()),
]
