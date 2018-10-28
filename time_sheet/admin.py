from django.contrib import admin
from .models import Job, WorkDay, TimeSheet, Receipt, EmployeeWork


admin.site.register(Job)
admin.site.register(WorkDay)
admin.site.register(TimeSheet)
admin.site.register(Receipt)
admin.site.register(EmployeeWork)


