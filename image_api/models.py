import uuid
from django.db import models


def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)

class Image(models.Model):
    fn = models.ImageField(upload_to=scramble_uploaded_filename)
    extension = models.CharField(max_length=100,default="")


class TransferedImage(models.Model):
    source_pk = models.ForeignKey(Image,on_delete=models.CASCADE)
    fn = models.ImageField(upload_to=scramble_uploaded_filename)
    extension = models.CharField(max_length=100)

class RotatedImage(models.Model):
    source_pk = models.ForeignKey(Image,on_delete=models.CASCADE)
    fn = models.ImageField(upload_to=scramble_uploaded_filename)
    degree = models.IntegerField()