from cacheops import cached_as
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from e_logs.common.all_journals_app.models import Plant, Journal, Table, Field, Cell, Shift
from .serializers import PlantSerializer, JournalSerializer, TableSerializer, FieldSerializer, \
    CellSerializer, ShiftSerializer


class ShiftsList(generics.ListAPIView):
    serializer_class = ShiftSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Shift.objects.all()
    filter_backends = (DjangoFilterBackend,)


class ShiftAPI(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = ShiftSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Shift.objects\
        .select_related('journal', 'journal__plant') \
        .prefetch_related('journal__plant', 'journal', 'cells', 'cells__field', 'journal__tables')\
        .all()


shift_api_view = ShiftAPI.as_view()


class PlantsList(generics.ListAPIView):
    serializer_class = PlantSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Plant.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name',)


class PlantAPI(generics.RetrieveAPIView):
    lookup_field = 'name'
    serializer_class = PlantSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Plant.objects.all()


class JournalsList(generics.ListAPIView):
    serializer_class = JournalSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Journal.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('plant__name', 'type', 'name')


class JournalAPI(generics.RetrieveAPIView):
    lookup_field = 'name'
    serializer_class = JournalSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Journal.objects.all()


class ShiftList(generics.ListAPIView):
    serializer_class = ShiftSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Shift.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('date', 'order')


class TablesList(generics.ListAPIView):
    serializer_class = TableSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Table.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('journal__plant__name', 'journal__name', 'name')


class TableAPI(generics.RetrieveAPIView):
    lookup_field = 'name'
    serializer_class = TableSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Table.objects.all()


class FieldsList(generics.ListAPIView):
    serializer_class = FieldSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Field.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('table__journal__plant__name', 'table__journal__name', 'table__name', 'name',)


class FieldAPI(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = FieldSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Field.objects.all()


class CellsList(generics.ListAPIView):
    serializer_class = CellSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Cell.objects.all()

    def post(self, request):
        return Response({"detail": "Hello, !"}, status=status.HTTP_200_OK)

    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = (
    #     'field__table__journal__plant__name', 'field__table__journal__name', 'field__table__name',
    #     'field__name', 'group_id')


class CellAPI(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = CellSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Cell.objects.all()
