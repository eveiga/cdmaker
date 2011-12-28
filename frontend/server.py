import os
from wsgiref.simple_server import make_server
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler


os.environ['DJANGO_SETTINGS_MODULE']='settings'

httpd = make_server('', 8000, AdminMediaHandler(WSGIHandler()))
httpd.serve_forever()
