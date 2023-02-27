# 데이터 처리
from .models import Session,SessionImage
from .serializers import SessionSerializer, SessionImageSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import viewsets
from django.http import Http404

@method_decorator(csrf_exempt, name="dispatch")
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer