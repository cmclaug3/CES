from django.db import models
from accounts.models import Employee

from datetime import datetime






JOB_TYPE_CHOICES = (
    ('Single', 'Single'),
    ('Ongoing', 'Ongoing'),
    ('ER', 'ER'),
)

class Job(models.Model):
    address = models.CharField(max_length=150) # ADDED
    name = models.CharField(max_length=100)
    job_num = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    completed = models.BooleanField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True, blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.job_num)




TIMESHEET_STATUS_CHOICES = (
    ('Incomplete', 'Incomplete'),
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Complete', 'Complete'),
)

class TimeSheet(models.Model):
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(default=datetime.now)
    address = models.CharField(max_length=150)
    supervisor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    supervisor_sig = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=TIMESHEET_STATUS_CHOICES, default=TIMESHEET_STATUS_CHOICES[0][0])

    def __str__(self):
        return self.date.strftime('%m/%d/%Y')





class Receipt(models.Model):
    driver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    time_sheet = models.ForeignKey(TimeSheet, blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField()

    def __str__(self):
        return 'Image -> {} work_day'.format(self.work_day)




EMPLOYEEWORK_LUNCH_CHOICES = (
    ('half-hour', 'Half Hour'),
    ('hour', 'Hour'),
    ('none', 'None'),
)

class EmployeeWork(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    time_sheet = models.ForeignKey(TimeSheet, blank=True, null=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    lunch = models.CharField(max_length=20, choices=EMPLOYEEWORK_LUNCH_CHOICES)
    injured = models.BooleanField()
    comment = models.CharField(max_length=300)
    signature = models.CharField(max_length=50)

    def __str__(self):
        return self.employee.user.get_full_name()








































