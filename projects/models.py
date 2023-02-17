from django.db import models
from django.conf import settings
from accounts.models import User

class Project(models.Model):
    # 1. 게시글의 id 값
    project_id = models.AutoField(primary_key=True, null=False, blank=False)
    # 2. 작성자 id 값
    member_id = models.ForeignKey(User, on_delete = models.CASCADE, 
                                  db_column = "member_id", verbose_name = "작성자 id값", )
    # 3. 글 제목
    title = models.CharField(max_length= 50)
    # 4 기술 스택
    dev_stack = models.CharField(null=False, blank = False, max_length = 200, verbose_name='트랙')
    # 5. 썸네일
    thumbnail = models.ImageField(verbose_name = "썸네일", max_length=200)
    # 6. 프로젝트 상세 설명
    description = models.TextField(null=True, blank = True, verbose_name = "글 내용")
    # 7. 기수
    version = models.IntegerField(verbose_name = "기수")
    # 8. 팀 이름
    team_name = models.CharField(verbose_name='팀 이름', max_length=30)
    # 9. 팀 멤버
    team_member = models.JSONField(default=dict)
    # 10. 프로젝트 시작 일자
    start_date = models.CharField(verbose_name= '프로젝트 시작일자', max_length=20)
    # 11. 프로젝트 종료 일자
    end_date = models.CharField(verbose_name='프로젝트 종료 일자', max_length=20)
    # 12. 관련 링크
    link = models.JSONField(default=dict)
    # 13. 카테고리
    category = models.CharField(max_length=100)

    class Meta:
        verbose_name = '프로젝트'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title    

# class Link(models.Model):
#     CHOICES = (
#         ('github' , 'github'),
#         ('youtube' , 'youtube'),
#         ('web' , 'web'),
#     )

#     type = models.CharField(max_length=100, choices = CHOICES)
#     src = models.URLField(max_length=1024)
#     project = models.ForeignKey(Project, on_delete = models.CASCADE, db_column='project')



class ProjectImage(models.Model):
    # 1. 사진 id 값
    id = models.AutoField(primary_key=True, null = False, blank = False)
    # 2. 프로젝트 id 값
    project_id = models.ForeignKey(Project, related_name = "image", on_delete = models.CASCADE, 
                                    db_column= "project_id", verbose_name = "프로젝트id값",)
    # 3. 사진 url 값                                
    image = models.ImageField(verbose_name = "사진 url", max_length = 100)     

    class Meta:
        verbose_name = "프로젝트사진"
        verbose_name_plural = "프로젝트사진들"