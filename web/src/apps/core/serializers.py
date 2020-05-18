from rest_framework import serializers

from . import models


class SimulationOutcomeSerializer(serializers.ModelSerializer):
    winner_behavior = serializers.CharField()

    class Meta:
        model = models.SimulationOutcome
        fields = [
            'simulation', 'timed_out_matches', 'average_turns', 'winner_behavior',
            'impulsive_behavior', 'picky_behavior', 'conservative_behavior', 'random_behavior',
        ]


class SimulationSerializer(serializers.HyperlinkedModelSerializer):
    outcome = SimulationOutcomeSerializer(read_only=True)

    class Meta:
        model = models.Simulation
        fields = [
            'url', 'times_to_run', 'max_turns', 'number_of_properties', 'number_of_players',
            'initial_account_balance', 'bonus', 'dice', 'outcome',
        ]
