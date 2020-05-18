from django.db import models
from django.utils.translation import gettext_lazy as _


class Dice(models.Model):
    DEFAULT_NUMBER_OF_FACES = 6
    MIN_NUMBER_OF_FACES = 2
    number_of_faces = models.PositiveSmallIntegerField(
        _('Number of faces'), default=DEFAULT_NUMBER_OF_FACES
    )

    class Meta:
        verbose_name = _('Dice')
        verbose_name_plural = _('Dices')

    def __str__(self):
        return f'{self.number_of_faces}'


class Simulation(models.Model):
    DEFAULT_TIMES_TO_RUN = 300
    MIN_TIMES_TO_RUN = 1
    MAX_TIMES_TO_RUN = 1000
    DEFAULT_NUMBER_OF_PROPERTIES = 20
    DEFAULT_NUMBER_OF_PLAYERS = 4
    MIN_NUMBER_OF_PLAYERS = 2
    DEFAULT_MAX_TURNS = 1000
    DEFAULT_INITIAL_ACCOUNT_BALANCE = 300.0
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
    dice = models.ForeignKey(Dice, on_delete=models.CASCADE)
    times_to_run = models.PositiveSmallIntegerField(_('times to run'), default=DEFAULT_TIMES_TO_RUN)
    alias = models.CharField(_('alias'), max_length=80, blank=True)

    class Meta:
        verbose_name = _('Simulation')
        verbose_name_plural = _('Simulations')

    def __str__(self):
        return f'{self.alias or self.pk}'


class Match(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')

    def __str__(self):
        return f'{self.pk}'


class Player(models.Model):
    class TypeChoices(models.TextChoices):
        IMPULSIVE = 'impulsive', _('Impulsive')
        PICKY = 'picky', _('Picky')
        CONSERVATIVE = 'conservative', _('Conservative')
        RANDOM = 'random', _('Random')
    behavior = models.CharField(_('behavior'), max_length=12, choices=TypeChoices.choices)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=80)
    account_balance = models.DecimalField(
        _('account'),
        max_digits=8, decimal_places=2
    )
    order = models.PositiveSmallIntegerField(_('order'))
    is_winner = models.NullBooleanField(_('Winner'), default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['match', 'order'], name='player-match-order',
            ),
        ]
        verbose_name = _('Player')
        verbose_name_plural = _('Players')

    def __str__(self):
        return f'{self.name} ({self.get_behavior_display()})'


class Property(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_('name'), max_length=80)
    rent_price = models.DecimalField(_('rent price'), max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(_('sale price'), max_digits=8, decimal_places=2)
    order = models.PositiveSmallIntegerField(_('order'))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['match', 'order'], name='property-match-order',
            ),
        ]
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')

    def __str__(self):
        return f'{self.name}'


class Turn(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    dice_result = models.PositiveSmallIntegerField(_('dice result'))

    class Meta:
        verbose_name = _('Turn')
        verbose_name_plural = _('Turns')

    def __str__(self):
        return f'{self.dice_result}'


class TurnAccountMovement(models.Model):
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    value = models.DecimalField(_('account movement'), max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = _('Turn account movement')
        verbose_name_plural = _('Turns account movements')

    def __str__(self):
        return f'{self.turn} - {self.value}'
