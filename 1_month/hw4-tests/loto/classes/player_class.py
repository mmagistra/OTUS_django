from .card_class import Card


class Player:
    def __init__(self):
        self.name = input('Type name for this player\n')
        self.card = Card(self.name)

    def __str__(self):
        return f"Player {self.name}"


class Human(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Human'

    def turn(self, barrel) -> str:
        print(self.card)
        player_action = input(f'Do you want cross out number {barrel}? (y/n) ')
        if player_action == 'y':
            is_number_crossed_out = self.card.cross_out_number(barrel)
            if is_number_crossed_out:
                if self.card.is_card_cleared():
                    return 'win'
                return 'in_game'
            return 'lose'
        else:
            is_number_in_card = self.card.has_number(barrel)
            if is_number_in_card:
                return 'lose'
            return 'in_game'


class Computer(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Computer'

    def turn(self, barrel):
        print(self.card)
        if self.card.has_number(barrel):
            print(f'player {self.name} cross out {barrel}')
            is_number_crossed_out = self.card.cross_out_number(barrel)
            if is_number_crossed_out:
                if self.card.is_card_cleared():
                    return 'win'
                return 'in_game'
        print(f'player {self.name} skip {barrel}')
        return 'in_game'
