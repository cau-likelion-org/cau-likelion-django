from django.urls import path
from .views import *

urlpatterns = [
    path('', ProfileView.as_view()),
]
