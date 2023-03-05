from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('', views.GalleryList.as_view()),
#     path('<int:pk>/', views.GalleryDetail.as_view()),
# ]

# router = DefaultRouter()
# router.register('', ProjectViewSet)

urlpatterns = [
    path('', views.ProjectList.as_view()),
    path('/<int:pk>', views.ProjectDetail.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)
