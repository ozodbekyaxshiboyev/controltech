from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .enums import UserRoles
from .managers import StudentsManager
from .services import location_image,validate_image,custom_validator


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(verbose_name='Ism', max_length=50)
    last_name = models.CharField(verbose_name='Familiya', max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='Yosh')
    image = models.FileField(upload_to='users_images', validators=[validate_image, custom_validator],
                             help_text='2 mb gacha bo`lgan rasm yuklang', blank=True, null=True,
                             verbose_name="Profil rasmi")
    role = models.CharField(max_length=20, choices=UserRoles.choices(), blank=True, null=True)
    bio = models.CharField(max_length=200, default="")
    last_active = models.DateField(auto_now=True, null=True, blank=True)
    report_per = models.BooleanField(default=True)
    chat_per = models.BooleanField(default=True)
    task_per = models.BooleanField(default=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f" {self.role} {self.full_name}"


class Student(User):
    objects = StudentsManager()

    class Meta:
        proxy = True