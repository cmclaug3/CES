from django import forms




class PreSetAuthorizedUserForm(forms.Form):
    first_name = forms.CharField(max_length=70)
    last_name = forms.CharField(max_length=70)
    email = forms.EmailField(max_length=255)
    code = forms.CharField(max_length=15)


class SetNewUserPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)