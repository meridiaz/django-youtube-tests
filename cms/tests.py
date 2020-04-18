from django.test import TestCase
from . import views
from .ytchannel import YTChannel
from urllib.request import urlopen
# Create your tests here.

class TestYTChannel(TestCase):
    """Tests of YTChannel"""
    def setUp(self):
        self.simpleFile = url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' \
            + 'UC300utwSVAYOoRLEqmsprfg'

        self.expected = [{'link': 'https://www.youtube.com/watch?v=SPLwYv62-og',
                     'title': 'JSON práctico',
                     'id': 'SPLwYv62-og'},
                    {'link': 'https://www.youtube.com/watch?v=MyaRcqzBbk4',
                     'title': 'Django práctico: testing',
                     'id': 'MyaRcqzBbk4'},
                    {'link': 'https://www.youtube.com/watch?v=kmq_7G8YoS4',
                     'title': 'XML y Django practico: django-youtube-1',
                     'id': 'kmq_7G8YoS4'},
                    {'link': 'https://www.youtube.com/watch?v=WSPrhKPT3uQ',
                     'title': 'Frikiminutos: Contenedores por todas partes',
                     'id': 'WSPrhKPT3uQ'},
                    {'link': 'https://www.youtube.com/watch?v=xI8lDsJPsw0',
                     'title': 'Práctica: "Guión 4" Usuarios y ficheros estáticos en Django',
                     'id': 'xI8lDsJPsw0'},
                    {'link': 'https://www.youtube.com/watch?v=j3FwKACOARQ',
                     'title': 'Frikiminutos: Servidor web en producción',
                     'id': 'j3FwKACOARQ'}]

    def test_extraerXML(self):
        xmlFile = urlopen(self.simpleFile)
        channel = YTChannel(xmlFile)
        videos = channel.videos()
        self.assertEqual(videos[0:6], self.expected)

class TestViews(TestCase):
    def set_up(self):
        xmlFile = urlopen('https://www.youtube.com/feeds/videos.xml?channel_id=' \
            + 'UC300utwSVAYOoRLEqmsprfg')
        channel = YTChannel(xmlFile)
        
    def test_func_aux(self):
        self.assertEqual(True, views.negar(False))
        self.assertEqual(False, views.negar(True))

    def test_get_barra(self):
        checks = ["<h1>Lista de videos seleccionados:</h1>",
                  "<h1>Lista de videos seleccionables:</h1>"]
        response = self.client.get('/cms/')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_post_barra(self):
        check = '<button name="action" value=j3FwKACOARQ type = "submit">Eliminar</button>'
        response = self.client.post('/cms/', {'action': 'j3FwKACOARQ'})
        content = response.content.decode(encoding='UTF-8')
        self.assertInHTML(check, content)

    def test_get_content(self):
        response = self.client.get('/cms/j3FwKACOARQ')
        self.assertEqual(response.status_code, 404)
