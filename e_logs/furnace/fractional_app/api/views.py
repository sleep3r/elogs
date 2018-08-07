from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from e_logs.core.api import CustomRendererView
from e_logs.furnace.fractional_app.api.serializers import MeasurementSerializer, MeasurementGraphsSerializer
from e_logs.common.all_journals_app.models import Cell, Measurement


class MeasurementAPI(CustomRendererView, generics.ListAPIView):
    serializer_class = MeasurementSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @staticmethod
    def get_queryset(qs=Measurement.objects.only('id', 'time').all().order_by('-time')):
        list = [
        {'id': m.id,
         'time': m.time,
         'cinder_masses':[float(c.value) for c in Cell.objects.only('value').filter(field_name='cinder_mass', group=m)],
         'schieht_masses':[float(c.value) for c in Cell.objects.only('value').filter(field_name='schieht_mass', group=m)],
         'cinder_sizes':[float(c.value) for c in Cell.objects.only('value').filter(field_name='cinder_size', group=m)],
         'schieht_sizes':[float(c.value) for c in Cell.objects.only('value').filter(field_name='schieht_size', group=m)],
        } for m in qs ]

        return list

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MeasurementRUD(CustomRendererView, generics.DestroyAPIView):
    lookup_field = 'id'
    serializer_class = MeasurementSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurement.objects.only('id', 'time')

    def get(self, request, id):
        obj = MeasurementAPI.get_queryset(qs=self.queryset.filter(id=id))
        if len(obj) != 0:
            serializer = self.get_serializer(data=obj[0])
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail":"Not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Measurement.objects.get(id=id)
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.data)

        return Response(serializer.data)

class MeasurementGraphs(CustomRendererView, generics.GenericAPIView):
    serializer_class = MeasurementGraphsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def get_queryset(self):
        def get_mean(masses, sizes):
            msum = sum(masses)
            if msum == 0:
                return 0

            mass_parts = [m / msum for m in masses]
            sizes = sizes + [sizes[-1]]
            middles = [(sizes[i] + sizes[i + 1]) / 2 for i in range(len(sizes) - 1)]
            res = [float(mas) * float(mid) for mas, mid in zip(mass_parts, middles)]
            return sum(res)

        cinders = []
        schieht = []

        for measurement in Measurement.objects.only('id', 'time').all().order_by('-time'):
            masses = [float(m.value) for m in Cell.objects.filter(field_name="cinder_mass", group=measurement)]
            min_sizes = [float(m.value) for m in Cell.objects.filter(field_name="cinder_size", group=measurement)]
            cinders.append([measurement.time.timestamp(), get_mean(masses, min_sizes)])

            masses = [float(m.value) for m in Cell.objects.filter(field_name="schieht_mass", group=measurement)]
            min_sizes = [float(m.value) for m in Cell.objects.filter(field_name="schieht_size", group=measurement)]
            schieht.append([measurement.time.timestamp(), get_mean(masses, min_sizes)])

        res = dict()
        res['cinder'] = cinders
        res['schieht'] = schieht

        return res

    def get(self, request):
        serializer = self.get_serializer(data=self.get_queryset())
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)