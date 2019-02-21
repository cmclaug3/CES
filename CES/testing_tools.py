from time_sheet.models import TimeSheet, WorkDay, EmployeeWork, Job
from accounts.models import Employee, User
import random
from datetime import date, time, timedelta




def clear_all_but_jobs_employees():
    TimeSheet.objects.all().delete()
    WorkDay.objects.all().delete()
    EmployeeWork.objects.all().delete()
    print('just deleted all timesheets, workdays, and employeeworks')



def data_injection(start_date, end_date):
    '''

    inject variable amount of fake data into system
        do this with 12 employees

        get all days between start and end date in a list
        create work days with random amount of employees with at random jobs

    '''

    all_jobs = Job.objects.all()
    all_employees = Employee.objects.all()
    all_days = []
    group_amounts = [1, 2, 3, 4]

    while start_date < end_date:
        all_days.append(start_date)
        start_date += timedelta(days=1)

    for day in all_days:
        pass