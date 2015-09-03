from wand.image import  Image as WandImage
from hashlib import md5
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.conf import settings
from django.utils.log import getLogger

log = getLogger('django')


image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')
avatar_path = getattr(settings, 'Avatar_Image_Path', 'avatar/')
# avatar_size = getattr(settings, 'Avatar_Image_Size', [50, 180])

class GImageException(Exception):
    pass

class HandleImage(object):
    path = image_path

    def __init__(self, image_file):
        try:
            self._content_type = image_file.content_type
        except AttributeError:
            self._content_type = None

        if hasattr(image_file, 'chunks'):
            self._image_data = ''.join(chuck for chuck in image_file.chunks())
        else:
            self._image_data = image_file.read()

        self.ext_name = self.get_ext_name()
        image_file.close()
        log.info('init HandleImage obj---')
        self._name = None
        self.img = WandImage(blob=self._image_data)

    @property
    def image_data(self):
        # self._image_data.format = 'jpeg'
        return self._image_data

    @property
    def content_type(self):
        if self._content_type is None:
            return None

        if self._content_type == 'image/png':
            self._content_type = 'image/jpeg'
        return self._content_type

    def get_ext_name(self):
        ext = 'jpg'
        try:
            ext = self._content_type.split('/')[1]
        except :
            pass

        return ext

    @property
    def name(self):
        self._name = md5(self.image_data).hexdigest()
        return self._name

    def resize(self, w, h):
        # _img = WandImage(blob = self._image_data)
        # _img.format = 'jpeg'
        if (w /  h > self.img.width / self.img.height):
            _width = round(h * self.img.width / self.img.height)
            _height = h
        else:
            _width = w
            _height = round(w * self.img.height / self.img.width)

        _width = int(_width)
        _height = int(_height)
        # _img.sample(_width, _height)
        self.img.resize(_width, _height)
        # _img.transform("%sx%s" % (_width, _height), "200%")
        self._image_data = self.img.make_blob()
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
        # log.info('begin save -----')

        if self.ext_name == 'png':
            # _img = WandImage(blob = self._image_data)
            # _img.format = 'jpeg'
            self._image_data = self.img.make_blob(format='jpeg')
            self.ext_name = 'jpg'

        if square and (self.ext_name == 'jpg') :
            self.crop_square()
        # else:
        if path:
            self.path = path

        filename = self.path + self.name +'.' + self.ext_name
        # log.info(filename)
        if not default_storage.exists(filename):
            try:
                # log.info('real saveing begin----')
                filename = default_storage.save(filename, ContentFile(self.image_data))
            except Exception as e:
                log.info(e)
        else:
            # log.info('file exist!----')
            pass

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

    def icon_save(self, **kwargs):

        path = kwargs.pop('path', None)
        if path:
            self.path = path

        if self.img.format == "PNG":
            self.ext_name = 'png'

        filename = self.path + self.name +'.' + self.ext_name
        if not default_storage.exists(filename):
            filename = default_storage.save(filename, ContentFile(self.image_data))
        return filename

class LimitedImage(HandleImage):
    def __init__(self, image_file):
        super(LimitedImage,self).__init__(image_file)
        self.maxReturnWidth = 750


    def handleWidth(self, maxWidth):
        try :
            maxWidth = int(maxWidth)
        except ValueError:
            raise GImageException('maxWidth should be a number')

        (width, height) = self.img.size
        if width > maxWidth:
            ratio = float(maxWidth)/float(width)
            newHeight = int(height * ratio)
            self.img.sample(maxWidth,newHeight)
            self._image_data = self.img.make_blob()
        return

    def handleQuality(self, quality):
        try:
            quality = int(quality)
        except ValueError:
            raise GImageException('quality should be a number')

        if quality > 100 or quality <=0 :
            quality = 70

        self.img.compression_quality = quality
        self._image_data = self.img.make_blob()
        return

    def save(self, path = None, resize=False, square=False, maxWidth=None,maxQuality=None):
        if maxWidth:
            self.handleWidth(maxWidth)

        if maxQuality:
            self.handleQuality(maxQuality)

        file_name = super(LimitedImage,self).save(path, resize ,square)

        return file_name

__author__ = 'edison'
