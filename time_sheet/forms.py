from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.forms import BaseFormSet
from django.forms.models import BaseInlineFormSet

from .models import TimeSheet, EmployeeWork, Job, WorkDay
from datetime import datetime



class SetPinForm(forms.Form):
    pin1 = forms.CharField(max_length=8)
    pin2 = forms.CharField(max_length=8)
    agree_to_use_as_signature = forms.BooleanField()



class DateInput(forms.DateInput):
    input_type = 'date'

class AddTimesheetForm(ModelForm):
    class Meta:
        model = TimeSheet
        fields = ['work_day']
        widgets = {
            'date': DateInput()
        }

class WorkDayForm(ModelForm):
    class Meta:
        model = WorkDay
        fields = ['address']



# class EmployeeDateInput(forms.TimeInput):








class TimeInput(forms.TimeInput):
    input_type = 'time'


class EmployeeWorkForm(ModelForm):
    # start_time = forms.DateTimeField(input_formats=['%H:%M'])
    # end_time = forms.DateTimeField(input_formats=['%H:%M'])
    class Meta:
        model = EmployeeWork
        fields = ['employee', 'start_time', 'end_time', 'lunch', 'injured', 'comment']
        # widgets = {
        #     'start_time': TimeInput(format='%H:%M'),
        #     'end_time': TimeInput(format='%H:%M')
        # }





EmployeeWorkFormset = inlineformset_factory(TimeSheet, EmployeeWork, exclude=(), extra=2, can_delete=True)








class SignTimeSheetForm(forms.Form):
    pin = forms.CharField(max_length=8, help_text="Enter Pin")



class CreateJobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'job_num', 'address', 'type', 'notes']



