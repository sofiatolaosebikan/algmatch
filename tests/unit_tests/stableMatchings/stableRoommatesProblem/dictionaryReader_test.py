from copy import deepcopy
from typing import Callable
import pytest

from algmatch.errors.ReaderErrors import IDMisformatError, PrefListMisformatError
from algmatch.stableMatchings.stableRoommatesProblem.dictionaryReader import (
    DictionaryReader,
)

VALID_DICTIONARY = {
    1: [2, 3],
    2: [1, 3],
    3: [1, 2],
}

NON_INTS = ["1", None, 1.5]


def build_dictionary(mutation: Callable[[dict], None]) -> dict:
    dictionary = deepcopy(VALID_DICTIONARY)
    mutation(dictionary)
    return dictionary


class TestDictionaryReader:
    class TestSuccessfulReading:
        def validate_successful_reader(self, reader: DictionaryReader):
            assert reader.roommates["r1"]["list"] == ["r2", "r3"]
            assert reader.roommates["r2"]["list"] == ["r1", "r3"]
            assert reader.roommates["r3"]["list"] == ["r1", "r2"]

        def test_builds_men_dictionary(self):
            reader = DictionaryReader(VALID_DICTIONARY)

            self.validate_successful_reader(reader)

        # ideally this responsibility will be moved up out of the readers
        def test_initialises_empty_rank_maps(self):
            reader = DictionaryReader(VALID_DICTIONARY)

            for participant in reader.roommates.values():
                assert participant["rank"] == {}

        def test_accepts_empty_preference_lists(self):
            dictionary = build_dictionary(lambda x: x.__setitem__(1, []))

            reader = DictionaryReader(dictionary)

            assert reader.roommates["r1"]["list"] == []

    class TestRoommatesIDErrors:
        @pytest.mark.parametrize("id", NON_INTS)
        def test_id_not_an_integer(self, id):
            dictionary = build_dictionary(lambda x: x.__setitem__(id, [1, 2]))

            with pytest.raises(IDMisformatError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("id", NON_INTS)
        def test_preference_not_an_integer(self, id):
            dictionary = build_dictionary(lambda x: x.__setitem__(1, [1, id]))

            with pytest.raises(PrefListMisformatError):
                DictionaryReader(dictionary)
