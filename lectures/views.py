# 데이터 처리
from .models import Session
from .serializers import SessionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from django.http import Http404

# 세션의 목록을 보여주는 역할
class SessionList(APIView):
    # 세션 리스트를 보여줄 때
    def get(self,request):
        session_list = Session.objects.all()
    
        pm = []
        design = []
        front = []
        back = []
        etc = [] # 기타

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
            elif session.track == 3:
                back.append(session_json)
            elif session.track == 4:
                etc.append(session_json)


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
                "thumbnail" : images,
                "track" : session.track,
                "presenter" : session.presenter,
                "topic" : session.topic,
                "description" : session.description,
                "date" : session.date,
                "reference" : session.reference,
                "degree" : session.degree
            }
        }, status=status.HTTP_200_OK)  
        # session = Session.objects.get(session_id=id)
        
        # image_list = []
        
        # session_images = SessionImage.objects.filter(session=session)
        
        # for session_image in session_images:
        #     image_url = session_image.image
        #     image_list.append(image_url)
        
        # if session.track == 0:
        #     track = "기획"
        # elif session.track == 1:
        #     track = "디자인"
        # elif session.track == 2:
        #     track = "프론트엔드"
        # else:
        #     track = "백엔드"
        
        # session_detail_json = {
        #     "title" : session.title,
        #     "thumbnail" : image_list,
        #     "track" : track,
        #     "presenter" : session.presenter,
        #     "topic" : session.topic,
        #     "description" : session.description,
        #     "date" : session.date,
        #     "reference" : session.reference,
        #     "degree" : session.degree
        # }
        
        # return Response(data={
        #     "message" : "success",
        #     "data" : session_detail_json
        # }, status=status.HTTP_200_OK)
        
        
        


