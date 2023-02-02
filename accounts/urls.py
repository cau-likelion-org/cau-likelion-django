from django.urls import path
from .views import *

urlpatterns = [
    path('google/login', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    path('authentication/test/', cau_authentication, name='school_email_authentiation')
]
