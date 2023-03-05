# 데이터 처리
from .models import *
from .serializers import SessionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status

class PostListView(APIView):
    
    def get(self,request):
        session_list = Session.objects.all()
    
        pm = []
        design = []
        front = []
        back = []

        for session in session_list:
            session_json = {
                "id" : session.session_id,
                "title" : session.title,
                "degree" : session.degree,
                "thumbnail" : session.thumbnail
            }
            
            if session.track == 0:
                pm.append(session_json)
            elif session.track == 1:
                design.append(session_json)
            elif session.track == 2:
                front.append(session_json)
            else:
                back.append(session_json)


        return Response(data={
            "message" : "success",
            "data" : {
                "0" : pm,
                "1" : design,
                "2" : front,
                "3" : back
            }
        }, status=status.HTTP_200_OK)


class PostView(APIView):
    def get(self, request, id):
        
        session = Session.objects.get(session_id=id)
        
        image_list = []
        
        session_images = SessionImage.objects.filter(session=session)
        
        for session_image in session_images:
            image_url = session_image.image
            image_list.append(image_url)
        
        if session.track == 0:
            track = "기획"
        elif session.track == 1:
            track = "디자인"
        elif session.track == 2:
            track = "프론트엔드"
        else:
            track = "백엔드"
        
        session_detail_json = {
            "title" : session.title,
            "thumbnail" : image_list,
            "track" : track,
            "presenter" : session.presenter,
            "topic" : session.topic,
            "description" : session.description,
            "date" : session.date,
            "reference" : session.reference,
            "degree" : session.degree
        }
        
        return Response(data={
            "message" : "success",
            "data" : session_detail_json
        }, status=status.HTTP_200_OK)
        
        
        


