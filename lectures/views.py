# 데이터 처리
from .models import Session, SessionImage
from accounts.models import User
from .serializers import SessionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3

# 세션의 목록을 보여주는 역할
class SessionList(APIView):
    s3_client = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        )
    # 세션 리스트를 보여줄 때
    def get(self,request):

        session_list = Session.objects.values()
    
        pm = []
        design = []
        front = []
        back = []
        etc = [] # 기타

        for session in session_list:
            if session['track'] == 0:
                pm.append({
                "id" : session['session_id'],
                "title" : session['title'],
                "degree" : session['degree'],
                "thumbnail" : session['thumbnail']
                })
            elif session['track'] == 1:
                design.append({
                "id" : session['session_id'],
                "title" : session['title'],
                "degree" : session['degree'],
                "thumbnail" : session['thumbnail']
                })
            elif session['track'] == 2:
                front.append({
                "id" : session['session_id'],
                "title" : session['title'],
                "degree" : session['degree'],
                "thumbnail" : session['thumbnail']
                })
            elif session['track'] == 3:
                back.append({
                "id" : session['session_id'],
                "title" : session['title'],
                "degree" : session['degree'],
                "thumbnail" : session['thumbnail']
                })
            elif session['track'] == 4:
                etc.append({
                "id" : session['session_id'],
                "title" : session['title'],
                "degree" : session['degree'],
                "thumbnail" : session['thumbnail']
                })


        return Response(data={
            "message" : "success",
            "data" : {
                "0" : pm,
                "1" : design,
                "2" : front,
                "3" : back,
                "4" : etc,
            }
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        title = request.POST['title']
        track = request.POST['track']
        thumbnail = request.FILES['thumbnail']
        presenter = request.POST['presenter']
        date = request.POST['date']
        description = request.POST['description']
        topic = request.POST['topic']
        reference = request.POST['reference']
        degree = request.POST['degree']
        login_email = request.POST['login_email']

        memberid = User.objects.get(
            email = login_email
        )

        thumbnail_url = f"sessions/{title}/thumbnail" # DB에 저장될 썸네일 이미지 url 설정
        self.s3_client.upload_fileobj(
            thumbnail,
            "realchunghaha",
            thumbnail_url,
            ExtraArgs={
                    "ContentType": thumbnail.content_type
                }
        )
        session_post = Session.objects.create(
            title = title,
            thumbnail = "https://d2ojsutiiokydr.cloudfront.net/" + thumbnail_url,
            date = date,
            description = description,
            track = track,
            presenter = presenter,
            topic = topic,
            reference = reference,
            degree = degree,
            user_id = memberid
        )
        session_post.save()

        images = request.FILES.getlist('images')
        cnt = 1
        for image in images:
            image_url = f"sessions/{title}/image{cnt}"
            self.s3_client.upload_fileobj(
                image,
                "realchunghaha",
                image_url,
                ExtraArgs={
                        "ContentType": image.content_type
                    }
            )
            image = SessionImage.objects.create(
                session = session_post,
                image = "https://d2ojsutiiokydr.cloudfront.net/" + image_url
            )
            cnt = cnt + 1

        return Response(data={
        "message" : "success",
        "data" : {
            "title" : title
        }
    }, status=status.HTTP_200_OK)

# Session의 detail을 보여주는 역할
class SessionDetail(APIView):
        # Session 객체 가져오기
    def get_object(self, pk):
        try:
            return Session.objects.get(pk=pk)
        except Session.DoesNotExist:
            raise Http404
    
    # Session의 detail 보기
    def get(self, request, pk, format=None):
        session = self.get_object(pk)
        session_images = session.image.all() # 역참조 기능 이용. 
        images = []
        for img in session_images:
            images.append(str(img.image))
            
        return Response(data={
            "message" : "success",
            "data" : {
                "title" : session.title,
                "image" : images,
                "track" : session.track,
                "presenter" : session.presenter,
                "topic" : session.topic,
                "description" : session.description,
                "date" : session.date,
                "reference" : session.reference,
                "degree" : session.degree
            }
        }, status=status.HTTP_200_OK)  
        
        # session 수정하기
    def put(self, request, pk, format=None):
        gallery = self.get_object(pk)
        serializer = SessionSerializer(gallery, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Project 삭제하기
    def delete(self, request, pk, format=None):
        session = self.get_object(pk)
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)