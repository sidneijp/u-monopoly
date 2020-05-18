from rest_framework import viewsets

from . import models, serializers, tasks


class SimulationViewSet(viewsets.ModelViewSet):
    queryset = models.Simulation.objects.all()
    serializer_class = serializers.SimulationSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        tasks.run_simulation.delay(serializer.instance)
