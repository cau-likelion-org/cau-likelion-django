from django.urls import path
from .views import *

urlpatterns = [
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    path('authentication/', cau_authentication, name='school_email_authentiation'),
    path('caumail/', CauMailView.as_view()),
    path('user/', UserView.as_view()),
]
