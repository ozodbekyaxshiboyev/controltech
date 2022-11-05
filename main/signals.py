from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models import Report

# @receiver(pre_save, sender=Report)
# def my_handler(sender, **kwargs):
#     pass