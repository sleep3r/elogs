from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view


@csrf_exempt
def constructor_proxy(request, path):
    remoteurl = 'http://localhost:3000/' + path
    return proxy_view(request, remoteurl)
