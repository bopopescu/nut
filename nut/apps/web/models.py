from apps.core.models import Entity


class WebEntity(Entity):
    class Meta:
        proxy = True
