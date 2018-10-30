from django import forms
from django.forms import ModelForm

from .models import TimeSheet, WorkDay



class SetPinForm(forms.Form):
    pin1 = forms.CharField(max_length=8)
    pin2 = forms.CharField(max_length=8)
    agree_to_use_as_signature = forms.BooleanField()



class AddTimesheetForm(ModelForm):
    class Meta:
        model = TimeSheet
        fields = '__all__'



class WorkDayForm(ModelForm):
    class Meta:
        model = WorkDay
        fields = '__all__'



# location
# completed
# timesheet