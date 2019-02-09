from django.contrib import admin
from .models import Job, TimeSheet, Receipt, EmployeeWork, WorkDay


admin.site.register(Job)
admin.site.register(TimeSheet)
admin.site.register(Receipt)
admin.site.register(EmployeeWork)
admin.site.register(WorkDay)


