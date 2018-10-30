from django.db import models
from accounts.models import Employee




EMPLOYEEWORK_LUNCH_CHOICES = (
    ('half-hour', 'Half Hour'),
    ('hour', 'Hour'),
    ('none', 'None'),
)

class EmployeeWork(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    lunch = models.CharField(max_length=20, choices=EMPLOYEEWORK_LUNCH_CHOICES)
    injured = models.BooleanField()
    comment = models.TextField()
    signature = models.CharField(max_length=50)

    def __str__(self):
        return self.employee.user.get_full_name()



class Receipt(models.Model):
    image = models.ImageField()



TIMESHEET_STATUS_CHOICES = (
    ('Incomplete', 'Incomplete'),
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Complete', 'Complete'),
)

class TimeSheet(models.Model):
    supervisor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    supervisor_sig = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=TIMESHEET_STATUS_CHOICES)
    employee_works = models.ManyToManyField(EmployeeWork, blank=True, null=True)
    receipts = models.ManyToManyField(Receipt, blank=True, null=True)

    def __str__(self):
        return self.date




class WorkDay(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=150)
    completed = models.BooleanField()
    time_sheet = models.ForeignKey(TimeSheet, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.date



JOB_TYPE_CHOICES = (
    ('Single', 'Single'),
    ('Ongoing', 'Ongoing'),
    ('ER', 'ER'),
)

class Job(models.Model):
    location = models.CharField(max_length=150) # ADDED
    name = models.CharField(max_length=100)
    job_num = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    completed = models.BooleanField()
    created_date = models.DateField(auto_now_add=True, blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    workdays = models.ManyToManyField(WorkDay, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.job_num)




















