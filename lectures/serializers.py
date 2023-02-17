from rest_framework import serializers
from .models import Session, SessionImage


class SessionImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = SessionImage
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()

    # 게시글에 등록된 이미지들 가지고 오기
    def get_images(self,obj):
        image = obj.image.all()
        return SessionImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Session
        fields = '__all__'

    def create(self, validated_data):
        instance = Session.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            SessionImage.objects.create(session_id=instance, image=image_data)
        return instance

