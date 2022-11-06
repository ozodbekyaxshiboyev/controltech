from django.db import models
from .enums import UserRoles
from django.contrib.auth.models import BaseUserManager



class StudentsManager(models.Manager):
    def get_queryset(self):
        return super(StudentsManager, self).get_queryset().filter(
            role=UserRoles.student.value)

    # def create(self, **kwargs):
    #     kwargs.update({'role': UserRoles.student.value})
    #     return super(StudetnsManager, self).create(**kwargs)