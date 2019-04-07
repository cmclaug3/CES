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
        timesheet.save()
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






# EmployeeWorkFormset = inlineformset_factory(TimeSheet, EmployeeWork, exclude=(), extra=2, can_delete=True)

class AddEmployeeWork(View):
    def get(self, request, timesheet_id):
        timesheet = TimeSheet.objects.get(id=timesheet_id)
        initial_employee_works = EmployeeWork.objects.filter(time_sheet=timesheet)

        if initial_employee_works.count() > 0:
            form_set = EmployeeWorkFormset(instance=timesheet)
        else:
            form_set = EmployeeWorkFormset()

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
        timesheet = TimeSheet.objects.get(id=timesheet_id)
        initial_employee_works = EmployeeWork.objects.filter(time_sheet=timesheet)
        workday = timesheet.work_day

        form_set = EmployeeWorkFormset(request.POST)


        # for del_form in form_set.deleted_forms:
        #     del_form.delete()

        print('are there any forms marked for deletion? {}'.format(form_set.deleted_forms))

        for form in form_set:
            if not form.is_valid():

                import ipdb
                ipdb.set_trace()

                print('some form is not valid')
                if initial_employee_works.count() > 0:
                    form_set = EmployeeWorkFormset(instance=timesheet)
                else:
                    form_set = EmployeeWorkFormset()

                context = {
                    'form_set':form_set,
                    'timesheet': timesheet,
                }
                return render(request, 'add_employee_work.html', context)

            # if form.cleaned_values....

            employee_work = form.save(commit=False)
            employee_work.time_sheet = timesheet ### I DONT THINK I NEED THIS?? DO I??
            employee_work.save()

        print(len(form_set.deleted_forms))
        for obj in form_set.deleted_forms:
            obj.delete()
        print(len(form_set.deleted_forms))

        messages.add_message(request, messages.SUCCESS, 'You have added an employee work(s)')
        return redirect(reverse('single_workday', kwargs={'workday_id': workday.id}))



'''

PROBLEMS

    every time I open (what i think is) an editable timesheet, it pre populates all fields with the correct
    information (missing the employee) but saves all the employeeworks as new objects (not the same ones edited)
    
    get EmployeeWorkFormset (inline formset) working properly
        adding and deleting employeework rows from timesheet dynamically

    
    how exactly to model admininstrator interface
    
    
    
    
    
    
    
    dont worry about so much dynamically driven stuff with timesheets right now...
        use buttons as function views that can delete one empWork (based off form.initial.id) or to delete whole timesheet
    
    use the dam IPDB it is a freaking awesome tool!
    
    
    
    
    
    https://docs.djangoproject.com/en/2.1/ref/forms/validation/

if form.cleaned_values['DELETE_FIELD']:
    timesheet = GET TIMESHEET
    timesheet.delete()
    
    
`import ipdb; ipdb.set_trace()`
https://medium.com/@srijan.pydev_21998/complete-guide-to-deploy-django-applications-on-aws-ubuntu-16-04-instance-with-uwsgi-and-nginx-b9929da7b716

<a href="{% url 'NAMESPACE' %}" class="btn">DELETE</a>
    

'''




def delete_timesheet_view(request, timesheet_id):
    timesheet = TimeSheet.objects.get(id=timesheet_id)
    emp_works = EmployeeWork.objects.filter(time_sheet=timesheet)
    context = {
        'timesheet': timesheet,
        'emp_works': emp_works,
    }
    return render(request, 'delete_timesheet_view.html', context)


def delete_that_timesheet(request, timesheet_id):
    timesheet = TimeSheet.objects.get(id=timesheet_id)
    emp_works = EmployeeWork.objects.filter(time_sheet=timesheet)
    workday = timesheet.work_day

    for emp_work in emp_works:
        emp_work.delete()
    timesheet.delete()

    return redirect(reverse('single_workday', kwargs={'workday_id': workday.id}))




def delete_workday_view(request, workday_id):
    workday = WorkDay.objects.get(id=workday_id)
    context = {
        'workday': workday,
    }
    return render(request, 'delete_workday_view.html', context)


def delete_that_workday(request, workday_id):
    workday = WorkDay.objects.get(id=workday_id)
    workday.delete()
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

            employee_work.signature = True
            employee_work.save()
            print(employee_work.signature)

            messages.add_message(request, messages.SUCCESS, 'You have signed a time sheet')
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
    
    
    jobs.html
    should show just name and number, flowing down from columns dictating type
    



"""

class WorkDayData(View):
    def get(self, request):
        context = {
            'workdays': WorkDay.objects.all().order_by('-date'),
        }
        return render(request, 'workday_data.html', context)



class SingleWorkdayData(View):
    def get(self, request, workday_id):
        workday = WorkDay.objects.get(id=workday_id)
        timesheets = TimeSheet.objects.filter(work_day=workday)

        context = {
            'workday': workday,
            'timesheets': timesheets,
        }
        return render(request, 'single_workday_data.html', context)



class EmployeeData(View):
    def get(self, request):
        context = {
            'employees': Employee.objects.all(),
        }
        return render(request, 'employee_data.html', context)



class SingleEmployeeData(View):
    def get(self, request, employee_id):
        employee = Employee.objects.get(id=employee_id)
        context = {
            'employee': employee,
            'emp_workdays': WorkDay.objects.filter(created_by=employee),
            'emp_employee_works': EmployeeWork.objects.filter(employee=employee),
        }
        return render(request, 'single_employee_data.html', context)


'''
SEARCH/VIEW DATA
    Workday
        sort by day
            link displaying Job, date
    Job
        all workday for specific jobs (is it best to just do this in the already made template????)
        
    Employee
        all workdays, timesheets, receipts, pictures from specific employees
        need to include current hours, weekly hours, ect...
        
        
        
        
    How to encapsulate Pay Periods?
    problem with Jobs in Data because viewing jobs is the way to start a WorkDay for Employees/Admins
    write injection tests to test site with data...
        already in system: PreSetAuthorizedUser, Employee, Job (input more fake jobs manually)
        needs injection: WorkDay, TimeSheet, EmployeeWork
        
'''
