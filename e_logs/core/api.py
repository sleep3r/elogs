from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer, AdminRenderer, BrowsableAPIRenderer


class CustomRendererView:
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @property
    def renderer_classes(self):
        renderers = super().renderer_classes

        if not self.request.user.is_staff:
            renderers = [JSONRenderer,]

        return renderers