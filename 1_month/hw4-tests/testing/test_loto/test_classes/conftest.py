from pytest import fixture
from loto.classes.bag_class import Bag
from loto.classes.barrel_class import Barrel
from loto.classes.card_class import Card
from loto.classes.player_class import Player, Human, Computer


@fixture
def bag():
    return Bag()


@fixture
def barrel_1():
    return Barrel(1)


@fixture
def barrel_2():
    return Barrel(2)


@fixture
def card():
    return Card('Alan')


@fixture
def player(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Alan")
    return Player()


@fixture
def human(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Alan")
    return Human()


@fixture
def computer(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Alan")
    return Computer()
