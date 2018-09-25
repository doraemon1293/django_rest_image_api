import PIL.Image
import os
from image_api.models import TransferedImage, RotatedImage
from django_rest_image_api.settings import MEDIA_ROOT


def detect_image_format(fn):
    img = PIL.Image.open(fn)
    return img.format.lower()


def transfer_image_format(image, extension):
    extension = extension.lower()
    img = PIL.Image.open(image.fn)
    # if extension is the same with original, return 0
    if img.format.lower() == extension:
        return 0
    else:
        fn = os.path.splitext(str(image.fn))[0]
        new_fn = "{}.{}".format(fn,extension)
        transfered_image = TransferedImage(source_pk=image, fn=new_fn, extension=extension)
        # remove alpha if required format is jpeg
        if extension == "jpeg":
            img = img.convert("RGB")
        img.save(os.path.join(MEDIA_ROOT, new_fn))
        return transfered_image


def rotate_image(image, degree):
    img = PIL.Image.open(image.fn)
    fn, extension = os.path.splitext(str(image.fn))
    new_img = img.rotate(degree, expand=1)
    new_fn = "{}_{}.{}".format(fn,degree,extension)
    rotated_image = RotatedImage(source_pk=image, fn=new_fn, degree=degree)
    new_img.save(os.path.join(MEDIA_ROOT, new_fn))
    return rotated_image
