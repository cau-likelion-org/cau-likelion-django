from django.urls import path
from .views import *

urlpatterns = [
    path('password/', attendance_list),
    path('attendance/', AttendanceView.as_view())
]
