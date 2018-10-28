from django import forms



class SetPinForm(forms.Form):
    pin1 = forms.CharField(max_length=8)
    pin2 = forms.CharField(max_length=8)




