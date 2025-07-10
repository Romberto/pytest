import pytest
from contextlib import nullcontext as does_not_raise

from src.main import Calculator

class TestCalculator:
    @pytest.mark.parametrize(
        'x, y, res, expected',[
            (10, 2, 5, does_not_raise()),
            (5, 2, 2.5, does_not_raise()),
            (25, 5, 5, does_not_raise()),
            (20,0,20, pytest.raises(ZeroDivisionError)),
             (20, "-4", 0, pytest.raises(TypeError))
        ]
    )
    def test_devide(self, x, y, res, expected):
        with expected:
            assert Calculator().devide(x, y) == res

