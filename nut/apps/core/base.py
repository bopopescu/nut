from django.db import  models

class BaseModel(models.Model):
    class Meta:
        abstract = True

    def toDict(self):
        fields = []
        for f in self._meta.fields:
            fields.append(f.column)
        d = {}
        for attr in fields:
            # log.info( getattr(self, attr) )
            value = getattr(self, attr)
            if value is None:
                continue
            elif isinstance(value, dict):
                d[attr] = getattr(self, attr)
            elif isinstance(value, list):
                d[attr] = getattr(self, attr)
            else:
                d[attr] = "%s" % getattr(self, attr)
        return d

    def pickToDict(self, *args):
        '''
          only work on simple python value fields ,
          can not use to serialize object field!
        '''
        d = {}
        for key in args:
            d[key] = getattr(self, key, None)
        return d