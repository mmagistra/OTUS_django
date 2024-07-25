import pytest

from loto.classes.barrel_class import Barrel


class TestPlayer:
    def test_init(self, player):
        assert player.name == 'Alan'

    def test_str(self, player):
        assert str(player) == "Player Alan"


class TestHuman:
    def test_init(self, human):
        assert human.type == 'Human'

    def test_turn(self, human, monkeypatch):
        for i in range(1, 91):
            barrel = Barrel(i)
            monkeypatch.setattr('builtins.print', lambda _: None)
            if human.card.has_number(barrel):
                monkeypatch.setattr('builtins.input', lambda _: "n")
                assert human.turn(barrel) == 'lose'

                monkeypatch.setattr('builtins.input', lambda _: "y")
                count_of_nums = 0
                for cells in human.card.cells:
                    for cell in cells:
                        if count_of_nums >= 2:
                            break
                        if isinstance(cell, int):
                            count_of_nums += 1
                    if count_of_nums >= 2:
                        break

                assert count_of_nums >= 1
                if count_of_nums == 1:
                    assert human.turn(barrel) == 'win'
                else:
                    assert human.turn(barrel) == 'in_game'
            else:
                monkeypatch.setattr('builtins.input', lambda _: "y")
                assert human.turn(barrel) == 'lose'

                monkeypatch.setattr('builtins.input', lambda _: "n")
                assert human.turn(barrel) == 'in_game'


class TestComputer:
    def test_init(self, computer):
        assert computer.type == 'Computer'

    def test_turn(self, computer, monkeypatch):
        for i in range(1, 91):
            barrel = Barrel(i)
            monkeypatch.setattr('builtins.print', lambda _: None)
            if computer.card.has_number(barrel):
                count_of_nums = 0
                for cells in computer.card.cells:
                    for cell in cells:
                        if count_of_nums >= 2:
                            break
                        if isinstance(cell, int):
                            count_of_nums += 1
                    if count_of_nums >= 2:
                        break

                assert count_of_nums >= 1
                if count_of_nums == 1:
                    assert computer.turn(barrel) == 'win'
                else:
                    assert computer.turn(barrel) == 'in_game'
            else:
                assert computer.turn(barrel) == 'in_game'
