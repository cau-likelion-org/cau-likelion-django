from rest_framework import serializers
from .models import Project, ProjectImage
import boto3 
from django.conf import settings


class ProjectImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProjectImage
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()

    # 게시글에 등록된 이미지들 가지고 오기
    def get_images(self,obj):
        image = obj.image.all()
        return ProjectImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        thumbnail_data = validated_data.pop('thumbnail', None)
        
        project = Project.objects.create(**validated_data)

        if thumbnail_data:
            project.thumbnail = self.upload_to_s3(thumbnail_data, 'thumbnail')
            project.save()

        for image in images_data:
            image_url = self.upload_to_s3(image, 'project-images')
            ProjectImage.objects.create(project_id=project, image=image_url)
            
        return project
    
    def upload_to_s3(self, file, folder):
        s3_client = boto3.client(
            's3',
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
            region_name = settings.AWS_REGION
            )

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        file_key = f"{folder}/{file.name}"

        s3_client.upload_fileobj(file, bucket_name, file_key)

        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
        return s3_url

