from wand.image import  Image as WandImage
from hashlib import md5
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.conf import settings

image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')

avatar_path = getattr(settings, 'Avatar_Image_Path', 'avatar/')
# avatar_size = getattr(settings, 'Avatar_Image_Size', [50, 180])


class HandleImage(object):
    path = image_path

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
        _img.sample(_width, _height)
        # _img.resize(_width, _height)
        # _img.transform("%sx%s" % (_width, _height), "200%")
        self._image_data =  _img.make_blob()
        return self.image_data

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

    def save(self, path = None, resize=False, square=False):

        if square:
            self.crop_square()

        # else:
        if path:
            self.path = path

        filename = self.path + self.name + '.jpg'
        if not default_storage.exists(filename):
            filename = default_storage.save(filename, ContentFile(self.image_data))
        return filename


    def avatar_save(self, resize=True):
        self.path = avatar_path

        self.crop_square()
        if resize:
            self.resize(300, 300)

        filename = self.path + self.name + '.jpg'
        if not default_storage.exists(filename):
            filename = default_storage.save(filename, ContentFile(self.image_data))
        return filename


__author__ = 'edison'
