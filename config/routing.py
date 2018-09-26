from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from e_logs.common.all_journals_app.ws.consumers import CommonConsumer


ASGI_APPLICATION = "config.asgi.application"

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^e-logs/$", CommonConsumer),
                ]
            )
        )
    )
})
