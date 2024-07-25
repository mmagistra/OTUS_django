from .bag_class import Bag
from .player_class import Computer, Human


class Game:
    def __init__(self):
        num_of_players = int(input('type count of players\n'))
        if num_of_players < 2:
            raise "Number of players must be 2 or more"

        self.players = list()
        for i in range(num_of_players):
            if input(f'will player {i+1} be computer controlled? (y/n)\n') == 'y':
                self.players.append(Computer())
            else:
                self.players.append(Human())

        self.bag = Bag()

    def game_loop(self):
        continue_game = True
        win_players = []
        lose_players = []
        while continue_game:
            input('And next number is... (press ENTER, to continue)\n')
            barrel = self.bag.get_random_barrel()
            print(f'{barrel} is the next number!\n')

            for player in self.players:
                player_state = player.turn(barrel)  # can be 'win', 'lose' or 'in_game'
                if player_state == 'lose':
                    continue_game = False
                    lose_players.append(player)
                elif player_state == 'win':
                    continue_game = False
                    win_players.append(player)
                print('_'*26, '\n')

            if not continue_game:
                print('\n\n')
                for player in win_players:
                    print(f'{player} win this game!')

                for player in lose_players:
                    print(f'{player} lose this game!')

                break
