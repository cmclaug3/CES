from django.urls import path
from .views import SetPinView, JobsView, SingleJobView, AddTimeSheetView, AddWorkDayView



urlpatterns = [
    path('set_pin', SetPinView.as_view(), name='set_pin'),
    path('jobs', JobsView.as_view(), name='jobs'),
    path('job/<int:job_id>', SingleJobView.as_view(), name='single_job'),
    path('add_timesheet/<int:job_id>', AddTimeSheetView.as_view(), name='add_timesheet'),
    path('add_workday/<int:job_id>', AddWorkDayView.as_view(), name='add_workday'),

]