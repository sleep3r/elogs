from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Setting
from .serializers import SettingSerializer


class SettingsList(generics.ListAPIView):
    serializer_class = SettingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Setting.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'journals__name')


class SettingAPI(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = SettingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Setting.objects.all()