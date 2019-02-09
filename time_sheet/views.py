from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from .forms import SetPinForm
from datetime import datetime

from django.forms import formset_factory, modelformset_factory

from accounts.models import Employee
from time_sheet.models import Job, TimeSheet, EmployeeWork, WorkDay

from .forms import AddTimesheetForm, EmployeeWorkFormset, SignTimeSheetForm, CreateJobForm, WorkDayForm





class HelpView(View):
    def get(self, request):
        return render(request, 'help.html')



class SetPinView(View):
    def get(self, request):
        context = {
            'form': SetPinForm()
        }
        return render(request, 'set_pin_form.html', context)

    def post(self, request):
        form = SetPinForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'set_new_user_password_form.html', context)

        pin1 = form.cleaned_data['pin1']
        pin2 = form.cleaned_data['pin2']
        agree = form.cleaned_data['agree_to_use_as_signature']

        employee = Employee.objects.get(user=request.user)

        if agree == False:
            messages.add_message(request, messages.ERROR, 'You must check box to agree to use pin as signature to proceed')
            return redirect(reverse('set_pin'))

        if pin1.isdigit() and pin2.isdigit() == True:

            if len(pin1) and len(pin2) >= 6:

                if pin1 == pin2:

                    # SUCCESS
                    employee.pin = pin1
                    employee.save()
                    messages.add_message(request, messages.SUCCESS, 'You have successfully Changed/Added your pin')
                    return redirect(reverse('home'))

                else:
                    messages.add_message(request, messages.ERROR, 'Pins do not match try again')
                    return redirect(reverse('set_pin'))

            else:
                messages.add_message(request, messages.ERROR, 'Pins must be atleast 6 characters long try again')
                return redirect(reverse('set_pin'))

        else:
            messages.add_message(request, messages.ERROR, 'Pins must be all numerical characters try again')
            return redirect(reverse('set_pin'))





class JobsView(View):
    def get(self, request):
        context = {
            'jobs': Job.objects.all()
        }
        return render(request, 'jobs.html', context)






class CreateJob(View):
    def get(self, request):
        form = CreateJobForm()
        context = {
            'form': form
        }
        return render(request, 'create_job.html', context)
    def post(self, request):
        form = CreateJobForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'create_job.html', context)
        new_job = form.save(commit=False)
        new_job.created_by = request.user.employee
        new_job.save()
        return redirect(reverse('home'))








class SingleJobView(View):
    def get(self, request, job_id):
        context = {
            'job': Job.objects.get(id=job_id)
        }

    # THIS DOESNT WORK??
        # if request.POST.get('add_a_timesheet'):
        #     return redirect((reverse('add_timesheet', kwargs={'job_id': Job.objects.get(id=job_id)})))

        return render(request, 'single_job.html', context)



class AddWorkDayView(View):
    def get(self, request, job_id):
        data = {
            'address': Job.objects.get(id=job_id).address,
            # 'job': Job.objects.get(id=job_id)
        }
        job = Job.objects.get(id=job_id)
        employee = request.user.employee

        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        date = datetime(year, month, day).date()
        context = {
            'form': WorkDayForm(initial=data),
            'job': job,
            'employee': employee,
            'date': date,

            'job_workdays': WorkDay.objects.filter(job__id=job_id)
        }
        return render(request, 'add_workday.html', context)

    def post(self, request, job_id):
        form = WorkDayForm(request.POST)
        job = Job.objects.get(id=job_id)
        employee = request.user.employee

        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        date = datetime(year, month, day)

        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'add_workday.html', context)

        workday = form.save(commit=False)
        workday.job = job
        workday.created_by = employee
        workday.date = date
        workday.save()

        return redirect(reverse('single_workday', kwargs={'workday_id': workday.id}))




class SingleWorkDay(View):
    def get(self, request, workday_id):
        workday = WorkDay.objects.get(id=workday_id)
        timesheets = TimeSheet.objects.filter(work_day=workday)
        context = {
            'workday': workday,
            'timesheets': timesheets,
        }
        return render(request, 'single_workday.html', context)







