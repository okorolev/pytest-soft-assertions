class TestShowAssertsTable:

    def test_table(self):
        value = -1
        assert value == 1
        assert 1 == 2
        assert 'Kek' is None
        assert object is None
        assert None is not None
        assert 1 is None

        assert 1 in [2, 2]
        assert 1 not in [1, 2]
        orders = [1, 2, 3]
        assert 4 in orders

        assert None or False
        assert not True

        assert {}
        assert None

        assert 1 > 1
        assert 1 < 1
        assert 1 >= 2
        assert 2 <= 1
        assert 1 != 1
