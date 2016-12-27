from unittest import TestCase

from apps.api.serializers.sellers import IndexPageMetaSerializer
from apps.seller.models import IndexPageMeta
import  rest_framework.generics

class TestIndexMetaSerializer(TestCase):
    def test_serializer_validation(self):
        data = {
            'year': 2015,
            'writer_list' : 'ant,clara,steph',
            'topic_tag_list'  : 'bread,cake,tuko',
            'column_article_tag_list':'war,peace'
        }

        s = IndexPageMetaSerializer(data=data)
        self.assertEqual(s.is_valid(), True)
        inst = s.save()
        self.assertIsInstance(inst, IndexPageMeta)
        self.assertIsInstance(inst.writer_list, list)
        self.assertEqual(inst.writer_list, ['ant', 'clara', 'steph'])



