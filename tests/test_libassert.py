import textwrap

import pytest

from pytest_soft_asserts.libassert import SoftAssertions, Assert


class TestSoftAssert:

    def test_draw_results(self):
        # arrange
        ctx = SoftAssertions()
        ctx.assert_('(1 in [2, 2])\n', result=1 in [2, 2], condition='in', left=1, right=[2, 2])

        expected_result = textwrap.dedent(
            """
            +--------------------+-----------+---------------+-----------+
            |     expression     | condition | current value | expected  |
            +====================+===========+===============+===========+
            | assert 1 in [2, 2] | in        | 1             | in [2, 2] |
            +--------------------+-----------+---------------+-----------+
            """
        ).lower().strip()

        # act
        result = ctx.draw_results()

        # assert
        assert result == expected_result

    def test_is_failed(self):
        # arrange
        ctx = SoftAssertions()

        # act
        ctx.assert_('(1 in [2, 2])\n', result=1 in [2, 2], condition='in', left=1, right=[2, 2])

        # assert
        assert ctx.is_failed is True

    def test_ctx_manager(self):
        # act, assert
        with pytest.raises(AssertionError):
            with SoftAssertions() as ctx:
                ctx.assert_('(1 in [2, 2])\n', result=1 in [2, 2], condition='in', left=1, right=[2, 2])

    def test_assert_model(self):
        # arrange, act
        _assert = Assert(
            code='(1 in [2, 2])\n',
            result=1 in [2, 2],
            condition='in',
            left=1,
            right=[2, 2]
        )

        # assert
        assert _assert.left == 1
        assert _assert.right == [2, 2]
        assert _assert.code == '(1 in [2, 2])\n'
        assert _assert.result is False
        assert _assert.condition == 'in'
        assert _assert.is_failed is True
        assert _assert.left_only is False
        assert _assert.pretty_code == 'assert 1 in [2, 2]'
