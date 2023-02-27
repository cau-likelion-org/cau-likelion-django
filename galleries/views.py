# 데이터 처리
from .models import Gallery,GalleryImage
from .serializers import GallerySerializer, GalleryImageSerializer
from django.views.decorators.csrf import csrf_exempt

# APIView를 사용하기 위해 import
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
from rest_framework import status, viewsets
# from django.http import Http404

@csrf_exempt
class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

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