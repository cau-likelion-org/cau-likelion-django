from .models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from django.http import Http404

class GalleryList(APIView):
    # 프로젝트 리스트를 보여줄 때
    def get(self, request):
        project_list = Project.objects.values()

        nine = [] # 9기
        ten = [] # 10기
        eleven = [] # 11기 // 사이드프로젝트 이어받는 분들~ 이 다음부터 12기는 twelve 13기는 thirteen 하시면 됩니다.       

        for project in project_list:
            if project['version'] == '9':
                nine.append({
                    'id' : project['gallery_id'],
                    'title' : project['title'],
                    'dev_stack' : project['dev_stack'],
                    'description' : project['description'],
                    'category' : project['category'],
                    'thumbnail' : project['thumbnail'],
                })
            elif project['version'] == '10':
                ten.append({
                    'id' : project['gallery_id'],
                    'title' : project['title'],
                    'dev_stack' : project['dev_stack'],
                    'description' : project['description'],
                    'category' : project['category'],
                    'thumbnail' : project['thumbnail'],
                })
            elif project['version'] == '11':
                eleven.append({
                    'id' : project['gallery_id'],
                    'title' : project['title'],
                    'dev_stack' : project['dev_stack'],
                    'description' : project['description'],
                    'category' : project['category'],
                    'thumbnail' : project['thumbnail'],
                })


        return Response(data={
            "message" : "success",
            "data" : {
                "9" : nine,
                "10" : ten,
                "11" : eleven,
                # "2024" : four,
            }
        }, status=status.HTTP_200_OK)

# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer