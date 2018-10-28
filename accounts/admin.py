from django.contrib import admin
from .models import Employee, PreSetAuthorizedUser
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(PreSetAuthorizedUser)

# Register your models here.
