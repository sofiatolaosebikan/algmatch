import pytest

from algmatch.abstractClasses.abstractPreferenceInstance import (
    AbstractPreferenceInstance,
)
from algmatch.errors.InstanceSetupErrors import (
    PrefRepError,
    PrefNotFoundError,
)


class DummyPreferenceInstance(AbstractPreferenceInstance):
    def _load(self, source):
        pass

    def check_preference_lists(self):
        pass

    def set_up_rankings(self):
        pass


@pytest.fixture
def instance():
    return DummyPreferenceInstance(source=None)


@pytest.fixture
def targets():
    return {"X", "Y"}


class TestAbstractPreferenceInstance:
    class TestCleanUnacceptablePairs:
        def test_clean_unacceptable_pairs(self, instance):
            a_side = {
                "A": {"list": ["X", "Y"]},
                "B": {"list": ["X", "Y"]},
            }
            b_side = {
                "X": {"list": ["A"]},
                "Y": {"list": ["B"]},
                "Z": {"list": ["A", "B"]},
            }

            instance.clean_unacceptable_pairs(a_side, b_side)

            assert a_side["A"]["list"] == ["X"]
            assert a_side["B"]["list"] == ["Y"]
            assert b_side["X"]["list"] == ["A"]
            assert b_side["Y"]["list"] == ["B"]
            assert b_side["Z"]["list"] == []

    class TestCheckPreferences:
        def test_valid(self, instance, targets):
            group = {"A": {"list": ["X", "Y"]}}

            instance.check_preferences_single_group(group, "entity", targets)

        def test_single_group_duplicate(self, instance, targets):
            group = {"A": {"list": ["X", "X"]}}

            with pytest.raises(PrefRepError):
                instance.check_preferences_single_group(group, "entity", targets)

        def test_single_group_invalid_target(self, instance, targets):
            group = {"A": {"list": ["X", "Z"]}}

            with pytest.raises(PrefNotFoundError):
                instance.check_preferences_single_group(group, "entity", targets)

    class TestTielessListsToRank:
        def test_tieless_lists_to_rank(self, instance):
            group = {
                "A": {"list": ["X", "Y", "Z"]},
            }

            instance.tieless_lists_to_rank(group)

            assert group["A"]["rank"] == {"X": 0, "Y": 1, "Z": 2}

        def test_tieless_lists_to_rank_empty_list(self, instance):
            group = {"A": {"list": []}}

            instance.tieless_lists_to_rank(group)

            assert group["A"]["rank"] == {}
