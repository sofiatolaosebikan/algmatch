import pytest

from algmatch.abstractClasses.stabilityType import StabilityType


class TestStabilityTypeEnum:
    def test_enum_values(self):
        assert StabilityType.STRONG.value == "strong"
        assert StabilityType.SUPER.value == "super"
        assert StabilityType.WEAK.value == "weak"

    @pytest.mark.parametrize("value", ["STRONG", "strong"])
    def test_from_value_strong(self, value):
        assert StabilityType.from_value(value) == StabilityType.STRONG

    @pytest.mark.parametrize("value", ["SUPER", "super"])
    def test_from_value_super(self, value):
        assert StabilityType.from_value(value) == StabilityType.SUPER

    @pytest.mark.parametrize("value", ["WEAK", "weak"])
    def test_from_value_weak(self, value):
        assert StabilityType.from_value(value) == StabilityType.WEAK

    @pytest.mark.parametrize("value", ["abcde", ""])
    def test_from_value_throws(self, value):
        with pytest.raises(ValueError):
            StabilityType.from_value(value)
