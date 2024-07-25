from loto.classes.bag_class import Bag


class TestBag:
    def test_get_random_barrel(self, bag):
        barrels = set()
        for _ in range(90):
            barrels.add(bag.get_random_barrel())
        assert len(barrels) == 90
        assert bag.get_random_barrel().get_num() == -1
