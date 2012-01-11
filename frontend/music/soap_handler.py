# encoding: utf-8
from cStringIO import StringIO

from soaplib.core.server.wsgi import Application as WSGIApplication

from django.http import HttpResponse

class DjangoSOAPAdaptor(WSGIApplication):
    """
    Adaptor class for handling soaplib webservices
    """
    def __call__(self, request):
        """
        Process soap request
        """
        django_response = HttpResponse()
        def start_response(status, headers):
            status, _ = status.split(' ', 1)
            django_response.status_code = int(status)
            for header, value in headers:
                django_response[header] = value

        environ = request.META.copy()
        body = request.raw_post_data

        environ['CONTENT_LENGTH'] = len(body)
        environ['wsgi.input'] = StringIO(body)
        environ['wsgi.multithread'] = False

        response = super(DjangoSOAPAdaptor, self).__call__(environ, start_response)
        django_response.content = "\n".join(response)

        return django_response
