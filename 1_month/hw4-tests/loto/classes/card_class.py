import random
from typing import Any

from .barrel_class import Barrel


class Card:
    def __init__(self, player_name):
        self.player_name = player_name
        remain_nums = list(range(1, 91))
        self.cells = []
        for _ in range(3):
            nums: list[int] = random.sample(remain_nums, k=5)
            for num in nums:
                remain_nums.remove(num)

            row: list[Any] = sorted(nums)
            for __ in range(4):
                row.insert(random.randint(0, len(row)), '  ')
            self.cells.append(row)

    def has_number(self, barrel: Barrel):
        num = barrel.get_num()
        for row in self.cells:
            if num in row:
                return True
        return False

    def cross_out_number(self, barrel: Barrel):
        num = barrel.get_num()
        for i, row in enumerate(self.cells):
            if num in row:
                self.cells[i][self.cells[i].index(num)] = '--'
                return True
        return False

    def is_card_cleared(self):
        if any([any(isinstance(el, int) for el in row) for row in self.cells]):
            return False
        return True

    def __str__(self):
        return (f'{f" Card of {self.player_name} ".center(26, "-")}\n'
                f'{" ".join([str(i).rjust(2, " ") for i in self.cells[0]])}\n'
                f'{" ".join([str(i).rjust(2, " ") for i in self.cells[1]])}\n'
                f'{" ".join([str(i).rjust(2, " ") for i in self.cells[2]])}\n'
                f'{"".center(26, "-")}')
