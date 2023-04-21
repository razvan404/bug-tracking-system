from django.urls import path
from API.views import *

urlpatterns = [
    path('login-employee', LoginEmployeeView.as_view()),
    path('get-employee', GetEmployeeView.as_view()),
    path('logout-employee', LogoutEmployeeView.as_view()),
    path('get-all-employees', GetAllEmployeesView.as_view()),
    path('create-employee', CreateEmployeeView.as_view()),
]
