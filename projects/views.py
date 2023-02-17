# 데이터 처리
from .models import Project, ProjectImage
from .serializers import ProjectImageSerializer, ProjectSerializer

from rest_framework import viewsets

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer