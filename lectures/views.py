# 데이터 처리
from .models import Session
from .serializers import SessionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

# class PostListAPIView(APIView):

#     def post(self,request):
#         serializer = SessionSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = 201)
#         return Response(serializer.errors, status=400)

#     def get(self,request):
#         session_list = Session.objects.values()

#         pm = []
#         design = []
#         front = []
#         back = []

#         for session in session_list:
#             if session['track'] == 'pm':
#                 pm.append({
#                     'id' : session['session_id'],
#                     'title' : session['title'],
#                     'degree' : session['degree'],
#                     'thumbnail' : session['thumbnail'],
#                 })
#             elif session['track'] == 'design':
#                 design.append({
#                     'id' : session['session_id'],
#                     'title' : session['title'],
#                     'degree' : session['degree'],
#                     'thumbnail' : session['thumbnail'],
#                 })
#             elif session['track'] == 'front':
#                 front.append({
#                     'id' : session['session_id'],
#                     'title' : session['title'],
#                     'degree' : session['degree'],
#                     'thumbnail' : session['thumbnail'],
#                 })
#             elif session['track'] == 'back':
#                 back.append({
#                     'id' : session['session_id'],
#                     'title' : session['title'],
#                     'degree' : session['degree'],
#                     'thumbnail' : session['thumbnail'],
#                 })


#         return Response(data={
#             "message" : "success",
#             "data" : {
#                 "0" : pm,
#                 "1" : design,
#                 "2" : front,
#                 "3" : back
#             }
#         }, status=status.HTTP_200_OK)




class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @action(detail=False, methods = ['GET'], url_path = 'sessionlisttest')
    def get_sessions(self, request):
        session_list = Session.objects.values()

        pm = []
        design = []
        front = []
        back = []

        for session in session_list:
            if session['track'] == 'pm':
                pm.append({
                    'id' : session['session_id'],
                    'title' : session['title'],
                    'degree' : session['degree'],
                    'thumbnail' : session['thumbnail'],
                })
            elif session['track'] == 'design':
                design.append({
                    'id' : session['session_id'],
                    'title' : session['title'],
                    'degree' : session['degree'],
                    'thumbnail' : session['thumbnail'],
                })
            elif session['track'] == 'front':
                front.append({
                    'id' : session['session_id'],
                    'title' : session['title'],
                    'degree' : session['degree'],
                    'thumbnail' : session['thumbnail'],
                })
            elif session['track'] == 'back':
                back.append({
                    'id' : session['session_id'],
                    'title' : session['title'],
                    'degree' : session['degree'],
                    'thumbnail' : session['thumbnail'],
                })


        return Response(data={
            "message" : "success",
            "data" : {
                "0" : pm,
                "1" : design,
                "2" : front,
                "3" : back
            }
        }, status=status.HTTP_200_OK)
