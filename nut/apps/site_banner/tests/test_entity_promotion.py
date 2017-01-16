from apps.core.tests.models.Base import DBTestBase

from apps.site_banner.models import Entity_Promotion


class TestEntityPromotion(DBTestBase):

    def test_promotion_model(self):
        '''
        a Entity_Promotion model can be inited
        :return:
        '''

        ep = Entity_Promotion(entity=self.entity, pos=0, area='index_pop')
        ep.save()

        ep2 = Entity_Promotion.objects.filter(area='index_pop')[0]
        self.assertEqual(ep2.entity_id, self.entity.id)

    def test_entity_promotion_manager(self):
        ep = Entity_Promotion(entity=self.entity, pos=0, area='index_top')
        ep.save()

        ep1 = Entity_Promotion(entity=self.entity, pos=0, area='index_popular')
        ep1.save()

        self.assertEqual(Entity_Promotion.objects.index_top_entities()[0].id, ep.id)
        self.assertEqual(Entity_Promotion.objects.index_popular_entities()[0].id, ep1.id)





