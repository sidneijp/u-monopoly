from collections import namedtuple
import random
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class Simulation(models.Model):
    DEFAULT_DICE_FACES = 6
    MIN_DICE_FACES = 2
    DEFAULT_TIMES_TO_RUN = 300
    MIN_TIMES_TO_RUN = 1
    MAX_TIMES_TO_RUN = 1000
    DEFAULT_NUMBER_OF_PROPERTIES = 20
    DEFAULT_NUMBER_OF_PLAYERS = 4
    MIN_NUMBER_OF_PLAYERS = 2
    DEFAULT_MAX_TURNS = 1000
    DEFAULT_INITIAL_ACCOUNT_BALANCE = Decimal('300.00')
    DEFAULT_BONUS = Decimal('100.00')
    number_of_properties = models.PositiveSmallIntegerField(
        _('number os properties'), default=DEFAULT_NUMBER_OF_PROPERTIES
    )
    number_of_players = models.PositiveSmallIntegerField(
        _('number os players'), default=DEFAULT_NUMBER_OF_PLAYERS
    )
    max_turns = models.PositiveSmallIntegerField(
        _('limit of turns'), default=DEFAULT_MAX_TURNS
    )
    initial_account_balance = models.DecimalField(
        _('initial player\'s account'), default=DEFAULT_INITIAL_ACCOUNT_BALANCE,
        max_digits=8, decimal_places=2
    )
    bonus = models.DecimalField(
        _('bonus'), default=DEFAULT_BONUS,
        max_digits=8, decimal_places=2
    )
    dice = models.PositiveSmallIntegerField(_('dice'), default=DEFAULT_DICE_FACES)
    times_to_run = models.PositiveSmallIntegerField(_('times to run'), default=DEFAULT_TIMES_TO_RUN)
    alias = models.CharField(_('alias'), max_length=80, blank=True)

    class Meta:
        verbose_name = _('Simulation muito loka')
        verbose_name_plural = _('Simulations muito lokas')

    def __str__(self):
        return f'{self.alias or self.pk}'

    def create_match(self):
        match = Match(simulation=self)
        match.save()
        return match


class SimulationOutcome(models.Model):
    simulation = models.OneToOneField(Simulation, on_delete=models.CASCADE, related_name='outcome')
    timed_out_matches = models.PositiveSmallIntegerField(_('time out matches'))
    average_turns = models.PositiveSmallIntegerField(_('average match turns'))
    impulsive_behavior = models.DecimalField(_('% impulsive behavior wins'), max_digits=5, decimal_places=2)
    picky_behavior = models.DecimalField(_('% picky behavior wins'), max_digits=5, decimal_places=2)
    conservative_behavior = models.DecimalField(_('% conservative behavior wins'), max_digits=5, decimal_places=2)
    random_behavior = models.DecimalField(_('% random behavior wins'), max_digits=5, decimal_places=2)

    BehaviorVictories = namedtuple('BehaviorVictories', ['behavior', 'victories'])

    class Meta:
        verbose_name = _('Simulation outcome')
        verbose_name_plural = _('Simulations outcomes')

    def __str__(self):
        return f'{self.simulation}'

    def winner_behavior(self):
        behaviors = [
            self.BehaviorVictories(
                behavior=Player.BehaviorChoices.IMPULSIVE.value, victories=self.impulsive_behavior),
            self.BehaviorVictories(
                behavior=Player.BehaviorChoices.PICKY.value, victories=self.picky_behavior),
            self.BehaviorVictories(
                behavior=Player.BehaviorChoices.CONSERVATIVE.value, victories=self.conservative_behavior),
            self.BehaviorVictories(
                behavior=Player.BehaviorChoices.RANDOM.value, victories=self.random_behavior),
        ]
        winner_behavior = max(behaviors, key=lambda behavior: behavior.victories)
        return winner_behavior.behavior


