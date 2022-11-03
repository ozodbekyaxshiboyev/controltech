from django import forms
from .models import (
    Report, ReportItem,
    Task, TaskResult, Chat)





class ReportForm(forms.ModelForm):
    class Meta:
        model=Report
        fields = ('book','from_lesson','to_lesson','count','comment')
        # widgets = {'book':"textinput textInput form-control"}

