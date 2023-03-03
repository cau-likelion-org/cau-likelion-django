from django.urls import path
from .views import *

urlpatterns = [
    path('google/callback/', google_callback, name='google_callback'),
    path('authentication/', cau_authentication, name='school_email_authentiation'),
    path('caumail/', CauMailView.as_view()),
    path('signup/', SignUpView.as_view()),
]
