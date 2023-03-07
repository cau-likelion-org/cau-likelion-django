from rest_framework import serializers
from .models import Gallery, GalleryImage

class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = GalleryImage
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = '__all__'

    # 게시글에 등록된 이미지들 가지고 오기
    # def get_images(self,obj):
    #     image = obj.image.all()
    #     return GalleryImageSerializer(instance=image, many=True, context=self.context).data

    # def create(self, validated_data):
    #     instance = Gallery.objects.create(**validated_data)
    #     image_set = self.context['request'].FILES
    #     for image_data in image_set.getlist('image'):
    #         image_url = "https://chunghaha.s3.ap-northeast-2.amazonaws.com/"+
    #         GalleryImage.objects.create(gallery_id=instance, image=image_data)
    #     return instance
