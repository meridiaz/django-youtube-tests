from django.apps import AppConfig
import sys
from urllib.request import urlopen
from .ytchannel import YTChannel

seguir = True


def deleteDB():
    from .models import Video, CanalYT
    if Video.objects.count() != 0:
        CanalYT.objects.all().delete()


class CmsConfig(AppConfig):
    name = 'cms'

    def ready(self):
        from .models import Video
        global seguir
        if 'runserver' in sys.argv and seguir:
            url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' \
                + 'UC300utwSVAYOoRLEqmsprfg'
            print("---------------------valor de url:"+url)
            deleteDB()
            xmlStream = urlopen(url)
            canal = YTChannel(xmlStream)
            videos = canal.videos()
            seguir = False
