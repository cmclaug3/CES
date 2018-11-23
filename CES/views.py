from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import Employee, User
from time_sheet.models import EmployeeWork, TimeSheet



@login_required
def home(request):
    unsigned_employee_works = EmployeeWork.objects.filter(time_sheet__status='Incomplete')
    current_user_unsigned_employee_works = []
    for employee_work in unsigned_employee_works:
        if employee_work.employee == Employee.objects.get(user=request.user):
            if employee_work.signature == '':
                current_user_unsigned_employee_works.append(employee_work)

    context = {
        'user': request.user,
        'unsigned_employee_works': current_user_unsigned_employee_works
    }
    return render(request, 'home.html', context)