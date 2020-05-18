import factory.fuzzy

from apps.core import models


class SimulationFactory(factory.DjangoModelFactory):
    alias = factory.Faker('name')

    class Meta:
        model = models.Simulation


class MatchFactory(factory.DjangoModelFactory):
    simulation = factory.SubFactory(SimulationFactory)
    player_set = factory.RelatedFactoryList(
        'apps.core.factories.PlayerFactory', factory_related_name='match',
        size=2,
    )
    property_set = factory.RelatedFactoryList(
        'apps.core.factories.PropertyFactory', factory_related_name='match',
        size=2,
    )

    class Meta:
        model = models.Match


class PlayerFactory(factory.DjangoModelFactory):
    behavior = factory.fuzzy.FuzzyChoice(models.Player.TypeChoices)
    account_balance = factory.fuzzy.FuzzyDecimal(
        low=0, high=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE, precision=2
    )

    class Meta:
        model = models.Player


class PropertyFactory(factory.DjangoModelFactory):
    sale_price = factory.fuzzy.FuzzyDecimal(
        low=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE,
        high=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE * 3,
        precision=2
    )
    rent_price = factory.fuzzy.FuzzyDecimal(
        low=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE / 5,
        high=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE * 3 / 5,
        precision=2
    )

    class Meta:
        model = models.Property


class TurnFactory(factory.DjangoModelFactory):
    player = factory.SubFactory(PlayerFactory)
    dice = factory.fuzzy.FuzzyInteger(
        low=models.Simulation.MIN_DICE_FACES,
        high=models.Simulation.DEFAULT_DICE_FACES,
    )
    account_movement = factory.fuzzy.FuzzyDecimal(
        low=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE / 5,
        high=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE * 3,
        precision=2
    )

    class Meta:
        model = models.Turn
