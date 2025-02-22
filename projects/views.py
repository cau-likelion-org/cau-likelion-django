from .models import Project, ProjectImage
from .serializers import ProjectSerializer
from accounts.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import Http404
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3

class ProjectList(APIView):
    parser_classes = [MultiPartParser, FormParser]
    s3_client = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        )
    # 프로젝트 리스트를 보여줄 때
    def get(self, request):
        project_list = Project.objects.values()

        nine = [] # 9기
        ten = [] # 10기
        eleven = [] # 11기 // 사이드프로젝트 이어받는 분들~ 이 다음부터 12기는 twelve 13기는 thirteen 하시면 됩니다.
        twelve = []     

        for project in project_list:
            if project['version'] == 9:
                nine.append({
                    'id' : project['project_id'],
                    'title' : project['title'],
                    'dev_stack' : project['dev_stack'],
                    'subtitle' : project['subtitle'],
                    'category' : project['category'],
                    'thumbnail' : project['thumbnail'],
                })
            elif project['version'] == 10:
                ten.append({
                    'id' : project['project_id'],
                    'title' : project['title'],
                    'dev_stack' : project['dev_stack'],
                    'subtitle' : project['subtitle'],
                    'category' : project['category'],
                    'thumbnail' : project['thumbnail'],
                })
            elif project['version'] == 11:
                eleven.append({
                    'id' : project['project_id'],
                    'title' : project['title'],
                    'dev_stack' : project['dev_stack'],
                    'subtitle' : project['subtitle'],
                    'category' : project['category'],
                    'thumbnail' : project['thumbnail'],
                })
            elif project['version'] == 12:
                twelve.append({
                    'id' : project['project_id'],
                    'title' : project['title'],
                    'dev_stack' : project['dev_stack'],
                    'subtitle' : project['subtitle'],
                    'category' : project['category'],
                    'thumbnail' : project['thumbnail'],
                })

        return Response(data={
            "message" : "success",
            "data" : {
                "9" : nine,
                "10" : ten,
                "11" : eleven,
                "12" : twelve
            }
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data["member_id"] = 1     
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Project create success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      


# Project의 detail을 보여주는 역할
class ProjectDetail(APIView):
    # Project 객체 가져오기
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    # Project의 detail 보기
    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        project_images = project.image.all()
        images = []
        for img in project_images:
            images.append(str(img.image))

        dev_stack = map(int,project.dev_stack.split(","))
        # thumb = 
        return Response(data={
            "message" : "success",
            "data" : {
                "id" : project.project_id,
                "title" : project.title,
                "dev_stack" : dev_stack,
                "subtitle" : project.subtitle,
                "generation" : project.version,
                "team_name" : project.team_name,
                "team_member" : project.team_member,
                "image" : images,
                "date" : project.start_date + " ~ " + project.end_date,
                "description" : project.description,
                "link" : project.link,
                "category" : project.category,
            }
        }, status=status.HTTP_200_OK)    

    # Project 수정하기
    def put(self, request, pk, format=None):
        gallery = self.get_object(pk)
        serializer = ProjectSerializer(gallery, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Project 삭제하기
    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
