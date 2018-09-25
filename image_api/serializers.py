from rest_framework import serializers
from image_api.models import Image, TransferedImage,RotatedImage  # Import our UploadedImage model


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('pk', 'fn','extension')


class TransferedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferedImage
        fields = ('pk', 'source_pk', 'fn', 'extension')

class RotatedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RotatedImage
        fields = ('pk', 'source_pk', 'fn', 'degree')