from rest_framework import serializers

from . import models


class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Simulation
        fields = [
            'times_to_run', 'max_turns', 'number_of_properties', 'number_of_players',
            'initial_account_balance', 'bonus', 'dice'
        ]
