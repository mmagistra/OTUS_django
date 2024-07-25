import pytest

from loto.classes.barrel_class import Barrel
from loto.classes.card_class import Card


class TestCard:
    @pytest.mark.parametrize(
        "row_num",
        [0, 1, 2]
    )
    def test_init_by_rows(self, row_num):
        card = Card('Alan')
        assert len(card.cells[row_num]) == 9
        assert card.cells[row_num].count('  ') == 4

        row = card.cells[row_num]
        for _ in range(4):
            row.remove('  ')
        assert row == sorted(row)

    def test_init_by_col(self, card):
        assert len(card.cells) == 3

    def test_has_number(self, card):
        count_of_numbers = 0
        for num in range(1, 91):
            if card.has_number(Barrel(num)):
                count_of_numbers += 1

        assert count_of_numbers == 15

    @pytest.mark.parametrize(
        "barrel",
        [Barrel(i) for i in range(1, 91)]
    )
    def test_cross_out_number(self, barrel, card):
        assert card.has_number(barrel) == card.cross_out_number(barrel)

    def test_is_card_cleared(self, card):
        assert card.is_card_cleared() is False
        for i in range(1, 91):
            barrel = Barrel(i)
            card.cross_out_number(barrel)
        assert card.is_card_cleared() is True

    def test_str(self, card):
        assert isinstance(str(card), str)
