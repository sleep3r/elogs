from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from e_logs.common.all_journals_app.ws.consumers import CommonConsumer
from e_logs.core.middleware import TokenAuthMiddleware

ASGI_APPLICATION = "config.asgi.application"

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                [
                    url(r"^e-logs/$", CommonConsumer),
                ]
            )
        )
    )
})
