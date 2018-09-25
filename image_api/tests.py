from django.test import TestCase
from rest_framework import status
from image_api.models import Image
from image_api.serializers import ImageSerializer
import urllib.request
import filecmp
from django_rest_image_api.settings import HOSTNAME
from django.urls import reverse
from django_rest_image_api.settings import MEDIA_ROOT
import os.path


# Create your tests here.

class ListImagesTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        Image.objects.create(
            fn="32170825-0139-43d5-8686-cac1cc37d585.jpeg", extension="jpeg")
        Image.objects.create(
            fn="b64c7d18-9aa8-4bfb-a3a7-5eed40345342.jpeg", extension="jpeg")
        Image.objects.create(
            fn="31e08b1f-b4f6-4477-bb29-b6a22c62016d.jpeg", extension="jpeg")

    def test_image_list(self):
        url = reverse("image")
        response = self.client.get(url)
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetImageTest(TestCase):
    _pk = 1
    _fn = "7033ab72-1bfa-46e4-9428-3b3e780d5972.jpeg"

    def setUp(self):
        Image.objects.create(
            pk=self._pk, fn=self._fn, extension="jpeg")

    def test_get_image(self):
        image = Image.objects.get(pk=self._pk)
        serializer = ImageSerializer(image)
        url = reverse("image-get", args=[self._pk])
        response = self.client.get(url)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UploadImageTest(TestCase):
    """ upload an Image, return its pk
        get the Image file URL by the pk
        download file and compare whether two files are the same
    """

    def test_upload_and_retreive_image(self):
        # upload
        test_upload_file_name = os.path.join(MEDIA_ROOT, r"testimages\1.jpeg")
        url = reverse("image")
        with open(test_upload_file_name, 'rb') as fp:
            response = self.client.post(url, {'fn': fp}, format='multipart')
        # uploaded successfully
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        pk = response.data["pk"]

        # get the uploaded image
        url = reverse("image-get", args=[pk])
        response = self.client.get(url)
        # successfully
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        fn = response.data["fn"]  # fn is the url of the image
        # download file
        test_download_file_name = os.path.join(MEDIA_ROOT, r"testimages\test_download_file")
        urllib.request.urlretrieve(HOSTNAME + fn, test_download_file_name)
        # file is the same with original
        self.assertEqual(filecmp.cmp(test_upload_file_name, test_download_file_name), True)


class TransferImageTest(TestCase):
    """ upload the image and download the format transfered image
        if _compare_file_required, this method will also compare whether the transfered file is exactly the same with sample file
        As some conversion cannot guarantee the file is always the same, for example from png to jpeg, so should not compare files in that case
    """
    _compare_file_required = True

    def test_transfer_image(self):

        original_image = os.path.join(MEDIA_ROOT, r"testimages\1.jpeg")
        extensions__correct_images = {"bmp": os.path.join(MEDIA_ROOT, r"testimages\1.bmp"),
                                      "gif": os.path.join(MEDIA_ROOT, r"testimages\1.gif"),
                                      "jpeg": os.path.join(MEDIA_ROOT, r"testimages\1.jpeg"),
                                      "tiff": os.path.join(MEDIA_ROOT, r"testimages\1.tiff"),
                                      "webp": os.path.join(MEDIA_ROOT, r"testimages\1.webp"),
                                      "png": os.path.join(MEDIA_ROOT, r"testimages\1.png"),
                                      }
        test_download_file_name = os.path.join(MEDIA_ROOT, r"testimages\test_download_file")

        # upload the original image
        url = reverse("image")
        with open(original_image, 'rb') as fp:
            response = self.client.post(url, {'fn': fp}, format='multipart')
        pk = response.data["pk"]
        original_extension = response.data["extension"]
        # test every extension
        for extension, correct_image in extensions__correct_images.items():
            # get the transfered image
            url = reverse("image-transfer", args=[pk, extension])
            response = self.client.get(url)
            # successfully
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            fn = response.data["fn"]  # fn is the url of the image
            if self._compare_file_required:
                # download file
                urllib.request.urlretrieve(HOSTNAME + fn, test_download_file_name)
                if extension == original_extension:  # if the required extension is the same with original one, compare to priginal file
                    self.assertEqual(filecmp.cmp(original_image, test_download_file_name), True)
                else:  # compare to the pre-converted image
                    self.assertEqual(filecmp.cmp(correct_image, test_download_file_name), True)


class RotateImageTest(TestCase):
    _degree = 90

    def test_rotate_image(self):
        """ upload an Image, return its pk
            get the Image file URL by the pk
            download file and compare whether two files are the same
        """
        original_image = os.path.join(MEDIA_ROOT, r"testimages\1.jpeg")
        test_download_file_name = os.path.join(MEDIA_ROOT, r"testimages\test_download_file")
        correct_image = os.path.join(MEDIA_ROOT, r"testimages\1_90.jpeg")
        # upload the original image
        url = reverse("image")
        with open(original_image, 'rb') as fp:
            response = self.client.post(url, {'fn': fp}, format='multipart')
        pk = response.data["pk"]
        # get the rotated image
        url = reverse("image-rotate", args=[pk, self._degree])
        response = self.client.get(url)
        # successfully
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        fn = response.data["fn"]  # fn is the url of the image
        # download file
        urllib.request.urlretrieve(HOSTNAME + fn, test_download_file_name)
        self.assertEqual(filecmp.cmp(correct_image, test_download_file_name), True)


if __name__ == "__main__":
    pass
