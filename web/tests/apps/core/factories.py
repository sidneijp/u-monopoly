import factory.fuzzy

from apps.core import models

NULL_BOOLEAN_VALUES = (True, False, None,)


class DiceFactory(factory.DjangoModelFactory):
    number_of_faces = factory.fuzzy.FuzzyInteger(
        low=models.Dice.MIN_NUMBER_OF_FACES,
        high=models.Dice.DEFAULT_NUMBER_OF_FACES
    )

    class Meta:
        model = models.Dice


class SimulationFactory(factory.DjangoModelFactory):
    number_of_properties = factory.fuzzy.FuzzyInteger(
        low=models.Simulation.MIN_NUMBER_OF_PLAYERS,
        high=models.Simulation.DEFAULT_NUMBER_OF_PROPERTIES
    )
    number_of_players = factory.fuzzy.FuzzyInteger(
        low=models.Simulation.MIN_NUMBER_OF_PLAYERS,
        high=models.Simulation.DEFAULT_NUMBER_OF_PLAYERS
    )
    max_turns = factory.fuzzy.FuzzyInteger(
        low=models.Simulation.MIN_NUMBER_OF_PLAYERS,
        high=models.Simulation.DEFAULT_MAX_TURNS
    )
    initial_account_balance = factory.fuzzy.FuzzyDecimal(
        low=0, high=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE, precision=2
    )
    times_to_run = factory.fuzzy.FuzzyInteger(
        low=models.Simulation.MIN_TIMES_TO_RUN,
        high=models.Simulation.MAX_TIMES_TO_RUN
    )
    dice = factory.SubFactory(DiceFactory)
    alias = factory.Faker('name')

    match_set = factory.RelatedFactoryList(
        'tests.apps.core.factories.MatchFactory', factory_related_name='simulation',
        size=times_to_run.fuzz,
    )

    class Meta:
        model = models.Simulation


class MatchFactory(factory.DjangoModelFactory):
    simulation = factory.SubFactory(SimulationFactory)
    player_set = factory.RelatedFactoryList(
        'tests.apps.core.factories.PlayerFactory', factory_related_name='match',
        size=2,
    )
    property_set = factory.RelatedFactoryList(
        'tests.apps.core.factories.PropertyFactory', factory_related_name='match',
        size=2,
    )

    class Meta:
        model = models.Match


class PlayerFactory(factory.DjangoModelFactory):
    behavior = factory.fuzzy.FuzzyChoice(models.Player.TypeChoices)
    match = factory.SubFactory(MatchFactory)
    account_balance = factory.fuzzy.FuzzyDecimal(
        low=0, high=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE, precision=2
    )
    name = factory.Faker('name')
    is_winner = factory.fuzzy.FuzzyChoice(NULL_BOOLEAN_VALUES)

    @factory.lazy_attribute_sequence
    def order(self, n):
        return n

    class Meta:
        model = models.Player


class PropertyFactory(factory.DjangoModelFactory):
    match = factory.SubFactory(MatchFactory)
    name = factory.Faker('street_address')
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

    @factory.lazy_attribute_sequence
    def order(self, n):
        return n

    class Meta:
        model = models.Property


class TurnFactory(factory.DjangoModelFactory):
    match = factory.SubFactory(MatchFactory)
    player = factory.SubFactory(PlayerFactory)
    property = factory.SubFactory(PropertyFactory)
    dice_result = factory.fuzzy.FuzzyInteger(
        low=models.Dice.MIN_NUMBER_OF_FACES,
        high=models.Dice.DEFAULT_NUMBER_OF_FACES,
    )

    class Meta:
        model = models.Turn


class TurnAccountMovementFactory(factory.DjangoModelFactory):
    turn = factory.SubFactory(TurnFactory)
    val = factory.SubFactory(PlayerFactory)
    property = factory.SubFactory(PropertyFactory)
    value = factory.fuzzy.FuzzyDecimal(
        low=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE / 5,
        high=models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE * 3,
        precision=2
    )

    class Meta:
        model = models.TurnAccountMovement
