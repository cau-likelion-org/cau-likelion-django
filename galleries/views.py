# 데이터 처리
from .models import Gallery, GalleryImage
from accounts.models import User
from .serializers import GallerySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3
from django.conf import settings

# 갤러리의 목록을 보여주는 역할
class GalleryList(APIView):
    # 갤러리 리스트를 보여줄 때
    s3_client = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        )
    def get(self, request):
        gallery_list = Gallery.objects.values()

        one = [] # 2021년
        two = [] # 2022년
        three = [] # 2023년 // 사이드프로젝트 이어받는 분들 이 다음부터 2024년은 four 2025년은 five 하시면 됩니다. 
        four = []      

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
            elif gallery['date'][0:4] == '2024':
                four.append({
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
                "2024" : four,
            }
        }, status=status.HTTP_200_OK)
    
    # 새로운 추억 글을 작성할 때
    def post(self, request):
        thumbnail = request.FILES['thumbnail'] # request의 썸네일 파일 가져오기
        gallery_title = request.POST['title'] # request의 제목 가져오기
        req_description = request.POST['description'] # request의 사진 내용설명 가져오기
        req_date = request.POST['date']
        login_email = request.POST['login_email']
        memberid = User.objects.get(
            email = login_email
        )
        thumbnail_url = f"gallery-images/{gallery_title}/thumbnail" # DB에 저장될 썸네일 이미지 url 설정
        self.s3_client.upload_fileobj(
            thumbnail,
            settings.AWS_STORAGE_BUCKET_NAME,
            thumbnail_url,
            ExtraArgs={
                    "ContentType": thumbnail.content_type
                }
        )
        gallery_post = Gallery.objects.create(
            title = gallery_title,
            thumbnail = "https://dcpshnp4boilw.cloudfront.net/" + thumbnail_url,
            description = req_description,
            date = req_date,
            member_id = memberid
        )
        gallery_post.save()
        # ------------------ 여기까지 request에서 thumbnail을 가져와서 s3에 업로드한 내용 ------------------------
        
        images = request.FILES.getlist('images')
        cnt = 1
        for image in images:
            image_url = f"gallery-images/{gallery_title}/image{cnt}"
            self.s3_client.upload_fileobj(
                image,
                settings.AWS_STORAGE_BUCKET_NAME,
                image_url,
                ExtraArgs={
                        "ContentType": image.content_type
                    }
            )
            image = GalleryImage.objects.create(
                gallery_id = gallery_post,
                image = "https://dcpshnp4boilw.cloudfront.net/" + image_url
            )
            cnt = cnt + 1

        # ------------------ 여기까지 request에서 사진들 받아서 한 장씩 s3에 업로드한 내용 ---------------------------
        
        return Response(data={
        "message" : "success",
        "data" : {
            "title" : gallery_title
        }
    }, status=status.HTTP_200_OK)

        
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