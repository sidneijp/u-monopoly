from django.contrib import admin

from . import models


@admin.register(models.Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'times_to_run', 'number_of_players',
        'number_of_properties', 'max_turns', 'initial_account_balance', 'dice',
    )


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('simulation',)


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('match', 'order', 'behavior', 'account_balance',)
    ordering = ('match', 'order',)


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('match', 'order', 'rent_price', 'sale_price', )
    ordering = ('match', 'order', )


@admin.register(models.Turn)
class TurnAdmin(admin.ModelAdmin):
    list_display = ('player', 'dice', 'account_movement')


