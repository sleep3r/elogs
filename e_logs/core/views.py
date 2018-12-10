from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden


class LoginRequired(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
