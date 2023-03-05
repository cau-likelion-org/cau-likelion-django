from .models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from django.http import Http404

class ProjectList(APIView):
    # 프로젝트 리스트를 보여줄 때
    def get(self, request):
        project_list = Project.objects.values()

        nine = [] # 9기
        ten = [] # 10기
        eleven = [] # 11기 // 사이드프로젝트 이어받는 분들~ 이 다음부터 12기는 twelve 13기는 thirteen 하시면 됩니다.       

        for project in project_list:
            if project['version'] == 9:
                nine.append({
                    'id' : project['project_id'],
                    'title' : project['title'],
                    'dev_stack' : project['dev_stack'],
                    'description' : project['description'],
                    'category' : project['category'],
                    'thumbnail' : project['thumbnail'],
                })
            elif project['version'] == 10:
                ten.append({
                    'id' : project['project_id'],
                    'title' : project['title'],
                    'dev_stack' : project['dev_stack'],
                    'description' : project['description'],
                    'category' : project['category'],
                    'thumbnail' : project['thumbnail'],
                })
            elif project['version'] == 11:
                eleven.append({
                    'id' : project['project_id'],
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

class ProjectDetail(APIView):
    # Project 객체 가져오기
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    # Gallery의 detail 보기
    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        project_images = project.image.all()
        images = []
        for img in project_images:
            images.append(str(img.image))
            
        return Response(data={
            "message" : "success",
            "data" : {
                "id" : project.project_id,
                "title" : project.title,
                "dev_stack" : project.dev_stack,
                "subtitle" : project.subtitle,
                "thumbnail" : project.thumbnail,
                "generation" : project.version,
                "team_name" : project.team_name,
                "team_member" : project.team_member,
                "image" : images,
                "start_date" : project.start_date,
                "end_date" : project.end_date,
                "description" : project.description,
                "link" : project.link,
                "category" : project.category,
            }
        }, status=status.HTTP_200_OK)    

    # Project 수정하기
    def put(self, request, pk, format=None):
        gallery = self.get_object(pk)
        serializer = GallerySerializer(gallery, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Project 삭제하기
    def delete(self, request, pk, format=None):
        gallery = self.get_object(pk)
        gallery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer