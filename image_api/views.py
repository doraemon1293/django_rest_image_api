from image_api.models import Image, TransferedImage, RotatedImage
from image_api.serializers import ImageSerializer, TransferedImageSerializer, RotatedImageSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from image_api.transfer import detect_image_format, transfer_image_format, rotate_image


class ImageList(APIView):
    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()
            # use PIL to detect the format of image
            extension = detect_image_format(image.fn)
            image.extension = extension
            image.save()
            serializer = ImageSerializer(image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):
    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageTransfer(APIView):
    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, extension):
        # if already exists, retreive
        transfered_image = TransferedImage.objects.filter(source_pk=pk, extension=extension)
        if len(transfered_image) == 1:
            serializer = TransferedImageSerializer(transfered_image[0])
        else:
            # not exist, transfer format
            image = self.get_object(pk)
            transfered_image = transfer_image_format(image, extension)
            # if return 0 extension is the same with original
            if transfered_image == 0:
                serializer = ImageSerializer(image)
            else:
                transfered_image.save()
                serializer = TransferedImageSerializer(transfered_image)
        return Response(serializer.data)


class ImageRotation(APIView):
    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, degree):
        # if already exists, retreive
        rotated_image = RotatedImage.objects.filter(source_pk=pk, degree=degree)
        if len(rotated_image) == 1:
            serializer = RotatedImageSerializer(rotated_image[0])
        else:
            # not exist, rotate
            image = self.get_object(pk)
            rotated_image = rotate_image(image, degree)
            rotated_image.save()
            serializer = RotatedImageSerializer(rotated_image)
        return Response(serializer.data)
