from django.db import models


class EmployeeTypes(models.TextChoices):
    ADMINISTRATOR = 'A', 'Administrator'
    TESTER = 'T', 'Tester'
    PROGRAMMER = 'P', 'Programmer'


class AdministratorManager(models.Manager):
    def get_queryset(self):
        return super(AdministratorManager, self).get_queryset().filter(type=EmployeeTypes.ADMINISTRATOR)

    def create(self, **kwargs):
        kwargs.update({'type': EmployeeTypes.ADMINISTRATOR})
        return super(AdministratorManager, self).create(**kwargs)


class TesterManager(models.Manager):
    def get_queryset(self):
        return super(TesterManager, self).get_queryset().filter(type='t')

    def create(self, **kwargs):
        kwargs.update({'type': EmployeeTypes.TESTER})
        return super(TesterManager, self).create(**kwargs)


class ProgrammerManager(models.Manager):
    def get_queryset(self):
        return super(ProgrammerManager, self).get_queryset().filter(type='p')

    def create(self, **kwargs):
        kwargs.update({'type': EmployeeTypes.PROGRAMMER})
        return super(ProgrammerManager, self).create(**kwargs)
