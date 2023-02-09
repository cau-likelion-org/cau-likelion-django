from django.urls import path
from .views import *

urlpatterns = [
    path('password/', create_password, name='create_password'),
    path('attendance/', AttendanceView.as_view())
]
