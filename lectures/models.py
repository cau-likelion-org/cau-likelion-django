from django.db import models
from django.conf import settings
from accounts.models import User

class Session(models.Model):
    CHOICES = (
        ('front', 'front'),
        ('back', 'back'),
        ('design', 'design'),
        ('pm', 'pm')
    )
    # 1. 게시글의 id 값
    session_id = models.AutoField(primary_key=True, null=False, blank=False)
    # 2. 작성자 id 값
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, 
                                  db_column = "user_id", verbose_name = "작성자 id값")
    # 3. 글 제목
    title = models.CharField(max_length= 50)
    # 4 트랙
    track = models.CharField(null=True, blank = True, verbose_name='트랙', max_length=10)
    # 5. 썸네일
    thumbnail = models.ImageField(verbose_name = "썸네일", max_length=200)
    # 6. 글 내용
    description = models.TextField(null=True, blank = True, verbose_name = "글 내용")
    # 7. 발표자
    presenter = models.CharField(max_length=10, verbose_name='발표자', default='변주현')
    # 8. 발표 주제
    topic = models.CharField(max_length=50, verbose_name='세션 주제')
    # 9. 몇차 세션
    degree = models.IntegerField(verbose_name= '세션 차수', null = True, blank = True)
    # 10. 세션 레퍼런스 pdf
    reference = models.URLField(max_length=1024, default='')
    # 11. 세션 날짜
    date = models.CharField(max_length=20, default='')
    
    class Meta:
        verbose_name = '세션'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title    
    
    def __int__(self):
        return self.session_id

class SessionImage(models.Model):
    # 1. 사진 id 값
    id = models.AutoField(primary_key=True, null = False, blank = False)
    # 2. 갤러리 
    session = models.ForeignKey(Session, related_name = "image", on_delete = models.CASCADE, 
                                    db_column= "session_id", verbose_name = "세션id값",)
    # 3. 사진 url 값                                
    image = models.ImageField(verbose_name = "사진 url", max_length = 100)     
    
    class Meta:
        verbose_name = "세션사진"
        verbose_name_plural = "세션사진들"

    def __int__(self):
        return self.id