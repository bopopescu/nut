from  django.db import models

class ShowEventBannerManager(models.Manager):
    def get_banner_urls_for_event(self, theEvent):
        banner_urls =[]
        showBanners = self.filter(event=theEvent)
        for theShowBanner in showBanners:
            banner_urls.append(theShowBanner.banner.image_url)
        return banner_urls