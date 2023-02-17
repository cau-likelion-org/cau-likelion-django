from rest_framework.urlpatterns import format_suffix_patterns
from .views import SessionViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('', views.GalleryList.as_view()),
#     path('<int:pk>/', views.GalleryDetail.as_view()),
# ]

router = DefaultRouter()
router.register('session', SessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]