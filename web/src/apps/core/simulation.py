import random

from . import models


class Dice:
    MIN_FACES = 2

    def __init__(self, faces, min_faces=2):
        self.faces = faces
        self.min_faces = min_faces

    def roll(self):
        return random.randint(self.MIN_FACES, self.faces)


class SimulationRunner:
    def __init__(self, simulation):
        self.simulation = simulation
        self.games = []

    def run(self, *args, **kwargs):
        self.setup()
        for game in self.games:
            game.run()
        self.shutdown()

    def setup(self):
        for _ in range(self.simulation.times_to_run):
            self.setup_game()

    def setup_game(self):
        match = self.simulation.create_match()
        players = match.create_players()
        properties = match.create_properties()
        game = Game(
            dice=Dice(self.simulation.dice),
            players=players, board=properties,
            max_turns=self.simulation.max_turns
        )
        self.games.append(game)

    def shutdown(self):
        self.save_simulation_outcome()

    def save_simulation_outcome(self):
        models.SimulationOutcome.objects.create(
            simulation=self.simulation,
            timed_out_matches=self.get_total_of_timed_out_matches(),
            average_turns=self.get_average_turns(),
            impulsive_behavior=self.get_behavior_victories_percentage(models.Player.BehaviorChoices.IMPULSIVE),
            picky_behavior=self.get_behavior_victories_percentage(models.Player.BehaviorChoices.PICKY),
            conservative_behavior=self.get_behavior_victories_percentage(models.Player.BehaviorChoices.CONSERVATIVE),
            random_behavior=self.get_behavior_victories_percentage(models.Player.BehaviorChoices.RANDOM),
        )

    def get_total_of_timed_out_matches(self):
        timed_out_matches = [game for game in self.games if game.has_timed_out()]
        return len(timed_out_matches)

    def get_average_turns(self):
        total_of_turns = sum([len(game.turns) for game in self.games])
        total_of_games = len(self.games)
        return total_of_turns / total_of_games

    def get_behavior_victories_percentage(self, behavior):
        behavior = behavior.value
        behavior_victories = [game for game in self.games if game.winner.behavior == behavior]
        behavior_victories = len(behavior_victories)
        total_of_games = len(self.games)
        return behavior_victories / total_of_games * 100


class Game:
    def __init__(self, dice, players, board, max_turns):
        self.dice = dice
        self.players = players
        self.board = board
        self.max_turns = max_turns
        self.turns = []
        self.finished = False
        self.winner = None
        self.last_player = None
        self.player = None
        self.player_sequence = None

    def run(self, *args, **kwargs):
        self.setup()
        while not self.has_finished():
            self.update()
        self.shutdown()

    def setup(self):
        self.player_sequence = self.get_player_sequence()

    def has_finished(self):
        return self.finished

    def update(self):
        turn = self.create_turn()
        self.player = self.get_next_player()
        turn.player = self.player
        turn.dice = self.dice.roll()
        _property = self.player.move(turn.dice, self.board)

        if _property.is_first_property(self.board):
            turn.account_movement += self.player.earn_bonus()

        if _property.should_charge_rent(self.player):
            turn.account_movement -= _property.charge_rent(self.player)
        elif self.player.is_able_to_buy(_property) and self.player.should_buy(_property):
            turn.account_movement -= self.player.buy(_property)

        if self.should_finish_game():
            self.finish_game()

    def get_next_player(self):
        try:
            return next(self.player_sequence)
        except (StopIteration, TypeError,):
            self.player_sequence = self.get_player_sequence()

    def get_player_sequence(self):
        players = self.players.copy()
        while players:
            player = players.pop(0)
            if player and player.account_balance >= 0:
                yield player
                self.last_player = player
            players.append(player)

    def create_turn(self):
        turn = models.Turn()
        self.turns.append(turn)
        return turn

    def should_finish_game(self):
        return self.player == self.last_player or self.has_timed_out()

    def has_timed_out(self):
        return len(self.turns) >= self.max_turns

    def finish_game(self):
        self.finished = True

    def shutdown(self):
        self.decide_winner()
        self.save_turns()

    def decide_winner(self):
        for player in self.players:
            if self.winner is None or player.account_balance > self.winner.account_balance:
                self.winner = player
        return self.winner

    def save_turns(self):
        models.Turn.save_turns(self.turns)
