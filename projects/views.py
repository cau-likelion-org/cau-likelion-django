# 데이터 처리
from .models import Project, ProjectImage
from .serializers import ProjectImageSerializer, ProjectSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets

@csrf_exempt
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer