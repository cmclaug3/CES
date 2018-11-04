from django import forms
from django.forms import ModelForm

from .models import TimeSheet, EmployeeWork



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



class EmployeeWorkForm(ModelForm):
    class Meta:
        model = EmployeeWork
        fields = '__all__'

