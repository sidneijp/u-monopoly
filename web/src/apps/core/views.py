from rest_framework import mixins, viewsets

from . import models, serializers, tasks


class SimulationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Simulation.objects.all()
    serializer_class = serializers.SimulationSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        tasks.run_simulation.delay(serializer.instance)
