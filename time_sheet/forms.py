from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory

from .models import TimeSheet, EmployeeWork
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
        fields = ['job', 'date', 'address', 'supervisor']
        widgets = {
            'date': DateInput()
        }



# class EmployeeDateInput(forms.TimeInput):



class TimeInput(forms.TimeInput):
    input_type = 'time'


# class EmployeeWorkForm(ModelForm):
#     class Meta:
#         model = EmployeeWork
#         fields = ['employee', 'start_time', 'end_time', 'lunch', 'injured', 'comment']
#         widgets = {
#             'start_time': TimeInput(format='%H:%M'),
#             'end_time': TimeInput(format='%H:%M')
#         }

EmployeeWorkFormset = modelformset_factory(EmployeeWork, exclude=(), extra=3)