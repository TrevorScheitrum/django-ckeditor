from io import BytesIO
import os.path

try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile

from ckeditor import utils

THUMBNAIL_SIZE = (75, 75)
PHOTO_SIZE = (800,600)

def image_verify(f):
    Image.open(f).verify()


def resize_image(upload, file_name):
    resized_image_filename = file_name
    thumbnail_format = 'JPEG' 
    #file_format = thumbnail_format.split('/')[1]
    file_format = 'JPEG'
    
    #image = default_storage.open(file_path)
    image = Image.open(upload)
    
    # Convert to RGB if necessary
    # Thanks to Limodou on DjangoSnippets.org
    # http://www.djangosnippets.org/snippets/20/
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    
    
    # scale and crop original photo
    resized_imagefit = ImageOps.fit(image, PHOTO_SIZE, Image.ANTIALIAS)
    resized_image_io = BytesIO()
    resized_imagefit.save(resized_image_io, format=file_format)

    resized_image = InMemoryUploadedFile(
        resized_image_io,
        None,
        resized_image_filename,
        thumbnail_format,
        len(resized_image_io.getvalue()),
        None)
    resized_image.seek(0)
    
    return resized_image

    
def create_thumbnail(file_path):
    thumbnail_filename = utils.get_thumb_filename(file_path)
    
    #thumbnail_format = utils.get_image_format(os.path.splitext(file_path)[1])
    thumbnail_format = 'JPEG'
    
    #file_format = thumbnail_format.split('/')[1]
    file_format = 'JPEG'

    image = default_storage.open(file_path)
    image = Image.open(image)

    # Convert to RGB if necessary
    # Thanks to Limodou on DjangoSnippets.org
    # http://www.djangosnippets.org/snippets/20/
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    # scale and crop to thumbnail
    imagefit = ImageOps.fit(image, THUMBNAIL_SIZE, Image.ANTIALIAS)
    thumbnail_io = BytesIO()
    imagefit.save(thumbnail_io, format=file_format)

    thumbnail = InMemoryUploadedFile(
        thumbnail_io,
        None,
        thumbnail_filename,
        thumbnail_format,
        len(thumbnail_io.getvalue()),
        None)
    thumbnail.seek(0)
    
    return default_storage.save(thumbnail_filename, thumbnail)


def should_create_thumbnail(file_path):
    image = default_storage.open(file_path)
    try:
        Image.open(image)
    except IOError:
        return False
    else:
        return True
