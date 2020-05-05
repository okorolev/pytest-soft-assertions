class TestPlugin:

    def test_simple_table(self, testdir):
        func_source = """
            def test_kek():
                assert 1 == 2
                assert object is None
        """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        result.stdout.fnmatch_lines([
            'E           +-----------------------+-----------+------------------+----------+',
            'E           |      expression       | condition |  current value   | expected |',
            'E           +=======================+===========+==================+==========+',
            'E           | assert 1 == 2         | ==        | 1                | 2        |',
            'E           +-----------------------+-----------+------------------+----------+',
            "E           | assert object is None | is        | <class 'object'> | None     |",
            'E           +-----------------------+-----------+------------------+----------+',
        ])
        assert result.ret == 1

    def test_simple_table2(self, testdir):
        func_source = """
            def test_kek():
                assert 1 in [2, 2]
                assert 1 not in [1, 2]
        """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        result.stdout.fnmatch_lines([
            'E           +------------------------+-----------+---------------+---------------+',
            'E           |       expression       | condition | current value |   expected    |',
            'E           +========================+===========+===============+===============+',
            'E           | assert 1 in [2, 2]     | in        | 1             | in [2, 2]     |',
            'E           +------------------------+-----------+---------------+---------------+',
            'E           | assert 1 not in [1, 2] | not in    | 1             | not in [1, 2] |',
            'E           +------------------------+-----------+---------------+---------------+'
        ])
        assert result.ret == 1

    def test_simple_table3(self, testdir):
        func_source = """
            def test_kek():
                assert None or False
                assert not True
        """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        result.stdout.fnmatch_lines([
            'E           +----------------------+-----------+---------------+------------+',
            'E           |      expression      | condition | current value |  expected  |',
            'E           +======================+===========+===============+============+',
            'E           | assert None or False | or        | None          | <Not None> |',
            'E           +----------------------+-----------+---------------+------------+',
            "E           | assert not True      | not       | True          | <Not None> |",
            'E           +----------------------+-----------+---------------+------------+',
        ])
        assert result.ret == 1

    def test_simple_table4(self, testdir):
        func_source = """
            def test_kek():
                assert {}
                assert None
        """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        result.stdout.fnmatch_lines([
            'E           +-------------+-----------------+---------------+------------+',
            'E           | expression  |    condition    | current value |  expected  |',
            'E           +=============+=================+===============+============+',
            'E           | assert {}   | <Not condition> | {}            | <Not None> |',
            'E           +-------------+-----------------+---------------+------------+',
            "E           | assert None | <Not condition> | None          | <Not None> |",
            'E           +-------------+-----------------+---------------+------------+',
        ])
        assert result.ret == 1

    def test_simple_table5(self, testdir):
        func_source = """
            def test_kek():
                assert 1 > 1
                assert 1 < 1
                assert 1 >= 2
                assert 2 <= 1
                assert 1 != 1
        """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        result.stdout.fnmatch_lines([
            'E           +---------------+-----------+---------------+----------+',
            'E           |  expression   | condition | current value | expected |',
            'E           +===============+===========+===============+==========+',
            'E           | assert 1 > 1  | >         | 1             | > 1      |',
            'E           +---------------+-----------+---------------+----------+',
            "E           | assert 1 < 1  | <         | 1             | < 1      |",
            'E           +---------------+-----------+---------------+----------+',
            'E           | assert 1 >= 2 | >=        | 1             | >= 2     |',
            'E           +---------------+-----------+---------------+----------+',
            'E           | assert 2 <= 1 | <=        | 2             | <= 1     |',
            'E           +---------------+-----------+---------------+----------+',
            'E           | assert 1 != 1 | !=        | 1             | != 1     |',
            'E           +---------------+-----------+---------------+----------+',
        ])
        assert result.ret == 1

    def test_simple_table6(self, testdir):
        func_source = """
            def test_kek():
                assert None is not None
        """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        result.stdout.fnmatch_lines([
            'E           +-------------------------+-----------+---------------+-------------+',
            'E           |       expression        | condition | current value |  expected   |',
            'E           +=========================+===========+===============+=============+',
            'E           | assert None is not None | is not    | None          | is not None |',
            'E           +-------------------------+-----------+---------------+-------------+',
        ])
        assert result.ret == 1

    def test_simple_support_reassigned_vars(self, testdir):
        func_source = """
            def test_kek():
                a = 1
                assert a > 2

                a = 2
                assert a > 3
        """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        result.stdout.fnmatch_lines([
            'E           +--------------+-----------+---------------+----------+',
            'E           |  expression  | condition | current value | expected |',
            'E           +==============+===========+===============+==========+',
            'E           | assert a > 2 | >         | 1             | > 2      |',
            'E           +--------------+-----------+---------------+----------+',
            'E           | assert a > 3 | >         | 2             | > 3      |',
            'E           +--------------+-----------+---------------+----------+'
        ])
        assert result.ret == 1

    def test_simple_support_cycles(self, testdir):
        func_source = """
            def test_kek():
                for x in range(3):
                    assert x < 0
        """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        result.stdout.fnmatch_lines([
            'E           +--------------+-----------+---------------+----------+',
            'E           |  expression  | condition | current value | expected |',
            'E           +==============+===========+===============+==========+',
            'E           | assert x < 0 | <         | 0             | < 0      |',
            'E           +--------------+-----------+---------------+----------+',
            'E           | assert x < 0 | <         | 1             | < 0      |',
            'E           +--------------+-----------+---------------+----------+',
            'E           | assert x < 0 | <         | 2             | < 0      |',
            'E           +--------------+-----------+---------------+----------+'
        ])
        assert result.ret == 1

    def test_simple_support_cycles__while(self, testdir):
        func_source = """
            def test_kek():
                a = [1, 2, 3]
                while a:
                    x = a.pop()
                    assert x > 4
        """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        result.stdout.fnmatch_lines([
            'E           +--------------+-----------+---------------+----------+',
            'E           |  expression  | condition | current value | expected |',
            'E           +==============+===========+===============+==========+',
            'E           | assert x > 4 | >         | 3             | > 4      |',
            'E           +--------------+-----------+---------------+----------+',
            'E           | assert x > 4 | >         | 2             | > 4      |',
            'E           +--------------+-----------+---------------+----------+',
            'E           | assert x > 4 | >         | 1             | > 4      |',
            'E           +--------------+-----------+---------------+----------+'
        ])
        assert result.ret == 1
