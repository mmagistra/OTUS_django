class TestBarrel:
    def test_get_num(self, barrel_1):
        assert barrel_1.get_num() == 1

    def test_str(self, barrel_1):
        assert str(barrel_1) == '1'

    def test_repr(self, barrel_1):
        assert repr(barrel_1) == '1'

    def test_eq(self, barrel_1):
        assert barrel_1 == barrel_1
        assert barrel_1 is barrel_1
        assert not (barrel_1 == 1)

    def test_ne(self, barrel_1, barrel_2):
        assert barrel_1 != barrel_2
