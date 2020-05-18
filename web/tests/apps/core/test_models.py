import pytest

from apps.core import models, factories


class TestDice:
    def setup(self):
        self.model = models.Dice
        self.model_factory = factories.DiceFactory
        self.instance = factories.DiceFactory.build()

    @pytest.mark.unittest
    @pytest.mark.skip
    @pytest.mark.parametrize('number_of_faces, expected', [
    ])
    def test_roll(self, number_of_faces, expected):
        assert self.instance.roll() == expected

    @pytest.mark.unittest
    @pytest.mark.skip
    @pytest.mark.parametrize('number_of_faces, expected', [
        [None, ''],
        [1, '1'],
        [0, '0'],
    ])
    def test_str(self, number_of_faces, expected):
        self.instance.number_of_faces = number_of_faces
        assert str(self.instance) == expected
