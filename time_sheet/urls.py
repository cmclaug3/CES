from django.urls import path
from .views import (SetPinView, JobsView, SingleJobView, AddTimeSheetView, AddWorkDayView, SingleWorkDay,
                    HelpView, AddEmployeeWork, SignEmployeeWork, CreateJob)



urlpatterns = [
    path('set_pin', SetPinView.as_view(), name='set_pin'),
    path('jobs', JobsView.as_view(), name='jobs'),
    path('job/<int:job_id>', SingleJobView.as_view(), name='single_job'),
    path('add_workday/<int:job_id>', AddWorkDayView.as_view(), name='add_workday'),
    path('single_workday/<int:workday_id>', SingleWorkDay.as_view(), name='single_workday'),
    path('add_timesheet/<int:workday_id>', AddTimeSheetView.as_view(), name='add_timesheet'),
    path('add_employee_work/<int:timesheet_id>', AddEmployeeWork.as_view(), name='add_employee_work'),
    path('sign_employee_work/<int:employee_work_id>', SignEmployeeWork.as_view(), name='sign_employee_work'),
    path('create_job', CreateJob.as_view(), name='create_job'),
    path('help', HelpView.as_view(), name='help'),

]