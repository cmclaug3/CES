from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from .forms import SetPinForm

from accounts.models import Employee
from time_sheet.models import Job

from .forms import AddTimesheetForm, EmployeeWorkForm





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



class SingleJobView(View):
    def get(self, request, job_id):
        context = {
            'job': Job.objects.get(id=job_id)
        }

    # THIS DOESNT WORK??
        # if request.POST.get('add_a_timesheet'):
        #     return redirect((reverse('add_timesheet', kwargs={'job_id': Job.objects.get(id=job_id)})))

        return render(request, 'single_job.html', context)



# class AddWorkDayView(View):
#     def get(self, request, job_id):
#         data = {
#             'address': Job.objects.get(id=job_id).address
#         }
#         job = Job.objects.get(id=job_id)
#         context = {
#             'form': WorkDayForm(initial=data),
#             'job': job,
#             'job_workdays': WorkDay.objects.filter(job__id=job_id)
#         }
#         return render(request, 'add_workday.html', context)
#
#     def post(self, request, job_id):
#         form = WorkDayForm(request.POST)
#         job = Job.objects.get(id=job_id)
#         if not form.is_valid():
#             context = {
#                 'form': form
#             }
#             return render(request, 'add_workday.html', context)
#
#         workday = form.save(commit=False)
#         workday.job = job
#         workday.save()
#
#         return redirect(reverse('add_timesheet', kwargs={'workday_id': workday.id}))







class AddTimeSheetView(View):
    def get(self, request, job_id):
        job = Job.objects.get(id=job_id)
        data = {
            'job': job,
            'address': job.address
        }
        context = {
            'form': AddTimesheetForm(initial=data),
            'job': job,

        }
        return render(request, 'add_timesheet.html', context)

    def post(self, request, job_id):
        job = Job.objects.get(id=job_id)
        form = AddTimesheetForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'add_timesheet.html', context)

        timesheet = form.save(commit=False)
        timesheet.save()
        return redirect(reverse('add_employee_work', kwargs={'timesheet_id': timesheet.id}))





class AddEmployeeWork(View):
    def get(self, request, timesheet_id):
        form = EmployeeWorkForm()
        context = {
            'form': form
        }
        return render(request, 'add_employee_work.html', context)





