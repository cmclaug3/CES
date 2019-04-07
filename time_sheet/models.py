from django.db import models
from accounts.models import User, Employee

from datetime import datetime
from datetime import time
from datetime import timedelta
from django import forms









class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ('Single', 'Single'),
        ('Ongoing', 'Ongoing'),
        ('ER', 'ER'),
    )

    name = models.CharField(max_length=100)
    job_num = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=150, blank=True, null=True, help_text='* Only if Job always has same address') # can set this here if it is always the same, else set on WorkDay
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    created_date = models.DateField(auto_now_add=True, blank=True, null=True)
    notes = models.TextField(default='')

    # Does HASP have to eventually connect as a foreign key here?

    def __str__(self):
        return '{} {}'.format(self.name, self.format_job_num())

    def format_job_num(self):
        nums = list(self.job_num)
        nums.insert(2, '-')
        yes = ''.join(nums)
        return yes




class WorkDay(models.Model):

    WORKDAY_STATUS_CHOICES = (
        ('Incomplete', 'Incomplete'),
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Complete', 'Complete'),
    )

    date = models.DateField()
    address = models.CharField(max_length=150, help_text="**Change if address mobile", blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=WORKDAY_STATUS_CHOICES, default=WORKDAY_STATUS_CHOICES[0][0])

    # I want put the HASP here because this is where the flow will be, but structure wise it would be better
    # connected to the Job because there is only one HASP Job

    def __str__(self):
        return '{} {}'.format(self.job.name, self.date)











# class TimeSheetManager(models.Manager):
#     '''
#     THIS DOESNT WORK HOW I WANT IT TO....
#     '''
#
#     def get_weeks_timesheets(self, certain_date=datetime.today()):
#
#         # I dont know if i want this like this
#         # this pay period logic needs to be elsewhere
#
#         today_num = datetime.today().weekday()
#         if certain_date != datetime.today():
#             today_num = certain_date.weekday()
#             print('break point')
#
#         # Get monday of the given week
#         starting_monday = certain_date - timedelta(days=today_num)
#         week = []
#
#         # Create list of 7 day week starting for that Monday
#         for week_days in range(7):
#             week.append(starting_monday)
#             starting_monday += timedelta(days=1)
#
#         this_weeks_timesheets = []
#
#         for day in week:
#             day_timesheets = TimeSheet.objects.filter(date=day)
#             if day_timesheets.count() == 0:
#                 continue
#             this_weeks_timesheets.append(day_timesheets)
#             return this_weeks_timesheets






class TimeSheet(models.Model):
    work_day = models.ForeignKey(WorkDay, on_delete=models.CASCADE, null=True, blank=True)
    # creator_signature = models.CharField(max_length=50, blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return 'Timesheet for {} on {}'.format(self.work_day.job.name, self.work_day.date)

    def get_employee_works(self):
        return EmployeeWork.objects.filter(time_sheet=self)

    objects = models.Manager()
    # this_week = TimeSheetManager()









class EmployeeWork(models.Model):
    '''
    Needs to only take in half hour choices of datetime
    '''

    EMPLOYEEWORK_LUNCH_CHOICES = (
        ('half-hour', 'Half Hour'),
        ('hour', 'Hour'),
        ('none', 'None'),
    )

    TIME_CHOICES = (
        (time(0, 0), '00:00'), (time(0, 30), '00:30'), (time(1, 0), '01:00'), (time(1, 30), '01:30'), (time(2, 0), '02:00'), (time(2, 30), '02:30'),
        (time(3, 0), '03:00'), (time(3, 30), '03:30'), (time(4, 0), '04:00'), (time(4, 30), '04:30'), (time(5, 0), '05:00'), (time(5, 30), '05:30'),
        (time(6, 0), '06:00'), (time(6, 30), '06:30'), (time(7, 0), '07:00'), (time(7, 30), '07:30'), (time(8, 0), '08:00'), (time(8, 30), '08:30'),
        (time(9, 0), '09:00'), (time(9, 30), '09:00'), (time(10, 0), '10:00'), (time(10, 30), '10:30'), (time(11, 0), '11:00'), (time(11, 30), '11:30'),
        (time(12, 0), '12:00'), (time(12, 30), '12:30'), (time(13, 0), '13:00'), (time(13, 30), '13:30'), (time(14, 0), '14:00'), (time(14, 30), '14:30'),
        (time(15, 0), '15:00'), (time(15, 30), '15:30'), (time(16, 0), '16:00'), (time(16, 30), '16:30'), (time(17, 0), '17:00'), (time(17, 30), '17:30'),
        (time(18, 0), '18:00'), (time(18, 30), '18:30'), (time(19, 0), '19:00'), (time(19, 30), '19:30'), (time(20, 0), '20:00'), (time(20, 30), '20:30'),
        (time(21, 0), '21:00'), (time(21, 30), '21:00'), (time(22, 0), '22:00'), (time(22, 30), '22:30'), (time(23, 0), '23:00'), (time(23, 30), '23:30'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    time_sheet = models.ForeignKey(TimeSheet, blank=True, null=True, on_delete=models.CASCADE)
    start_time = models.TimeField(choices=TIME_CHOICES)
    end_time = models.TimeField(choices=TIME_CHOICES)
    lunch = models.CharField(max_length=20, choices=EMPLOYEEWORK_LUNCH_CHOICES)
    injured = models.BooleanField(default=False)
    comment = models.CharField(max_length=300, blank=True, null=True)
    signature = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return '{} {} {}'.format(self.employee.get_short_name(), self.time_sheet.work_day.date, self.time_sheet.work_day.job)

    def total_hours(self):
        one = timedelta(hours=self.start_time.hour, minutes=self.start_time.minute)
        two = timedelta(hours=self.end_time.hour, minutes=self.end_time.minute)
        answer = two - one
        if self.lunch == 'half-hour':
            answer -= timedelta(minutes=30)
        elif self.lunch == 'hour':
            answer -= timedelta(hours=1)

        seconds = answer.seconds
        value = seconds/3600
        return value








class Receipt(models.Model):
    driver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    time_sheet = models.ForeignKey(TimeSheet, blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField()

    def __str__(self):
        return 'Image -> {} work_day'.format(self.work_day)




class Hasp(models.Model):
    pass








































