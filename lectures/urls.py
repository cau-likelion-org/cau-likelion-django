from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path

urlpatterns = [
    path('', views.SessionList.as_view()),
    path('/<int:pk>/', views.SessionDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