class Match(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')

    def __str__(self):
        return f'{self.pk}'

    def create_players(self):
        players = []
        behaviors_list = list(Player.BehaviorChoices)
        for order in range(self.simulation.number_of_players):
            behavior = behaviors_list[order % len(behaviors_list)]
            player = self.create_player(behavior=behavior, order=order)
            players.append(player)
        return players

    def create_player(self, *args, **kwargs):
        kwargs.update({
            'match': self,
        })
        player = Player.objects.create(**kwargs)
        player.account_balance = self.simulation.initial_account_balance
        return player

    def create_properties(self):
        from apps.core.factories import PropertyFactory
        properties = []
        _random_property = PropertyFactory.build()
        rent_price = Decimal(_random_property.rent_price)
        sale_price = Decimal(_random_property.sale_price)
        for order in range(self.simulation.number_of_properties):
            _property = self.create_property(order=order, rent_price=rent_price, sale_price=sale_price)
            properties.append(_property)
        return properties

    def create_property(self, *args, **kwargs):
        kwargs.update({
            'match': self,
        })
        return Property.objects.create(**kwargs)


class Player(models.Model):
    class BehaviorChoices(models.TextChoices):
        IMPULSIVE = 'impulsive', _('Impulsive')
        PICKY = 'picky', _('Picky')
        CONSERVATIVE = 'conservative', _('Conservative')
        RANDOM = 'random', _('Random')
    BEHAVIOR_METHODS = {}
    behavior = models.CharField(_('behavior'), max_length=12, choices=BehaviorChoices.choices)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=80)
    order = models.PositiveSmallIntegerField(_('order'))
    account_balance = Decimal('0')
    accumulated_position = -1

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['match', 'order'], name='player-match-order',
            ),
        ]
        verbose_name = _('Player')
        verbose_name_plural = _('Players')

    def __str__(self):
        return f'{self.get_behavior_display()}'

    def move(self, dice, board):
        self.accumulated_position += dice
        board_position = self.accumulated_position % len(board)
        return board[board_position]

    def earn_bonus(self):
        self.account_balance += self.match.simulation.bonus
        return self.match.simulation.bonus

    def is_able_to_buy(self, _property):
        return self.account_balance >= _property.sale_price

    def buy(self, _property):
        self.account_balance -= _property.sale_price
        _property.owner = self
        return _property.sale_price

    def should_buy(self, _property):
        behavior_method = self.get_behavior_method()
        return behavior_method(self, _property)

    def get_behavior_method(self):
        return self.BEHAVIOR_METHODS[self.behavior]

    def _impulsive_should_buy(self, _property):
        return True

    BEHAVIOR_METHODS[BehaviorChoices.IMPULSIVE.value] = _impulsive_should_buy

    def _picky_should_buy(self, _property):
        min_expected_rent_price = Decimal(50)
        return _property.rent_price > min_expected_rent_price

    BEHAVIOR_METHODS[BehaviorChoices.PICKY.value] = _picky_should_buy

    def _conservative_should_buy(self, _property):
        min_expected_account_balance_after_buy = Decimal(80)
        return (self.account_balance - _property.sale_price) >= min_expected_account_balance_after_buy

    BEHAVIOR_METHODS[BehaviorChoices.CONSERVATIVE.value] = _conservative_should_buy

    def _random_should_buy(self, _property):
        buy = True
        not_buy = False
        return random.choices([buy, not_buy])

    BEHAVIOR_METHODS[BehaviorChoices.RANDOM.value] = _random_should_buy


class Property(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    rent_price = models.DecimalField(_('rent price'), max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(_('sale price'), max_digits=8, decimal_places=2)
    order = models.PositiveSmallIntegerField(_('order'))
    owner = None

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['match', 'order'], name='property-match-order',
            ),
        ]
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')

    def __str__(self):
        return f'{self.order}'

    def is_first_property(self, board):
        return self == board[0]

    def has_owner(self):
        return bool(self.owner)

    def should_charge_rent(self, renter):
        return self.has_owner() and self.owner != renter

    def charge_rent(self, renter):
        renter.account_balance -= self.rent_price
        self.owner.account_balance += self.rent_price
        return self.rent_price


class Turn(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    dice = models.PositiveSmallIntegerField(_('dice result'))
    account_movement = models.DecimalField(_('account movement'), max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('Turn')
        verbose_name_plural = _('Turns')

    def __str__(self):
        return f'{self.dice}'

    @classmethod
    def save_turns(cls, turns):
        cls.objects.bulk_create(turns)