class AddTimeSheetView(View):
    '''
    The way that these get added, i dont need a page form becuase it already knows all the fields to create
        it is linked to a WorkDay, and has a Employee Signature that makes it completed

        SO WHAT THIS DOES...
            automatically creates a timesheet object with a FK to the WorkDay it was added on
    '''
    def get(self, request, workday_id):
        # work_day = WorkDay.objects.get(id=workday_id)
        # data = {
        #     'workday': work_day,
        #     'address': work_day.address
        # }
        # context = {
        #     'form': AddTimesheetForm(),
        #     'work_day': work_day,
        #
        # }
        # return render(request, 'add_timesheet.html', context)

        workday = WorkDay.objects.get(id=workday_id)
        timesheet = TimeSheet.objects.create(work_day=workday)
        return redirect(reverse('add_employee_work', kwargs={'timesheet_id': timesheet.id}))


    # def post(self, request, job_id):
    #     job = Job.objects.get(id=job_id)
    #     form = AddTimesheetForm(request.POST)
    #     if not form.is_valid():
    #         context = {
    #             'form': form
    #         }
    #         return render(request, 'add_timesheet.html', context)
    #
    #     timesheet = form.save(commit=False)
    #     # timesheet.job = job
    #     timesheet.save()
    #     return redirect(reverse('add_employee_work', kwargs={'timesheet_id': timesheet.id}))





class AddEmployeeWork(View):
    def get(self, request, timesheet_id):
        form_set = EmployeeWorkFormset(queryset=EmployeeWork.objects.none())
        timesheet = TimeSheet.objects.get(id=timesheet_id)

        context = {
            'form_set': form_set,
            'timesheet': timesheet,
        }

        # if request.GET.get('more_employees'):
        #     context['more_employees'] = True
        #
        # employees = request.GET.get('number_employees')

        return render(request, 'add_employee_work.html', context)

    def post(self, request, timesheet_id):
        form_set = EmployeeWorkFormset(request.POST)
        timesheet = TimeSheet.objects.get(id=timesheet_id)
        for form in form_set:
            if not form.is_valid():
                context = {
                    'form_set': EmployeeWorkFormset(queryset=EmployeeWork.objects.none()),
                    'timesheet': timesheet,
                }
                print('something is wrong, form not valid')
                return render(request, 'add_employee_work.html', context)
            employee_work = form.save(commit=False)
            employee_work.time_sheet = timesheet
            employee_work.save()
        messages.add_message(request, messages.SUCCESS, 'You have added an employee work')
        return redirect(reverse('home'))





class SignEmployeeWork(View):
    def get(self, request, employee_work_id):
        employee_work = EmployeeWork.objects.get(id=employee_work_id)
        timesheet = employee_work.time_sheet
        form = SignTimeSheetForm()

        context = {
            'employee_work': employee_work,
            'timesheet': timesheet,
            'form': form,
        }

        return render(request, 'sign_employee_work.html', context)

    def post(self, request, employee_work_id):
        employee_work = EmployeeWork.objects.get(id=employee_work_id)
        timesheet = employee_work.time_sheet
        form = SignTimeSheetForm(request.POST)

        if not form.is_valid():
            context = {
                'employee_work': employee_work,
                'timesheet': timesheet,
                'form': form,
            }
            return render(request, 'sign_employee_work.html', context)

        pin = form.cleaned_data['pin']
        employee = Employee.objects.get(user=request.user)




        if pin == employee.pin:

            # somehow this is not going though even though it seems to work
            employee_work.signature = True

            messages.add_message(request, messages.SUCCESS, 'You have signed an employee work')
            return redirect(reverse('home'))

        else:
            context = {
                'employee_work': employee_work,
                'timesheet': timesheet,
                'form': form,
            }
            messages.add_message(request, messages.ERROR, 'Your pin was incorrect, try again')
            return render(request, 'sign_employee_work.html', context)

"""

THINGS TO DO

    figure out employee_work datetime format
    * get fixtures up
    home page (what will it show)
    form_set automation and submission thinking
    model methods
    
    model managers
    
    signals
    
    CSS/JAVASCRIPT
    
    



"""