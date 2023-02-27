# 데이터 처리
from .models import Project, ProjectImage
from .serializers import ProjectImageSerializer, ProjectSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets

@method_decorator(csrf_exempt, name="dispatch")
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer