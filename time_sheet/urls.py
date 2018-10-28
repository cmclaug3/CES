from django.urls import path
from .views import SetPinView



urlpatterns = [
    path('set_pin', SetPinView.as_view(), name='set_pin'),

]