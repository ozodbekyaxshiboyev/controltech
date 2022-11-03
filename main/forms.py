from django import forms
from django.forms import TextInput
from .models import (
    Report, ReportItem,
    Task, TaskResult, Chat,Dayplan, Reachment)



class DayplanForm(forms.ModelForm):
    class Meta:
        model=Dayplan
        fields = ('text',)


class ReachmentForm(forms.ModelForm):
    class Meta:
        model=Reachment
        fields = ('text','image',)


class ReportForm(forms.ModelForm):
    class Meta:
        model=Report
        fields = ('book','from_lesson','to_lesson','count','comment')
        # widgets = {'book':"textInput form-control"}
        # widgets = {
        #     'comment': TextInput(attrs={'cols': 200, 'rows': 20}),
        # }

