from django.urls import path
from .views import *

urlpatterns = [
    path('attendance/admin', AttendanceAdminView.as_view()),
    path('attendance/', AttendanceView.as_view()),
    path('attendance/modify', AttendanceModifyView.as_view())
]
