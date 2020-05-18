from decimal import Decimal

import factory.fuzzy

from apps.core import models


class PropertyFactory(factory.DjangoModelFactory):
    sale_price = factory.fuzzy.FuzzyDecimal(
        low=0,
        high=float(models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE),
        precision=2
    )
    rent_price = factory.fuzzy.FuzzyDecimal(
        low=0,
        high=float(models.Simulation.DEFAULT_INITIAL_ACCOUNT_BALANCE),
        precision=2
    )

    class Meta:
        model = models.Property
