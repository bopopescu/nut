from django.db import models
from django.utils.encoding import force_unicode


from copy import deepcopy
# from base64 import b64encode, b64decode
# from zlib import compress, decompress
from json import dumps, loads


class ListObj(str):

    '''
    '''

def dbsafe_encode(value):
    _value = deepcopy(dumps(value))
    return ListObj(_value)

def dbsafe_decode(value):
    _value = deepcopy(loads(value))
    return _value

class ListObjectField(models.Field):

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        # self.compress = kwargs.pop('compress', False)
        kwargs.setdefault('editable', False)
        super(ListObjectField, self).__init__(*args, **kwargs)

    def get_default(self):
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        return super(ListObjectField, self).get_default()

    def to_python(self, value):
        if value is not None:
            try:
                value = dbsafe_decode(value)
            except:
                if isinstance(value, ListObj):
                    raise
        return value

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if value is not None and not isinstance(value, ListObj):
            value = force_unicode(dbsafe_encode(value))
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def get_internal_type(self):
        return 'TextField'

    def get_db_prep_lookup(self, lookup_type, value, connection=None,
                           prepared=False):
        if lookup_type not in ['exact', 'in', 'isnull']:
            raise TypeError('Lookup type %s is not supported.' % lookup_type)
        try:
            return super(ListObjectField, self).get_db_prep_lookup(lookup_type, value, connection, prepared)
        except TypeError:
            return super(ListObjectField, self).get_db_prep_lookup(lookup_type, value, None)


__author__ = 'edison7500'
