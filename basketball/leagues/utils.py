import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic import View

class JSONHttpResponse(HttpResponse):
    def __init__(self, content=None, *args, **kwargs):
        kwargs['content_type'] = 'application/json'
        content = json.dumps(content, cls=DjangoJSONEncoder)
        super(JSONHttpResponse, self).__init__(content, *args, **kwargs)


class JSONView(View):

    def dispatch(self, request, *args, **kwargs):
        data = super(JSONView, self).dispatch(request, *args, **kwargs)

        if settings.DEBUG and getattr(settings, 'DEBUG_TOOLBAR_ENABLED', False) \
                and request.GET.get('debug', "false").lower() in ('yes', '1', 'true'):
            return HttpResponse("<http><body><h1>DEBUG TOOLBAR STUFF</h1></body></http>")

        if isinstance(data, HttpResponse):
            return data
        else:
            return JSONHttpResponse(data)
