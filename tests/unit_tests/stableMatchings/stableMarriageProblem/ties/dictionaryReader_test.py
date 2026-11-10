from copy import deepcopy
from typing import Callable
import pytest

from algmatch.errors.ReaderErrors import (
    IDMisformatError,
    PrefListMisformatError,
)
from algmatch.stableMatchings.stableMarriageProblem.ties.dictionaryReader import (
    DictionaryReader,
)

VALID_DICTIONARY = {
    "men": {
        1: [1, [2]],
        2: [2, 1],
    },
    "women": {
        1: [1, 2],
        2: [[2, 1]],
    },
}

NON_INTS = ["1", None, 1.5]


def build_dictionary(mutation: Callable[[dict], None]) -> dict:
    dictionary = deepcopy(VALID_DICTIONARY)
    mutation(dictionary)
    return dictionary


class TestDictionaryReader:
    class TestSuccessfulReading:
        def validate_successful_reader(self, reader: DictionaryReader):
            assert reader.men["m1"]["list"] == [{"w1"}, {"w2"}]
            assert reader.men["m2"]["list"] == [{"w2"}, {"w1"}]
            assert reader.women["w1"]["list"] == [{"m1"}, {"m2"}]
            assert reader.women["w2"]["list"] == [{"m2", "m1"}]

        def test_builds_men_dictionary(self):
            reader = DictionaryReader(VALID_DICTIONARY)

            self.validate_successful_reader(reader)

        # ideally this responsibility will be moved up out of the readers
        def test_initialises_empty_rank_maps(self):
            reader = DictionaryReader(VALID_DICTIONARY)

            for participant in (*reader.men.values(), *reader.women.values()):
                assert participant["rank"] == {}

        def test_accepts_empty_ties(self):
            dictionary = build_dictionary(lambda x: x["men"].__setitem__(1, [[]]))

            reader = DictionaryReader(dictionary)

            assert reader.men["m1"]["list"] == [set()]

        def test_accepts_empty_preference_lists(self):
            dictionary = build_dictionary(lambda x: x["men"].__setitem__(1, []))

            reader = DictionaryReader(dictionary)

            assert reader.men["m1"]["list"] == []

        def test_accepts_empty_men_dictionary(self):
            dictionary = build_dictionary(lambda x: x.__setitem__("men", {}))

            reader = DictionaryReader(dictionary)

            assert reader.men == {}
            assert len(reader.women) == 2

        def test_accepts_empty_women_dictionary(self):
            dictionary = build_dictionary(lambda x: x.__setitem__("women", {}))

            reader = DictionaryReader(dictionary)

            assert reader.women == {}
            assert len(reader.men) == 2

        def test_just_ignores_unknown_keys(self):
            dictionary = build_dictionary(
                lambda x: x.__setitem__("unknown", {"gibberish": ["nonsense"]})
            )

            reader = DictionaryReader(dictionary)

            self.validate_successful_reader(reader)

    class TestManIDErrors:
        @pytest.mark.parametrize("id", NON_INTS)
        def test_id_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["men"].__setitem__(id, [1, [2, 3]])
            )

            with pytest.raises(IDMisformatError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("id", NON_INTS)
        def test_preference_tie_not_a_list_of_integers(self, id):
            dictionary = build_dictionary(
                lambda x: x["women"].__setitem__(1, [[1, id]])
            )

            with pytest.raises(PrefListMisformatError):
                DictionaryReader(dictionary)

    class TestWomanIDErrors:
        @pytest.mark.parametrize("id", NON_INTS)
        def test_id_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["women"].__setitem__(id, [1, [2, 3]])
            )

            with pytest.raises(IDMisformatError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("id", NON_INTS)
        def test_preference_tie_not_a_list_of_integers(self, id):
            dictionary = build_dictionary(
                lambda x: x["women"].__setitem__(1, [[1, id]])
            )

            with pytest.raises(PrefListMisformatError):
                DictionaryReader(dictionary)
