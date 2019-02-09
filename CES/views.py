from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import Employee, User
from time_sheet.models import EmployeeWork, TimeSheet, WorkDay



@login_required
def home(request):

    unsigned_employee_works = EmployeeWork.objects.filter(signature=False)
    current_user_unsigned_employee_works = []
    for employee_work in unsigned_employee_works:
        if employee_work.employee == Employee.objects.get(user=request.user):
            current_user_unsigned_employee_works.append(employee_work)


    unfinished_workdays = WorkDay.objects.filter(created_by=request.user.employee).filter(status='Incomplete')

    # If user is staff

    # this_weeks_timesheets = TimeSheet.this_week.get_weeks_timesheets()

    context = {
        'user': request.user,
        'unsigned_employee_works': current_user_unsigned_employee_works,
        'unfinished_workdays': unfinished_workdays,

        # 'this_weeks_timesheets': this_weeks_timesheets
    }
    return render(request, 'home.html', context)



class WeightCalculator(View):
    def get(self, request):
        context = {

        }
        return render(request, 'weight_calculator.html', context)

