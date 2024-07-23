from random import choice

from classes.barrel_class import Barrel


class Bag:
    def __init__(self):
        self.remain_barrels = list(range(1, 91))

    def get_random_barrel(self) -> Barrel:
        barrel_num = choice(self.remain_barrels)
        self.remain_barrels.remove(barrel_num)
        return Barrel(barrel_num)
