import pytest

from algmatch.abstractClasses.abstractPreferenceInstanceWithTies import (
    AbstractPreferenceInstanceWithTies,
)
from algmatch.errors.InstanceSetupErrors import (
    PrefRepError,
    PrefNotFoundError,
)


class DummyPreferenceInstance(AbstractPreferenceInstanceWithTies):
    def _load(self, source):
        pass

    def check_preference_lists(self):
        pass

    def set_up_rankings(self):
        pass


@pytest.fixture
def instance():
    return DummyPreferenceInstance(None)


@pytest.fixture
def targets():
    return {"a": {}, "b": {}, "c": {}}


class TestAbstractPreferenceInstanceWithTies:
    class TestAnyRepetitions:
        def test_no_repetitions(self, instance):
            pref_list = [{"a", "b"}, {"c", "d"}]
            assert instance.any_repetitions(pref_list) is False

        def test_repetition_between_ties(self, instance):
            pref_list = [{"a", "b"}, {"b", "c"}]
            assert instance.any_repetitions(pref_list) is True

        def test_empty_list(self, instance):
            pref_list = []
            assert instance.any_repetitions(pref_list) is False

        def test_empty_ties(self, instance):
            pref_list = [set(), {"a", "b"}, set()]
            assert instance.any_repetitions(pref_list) is False

    class TestTiedListsToRank:
        def test_creates_rank_dictionary(self, instance):
            group = {
                "x": {"list": [{"a", "b"}, {"c"}]},
                "y": {"list": [{"a"}, {"b", "c"}]},
            }

            instance.tied_lists_to_rank(group)

            assert group["x"]["rank"] == {"a": 0, "b": 0, "c": 1}
            assert group["y"]["rank"] == {"a": 0, "b": 1, "c": 1}

        def test_empty_preference_list(self, instance):
            group = {"x": {"list": []}}

            instance.tied_lists_to_rank(group)

            assert group["x"]["rank"] == {}

    class TestCheckPreferencesWithTiesSingleGroup:
        def test_valid_preferences(self, instance, targets):
            group = {"x": {"list": [{"a", "b"}, {"c"}]}}

            instance.check_preferences_with_ties_single_group(group, "entity", targets)

        def test_empty_preferences(self, instance, targets):
            group = {"x": {"list": []}}

            instance.check_preferences_with_ties_single_group(group, "entity", targets)

        def test_duplicate(self, instance, targets):
            group = {"x": {"list": [{"a"}, {"a"}]}}

            with pytest.raises(PrefRepError):
                instance.check_preferences_with_ties_single_group(
                    group, "entity", targets
                )

        def test_unfindable_target(self, instance, targets):
            group = {"x": {"list": [{"a"}, {"Beyng!? In my unit test?!"}]}}

            with pytest.raises(PrefNotFoundError):
                instance.check_preferences_with_ties_single_group(
                    group, "entity", targets
                )
