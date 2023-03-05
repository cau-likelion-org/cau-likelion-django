from django.db import models
from django.conf import settings
from accounts.models import User

class Gallery(models.Model):
    # 1. 게시글의 id 값
    gallery_id = models.AutoField(primary_key=True, null=False, blank=False)
    # 2. 작성자 id 값
    member_id = models.ForeignKey(User, on_delete = models.CASCADE, 
                                  db_column = "member_id", verbose_name = "작성자 id값", )
    # 3. 글 제목
    title = models.CharField(verbose_name = "글 제목", max_length=30)
    # 4. 썸네일
    thumbnail = models.ImageField(verbose_name = "썸네일", max_length=200)
    # 5. 글 내용
    description = models.TextField(null=True, blank = True, verbose_name = "글 내용")
    # 6. 날짜
    date = models.CharField(max_length = 30, null = True, blank = True)

    class Meta:
        verbose_name = '갤러리'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def __int__(self):
        return self.gallery_id

class GalleryImage(models.Model):
    # 1. 사진 id 값
    id = models.AutoField(primary_key=True, null = False, blank = False)
    # 2. 갤러리 id 값
    gallery_id = models.ForeignKey(Gallery, related_name = "image", on_delete = models.CASCADE, 
                                    db_column= "gallery_id", verbose_name = "갤러리id값",)
    # 3. 사진 url 값                                
    image = models.ImageField(verbose_name = "사진 url", max_length = 100)     

    class Meta:
        verbose_name = "추억사진"
        verbose_name_plural = "추억사진들"

    def __int__(self):
        return self.id