# 데이터 처리
from .models import Gallery,GalleryImage
from .serializers import GallerySerializer, GalleryImageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from django.http import Http404
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3
from datetime import datetime
from django.http import JsonResponse
import uuid

# 갤러리의 목록을 보여주는 역할
class GalleryList(APIView):
    # 갤러리 리스트를 보여줄 때
    def get(self, request):
        gallery_list = Gallery.objects.values()

        one = [] # 2021년
        two = [] # 2022년
        three = [] # 2023년 // 사이드프로젝트 이어받는 분들 이 다음부터 2024년은 four 2025년은 five 하시면 됩니다.       

        for gallery in gallery_list:
            if gallery['date'][0:4] == '2021':
                one.append({
                    'id' : gallery['gallery_id'],
                    'title' : gallery['title'],
                    'date' : gallery['date'],
                    'thumbnail' : gallery['thumbnail'],
                })
            elif gallery['date'][0:4] == '2022':
                two.append({
                    'id' : gallery['gallery_id'],
                    'title' : gallery['title'],
                    'date' : gallery['date'],
                    'thumbnail' : gallery['thumbnail'],
                })
            elif gallery['date'][0:4] == '2023':
                three.append({
                    'id' : gallery['gallery_id'],
                    'title' : gallery['title'],
                    'date' : gallery['date'],
                    'thumbnail' : gallery['thumbnail'],
                })


        return Response(data={
            "message" : "success",
            "data" : {
                "2021" : one,
                "2022" : two,
                "2023" : three,
                # "2024" : four,
            }
        }, status=status.HTTP_200_OK)

    # 새로운 추억 글을 작성할 때
    def post(self, request):
        s3_client = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        )
        
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        images = request.FILES.getlist('images')
        # gallery_id = request.GET.get('gallery_id')
        # thumbnail = request.FILES.get('thumbnail')
        
        for image in images :
            # image_time = (str(datetime.now())).replace(" ","")
            # image_type = (file.content_type).split("/")[1]
            image_id = str(uuid.uuid4())
            s3_client.upload_fileobj(
                image,
                "chunghaha",
                image_id,
                 ExtraArgs = {
                     "ContentType" : image.content_type
                }
            )
            image_url = f"http://chunghaha.s3.ap-northeast-2.amazonaws.com//{image_id}"
            member_id = request.GET.get('member_id')

            # Gallery.objects.create(
            #     title = request.GET.get('title'),
            #     thumbnail = thumbnail,
            #     description = request.GET.get('description'),
            #     member_id = member_id,
            #     date = request.GET.get('date')
            # )
            
            # image_url = image_url.replace(" ", "/")
                
            # image_time = (str(datetime.now())).replace(" ","")
            # image_type = (thumbnail.content_type).split("/")[1]
            # s3_client.upload_fileobj(
            #     thumbnail,
            #     "chunghaha",
            #     str(uuid.uuid4()),
            #     ExtraArgs = {
            #          "ContentType" : thumbnail.content_type
            #     }
            # )

            # GalleryImage.objects.create(
            #     image = image_url,
            #     gallery_id = gallery_id
            # )
        return Response(data={
        "message" : "success",
        "data" : {
            "gallery_id" : 13,
            "title" : request.GET.get('title')
        }
    }, status=status.HTTP_200_OK)


        # request.data는 사용자의 입력 데이터
        # serializer = GallerySerializer(data=request.data)
        # if serializer.is_valid(): #유효성 검사
        #     serializer.save() # 저장
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
# Gallery의 detail을 보여주는 역할
class GalleryDetail(APIView):
    # Gallery 객체 가져오기
    def get_object(self, pk):
        try:
            return Gallery.objects.get(pk=pk)
        except Gallery.DoesNotExist:
            raise Http404
    
    # Gallery의 detail 보기
    def get(self, request, pk, format=None):
        gallery = self.get_object(pk)
        gallery_images = gallery.image.all()
        images = []
        for img in gallery_images:
            images.append(str(img.image))
            
        return Response(data={
            "message" : "success",
            "data" : {
                "id" : gallery.gallery_id,
                "title" : gallery.title,
                "image" : images,
                "date" : gallery.date,
                "description" : gallery.description
            }
        }, status=status.HTTP_200_OK)    

    # Gallery 수정하기
    def put(self, request, pk, format=None):
        gallery = self.get_object(pk)
        serializer = GallerySerializer(gallery, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Gallery 삭제하기
    def delete(self, request, pk, format=None):
        gallery = self.get_object(pk)
        gallery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class GalleryViewSet(viewsets.ModelViewSet):
#     queryset = Gallery.objects.all()
#     serializer_class = GallerySerializer

#     @action(detail=False, methods = ['GET'], url_path = '')
#     def get_galleries(self, request):
#         gallery_list = Gallery.objects.values()

#         one = [] # 2021년
#         two = [] # 2022년
#         three = [] # 2023년 // 사이드프로젝트 이어받는 분들 이 다음부터 2024년은 four 2025년은 five 하시면 됩니다.       

#         for gallery in gallery_list:
#             if gallery['date'][0:4] == '2021':
#                 one.append({
#                     'id' : gallery['gallery_id'],
#                     'title' : gallery['title'],
#                     'date' : gallery['date'],
#                     'thumbnail' : gallery['thumbnail'],
#                 })
#             elif gallery['date'][0:4] == '2022':
#                 two.append({
#                     'id' : gallery['gallery_id'],
#                     'title' : gallery['title'],
#                     'date' : gallery['date'],
#                     'thumbnail' : gallery['thumbnail'],
#                 })
#             elif gallery['date'][0:4] == '2023':
#                 three.append({
#                     'id' : gallery['gallery_id'],
#                     'title' : gallery['title'],
#                     'date' : gallery['date'],
#                     'thumbnail' : gallery['thumbnail'],
#                 })


#         return Response(data={
#             "message" : "success",
#             "data" : {
#                 "2021" : one,
#                 "2022" : two,
#                 "2023" : three,
#                 # "2024" : four,
#             }
#         }, status=status.HTTP_200_OK)

# 추억게시판 목록 보여주기 + 새로운 게시글 생성
# class GalleryList(APIView):
#     # 추억게시판 목록 보여주는 메서드
#     def get(self, request):
#             Galleries = Gallery.objects.all()
#             # 여러 개의 객체를 serialization하기 위해 many=True로 설정
#             serializer = GallerySerializer(Galleries, many=True)
#             return Response(serializer.data)

#     # 새로운 게시글을 작성할 때
#     def post(self, request):
#         # request.data는 사용자의 입력 데이터
#         parser_classes = [MultiPartParser]
#         serializer = GallerySerializer(data=request.data)
#         if serializer.is_valid(): #유효성 검사
#             serializer.save() # 저장
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # 추억 게시판의 detail을 보여주는 역할
# class GalleryDetail(APIView):
#     # Gallery 객체 가져오기
#     def get_object(self, pk):
#         try:
#             return Gallery.objects.get(pk=pk)
#         except Gallery.DoesNotExist:
#             raise Http404
    
#     # Gallery의 detail 보기
#     def get(self, request, pk, format=None):
#         gallery = self.get_object(pk)
#         serializer = GallerySerializer(gallery)
#         return Response(serializer.data)

#     # Gallery 수정하기
#     def put(self, request, pk, format=None):
#         gallery = self.get_object(pk)
#         serializer = GallerySerializer(gallery, data=request.data) 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data) 
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Gallery 삭제하기
#     def delete(self, request, pk, format=None):
#         gallery = self.get_object(pk)
#         gallery.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# gallery = self.get_object(pk)
        # serializer = GallerySerializer(gallery)
        # return Response(serializer.data)