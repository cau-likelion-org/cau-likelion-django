from rest_framework.urlpatterns import format_suffix_patterns

from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter


urlpatterns = [
     path('', SessionList.as_view()),
     path('/<int:id>', SessionDetail.as_view())
]
