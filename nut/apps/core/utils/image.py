from wand.image import  Image as WandImage
from hashlib import md5
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


class HandleImage(object):

    def __init__(self, image_file):
        if hasattr(image_file, 'chunks'):
            self._image_data = ''.join(chuck for chuck in image_file.chunks())
        else:
            self._image_data = image_file.read()
        image_file.close()

        self._name = None


    @property
    def image_data(self):
        return self._image_data

    @property
    def name(self):
        self._name = md5(self.image_data).hexdigest()
        return self._name

    def resize(self, w, h):
        _img = WandImage(blob = self._image_data)

        if (w /  h > _img.width / _img.height):
            _width = round(h * _img.width / _img.height)
            _height = h
        else:
            _width = w
            _height = round(w * _img.height / _img.width)

        _width = int(_width)
        _height = int(_height)

        _img.resize(_width, _height)
        return _img.make_blob()


    def crop_square(self):
        _img = WandImage(blob = self._image_data)
        _delta = _img.width - _img.height
        if _delta > 0:
            _img.crop(_delta / 2 , 0, width = _img.height, height = _img.height)
        elif _delta < 0:
            _img.crop(0, -_delta / 2, width = _img.width, height = _img.width)

        self._image_data = _img.make_blob()
        # _img.resize(size, size)
        # return _img.make_blob()

        # if (w /  h > _img.width / _img.height):
        #     _width = round(h * _img.width / _img.height)
        #     _height = h
        # else:
        #     _width = w
        #     _height = round(w * _img.height / _img.width)
        #
        # _width = int(_width)
        # _height = int(_height)
        #
        # _img.resize(_width, _height)
        # return _img.make_blob()

    def save(self, resize=False, square=False):
        if resize:
            pass

        if square:
            self.crop_square()
        # else:

        filename =  image_path + self.name + '.jpg'
        filename = default_storage.save(filename, ContentFile(self.image_data))
        return filename


__author__ = 'edison'
