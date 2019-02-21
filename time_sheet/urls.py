from django.urls import path
from .views import (SetPinView, JobsView, SingleJobView, AddTimeSheetView, AddWorkDayView, SingleWorkDay,
                    HelpView, AddEmployeeWork, SignEmployeeWork, CreateJob, WorkDayData, SingleWorkdayData,
                    EmployeeData, SingleEmployeeData, delete_timesheet_view, delete_that_timesheet,
                    delete_workday_view, delete_that_workday)



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

    path('workday_data', WorkDayData.as_view(), name='workday_data'),
    path('single_workday_data/<int:workday_id>', SingleWorkdayData.as_view(), name='single_workday_data'),

    path('employee_data', EmployeeData.as_view(), name='employee_data'),
    path('single_employee_data/<int:employee_id>', SingleEmployeeData.as_view(), name='single_employee_data'),

    path('delete_timesheet_view/<int:timesheet_id>', delete_timesheet_view, name='delete_timesheet_view'),
    path('delete_that_timesheet/<int:timesheet_id>', delete_that_timesheet, name='delete_that_timesheet'),

    path('delete_workday_view/<int:workday_id>', delete_workday_view, name='delete_workday_view'),
    path('delete_that_workday/<int:workday_id>', delete_that_workday, name='delete_that_workday'),

    path('help', HelpView.as_view(), name='help'),

]