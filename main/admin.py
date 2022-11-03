from django.contrib import admin
from .models import *

admin.site.register((Report,ReportItem,Task,TaskResult,Chat,Reachment,Dayplan))
