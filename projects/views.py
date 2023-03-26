from .models import Project, ProjectImage
from .serializers import ProjectSerializer
from accounts.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3

class ProjectList(APIView):
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

        return Response(data={
            "message" : "success",
            "data" : {
                "9" : nine,
                "10" : ten,
                "11" : eleven,
                # "2024" : four,
            }
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        title = request.POST['title']
        subtitle = request.POST['subtitle']
        dev_stack = request.POST['dev_stack']
        thumbnail = request.FILES['thumbnail']
        generation = request.POST['generation']
        team_name = request.POST['team_name']
        team_member = request.POST['team_member']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        description = request.POST['description']
        link = request.POST['link']
        category = request.POST['category']
        login_email = request.POST['login_email']

        memberid = User.objects.get(
            email = login_email
        )

        thumbnail_url = f"projects/{title}/thumbnail" # DB에 저장될 썸네일 이미지 url 설정
        self.s3_client.upload_fileobj(
            thumbnail,
            "realchunghaha",
            thumbnail_url,
            ExtraArgs={
                    "ContentType": thumbnail.content_type
                }
        )
        project_post = Project.objects.create(
            title = title,
            subtitle = subtitle,
            dev_stack = dev_stack,
            thumbnail = "https://https://d2ojsutiiokydr.cloudfront.net/" + thumbnail_url,
            version = generation,
            team_name = team_name,
            team_member = team_member,
            start_date = start_date,
            end_date = end_date,
            description = description,
            link = link,
            category = category,
            member_id = memberid
        )
        project_post.save()

        images = request.FILES.getlist('images')
        cnt = 1
        for image in images:
            image_url = f"projects/{title}/image{cnt}"
            self.s3_client.upload_fileobj(
                image,
                "realchunghaha",
                image_url,
                ExtraArgs={
                        "ContentType": image.content_type
                    }
            )
            image = ProjectImage.objects.create(
                project_id = project_post,
                image = "https://d2ojsutiiokydr.cloudfront.net/" + image_url
            )
            cnt = cnt + 1

        return Response(data={
        "message" : "success",
        "data" : {
            "title" : title
        }
    }, status=status.HTTP_200_OK)


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
