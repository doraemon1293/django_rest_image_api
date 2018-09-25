from django.conf.urls import url
from image_api import views
from django.urls import path,register_converter

#allowed image formats
class ImageFormatConverter:
    regex = r"tiff|bmp|jpeg|webp|png|gif"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value

register_converter(ImageFormatConverter, 'image_format')

urlpatterns = [
    path('image_api/', views.ImageList.as_view(),name="image"),
    path('image_api/<int:pk>/', views.ImageDetail.as_view(),name="image-get"),
    path('image_api/<int:pk>/transfer/<image_format:extension>/', views.ImageTransfer.as_view(),name="image-transfer"),
    path('image_api/<int:pk>/rotate/<int:degree>/', views.ImageRotation.as_view(),name="image-rotate"),

]