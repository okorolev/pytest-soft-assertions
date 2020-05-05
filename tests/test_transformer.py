class TestTransformer:

    def test_no_asserts(self, testdir):
        func_source = """
                def test_kek():
                    pass
            """
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--soft-asserts')

        assert result.ret == 0
