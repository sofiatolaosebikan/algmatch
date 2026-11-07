from copy import deepcopy
from typing import Callable
import pytest

from algmatch.errors.ReaderErrors import (
    CapacityError,
    IDMisformatError,
    PrefListMisformatError,
)
from algmatch.stableMatchings.hospitalResidentsProblem.noTies.dictionaryReader import (
    DictionaryReader,
)

VALID_DICTIONARY = {
    "residents": {
        1: [1, 2],
        2: [2, 1],
    },
    "hospitals": {
        1: {
            "capacity": 2,
            "preferences": [1, 2],
        },
        2: {
            "capacity": 1,
            "preferences": [2, 1],
        },
    },
}

NON_INT_IDS = ["1", "A", None]


def build_dictionary(mutation: Callable[[dict], None]) -> dict:
    dictionary = deepcopy(VALID_DICTIONARY)
    mutation(dictionary)
    return dictionary


class TestDictionaryReader:
    class TestSuccessfulReading:
        def validate_successful_reader(self, reader: DictionaryReader):
            assert reader.residents["r1"]["list"] == ["h1", "h2"]
            assert reader.residents["r2"]["list"] == ["h2", "h1"]

            assert reader.hospitals["h1"]["list"] == ["r1", "r2"]
            assert reader.hospitals["h2"]["list"] == ["r2", "r1"]

            assert reader.hospitals["h1"]["capacity"] == 2
            assert reader.hospitals["h2"]["capacity"] == 1

        def test_builds_residents_dictionary(self):
            reader = DictionaryReader(VALID_DICTIONARY)

            self.validate_successful_reader(reader)

        # ideally this responsibility will be moved up out of the readers
        def test_initialises_empty_rank_maps(self):
            reader = DictionaryReader(VALID_DICTIONARY)

            for participant in (
                *reader.residents.values(),
                *reader.hospitals.values(),
            ):
                assert participant["rank"] == {}

        def test_accepts_empty_resident_preference_lists(self):
            dictionary = build_dictionary(lambda x: x["residents"].__setitem__(1, []))

            reader = DictionaryReader(dictionary)

            assert reader.residents["r1"]["list"] == []

        def test_accepts_empty_hospital_preference_lists(self):
            dictionary = build_dictionary(
                lambda x: x["hospitals"][1].__setitem__("preferences", [])
            )

            reader = DictionaryReader(dictionary)

            assert reader.hospitals["h1"]["list"] == []

        def test_accepts_empty_residents_dictionary(self):
            dictionary = build_dictionary(lambda x: x.__setitem__("residents", {}))

            reader = DictionaryReader(dictionary)

            assert reader.residents == {}
            assert len(reader.hospitals) == 2

        def test_accepts_empty_hospitals_dictionary(self):
            dictionary = build_dictionary(lambda x: x.__setitem__("hospitals", {}))

            reader = DictionaryReader(dictionary)

            assert reader.hospitals == {}
            assert len(reader.residents) == 2

        def test_just_ignores_unknown_keys(self):
            dictionary = build_dictionary(
                lambda x: x.__setitem__("unknown", {"gibberish": ["nonsense"]})
            )

            reader = DictionaryReader(dictionary)

            self.validate_successful_reader(reader)

    class TestResidentIDErrors:
        @pytest.mark.parametrize("id", NON_INT_IDS)
        def test_id_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["residents"].__setitem__(id, [1, 2])
            )

            with pytest.raises(IDMisformatError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("id", NON_INT_IDS)
        def test_preference_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["residents"].__setitem__(1, [1, id])
            )

            with pytest.raises(PrefListMisformatError):
                DictionaryReader(dictionary)

    class TestHospitalIDErrors:
        @pytest.mark.parametrize("id", NON_INT_IDS)
        def test_id_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["hospitals"].__setitem__(
                    id,
                    {"capacity": 2, "preferences": [1, 2]},
                )
            )

            with pytest.raises(IDMisformatError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("capacity", ["2", "A", None, 2.5])
        def test_capacity_not_an_integer(self, capacity):
            dictionary = build_dictionary(
                lambda x: x["hospitals"][1].__setitem__("capacity", capacity)
            )

            with pytest.raises(CapacityError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("id", NON_INT_IDS)
        def test_preference_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["hospitals"][1].__setitem__("preferences", [1, id])
            )

            with pytest.raises(PrefListMisformatError):
                DictionaryReader(dictionary)
