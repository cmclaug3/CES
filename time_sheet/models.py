from django.db import models
from accounts.models import Employee




EMPLOYEEWORK_LUNCH_CHOICES = (
    ('half-hour', 'Half Hour'),
    ('hour', 'Hour'),
    ('none', 'None'),
)

class EmployeeWork(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
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
    ('incomplete', 'Incomplete'),
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('complete', 'Complete'),
)

class TimeSheet(models.Model):
    date = models.DateField()
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    supervisor_sig = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=TIMESHEET_STATUS_CHOICES)
    employee_works = models.ManyToManyField(EmployeeWork)
    receipts = models.ManyToManyField(Receipt)

    def __str__(self):
        return self.date




class WorkDay(models.Model):
    location = models.CharField(max_length=150)
    completed = models.BooleanField()
    time_sheet = models.ForeignKey(TimeSheet, on_delete=models.CASCADE)

    def __str__(self):
        return self.date



JOB_TYPE_CHOICES = (
    ('single', 'Single'),
    ('ongoing', 'Ongoing'),
)

class Job(models.Model):
    name = models.CharField(max_length=100)
    job_num = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    completed = models.BooleanField()
    workdays = models.ManyToManyField(WorkDay)

    def __str__(self):
        return '{} {}'.format(self.name, self.job_num)




















