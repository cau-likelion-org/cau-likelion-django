from django.urls import path
from .views import *

urlpatterns = [
    path('/secret', AttendanceAdminView.as_view()),
    path('/check', UserAttendanceView.as_view()),
    path('', AttendanceView.as_view()),
]
