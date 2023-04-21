from django.db import models

from API.managers import EmployeeTypes, AdministratorManager, TesterManager, ProgrammerManager


class Employee(models.Model):
    username = models.CharField(max_length=24, unique=True, null=False)
    password = models.CharField(max_length=24, null=False)
    type = models.CharField(max_length=1, choices=EmployeeTypes.choices)


class EmployeeSession(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    session = models.CharField(max_length=15, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Administrator(Employee):
    objects = AdministratorManager()

    class Meta:
        proxy = True


class Tester(Employee):
    objects = TesterManager()

    class Meta:
        proxy = True


class Programmer(Employee):
    objects = ProgrammerManager()

    class Meta:
        proxy = True
