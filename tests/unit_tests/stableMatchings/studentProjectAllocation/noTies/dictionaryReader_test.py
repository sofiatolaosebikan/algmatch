from copy import deepcopy
from typing import Callable
import pytest

from algmatch.errors.ReaderErrors import (
    CapacityError,
    IDMisformatError,
    PrefListMisformatError,
    OffererError,
)
from algmatch.stableMatchings.studentProjectAllocation.noTies.dictionaryReader import (
    DictionaryReader,
)

VALID_DICTIONARY = {
    "students": {
        1: [1, 2],
        2: [2, 1],
    },
    "projects": {
        1: {
            "capacity": 2,
            "lecturer": 1,
        },
        2: {
            "capacity": 1,
            "lecturer": 2,
        },
    },
    "lecturers": {
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

NON_INTS = ["1", None, 1.5]


def build_dictionary(mutation: Callable[[dict], None]) -> dict:
    dictionary = deepcopy(VALID_DICTIONARY)
    mutation(dictionary)
    return dictionary


class TestDictionaryReader:
    class TestSuccessfulReading:
        def validate_successful_reader(self, reader: DictionaryReader):
            assert reader.students["s1"]["list"] == ["p1", "p2"]
            assert reader.students["s2"]["list"] == ["p2", "p1"]

            assert reader.projects["p1"]["upper_quota"] == 2
            assert reader.projects["p1"]["lecturer"] == "l1"
            assert reader.projects["p2"]["upper_quota"] == 1
            assert reader.projects["p2"]["lecturer"] == "l2"

            assert reader.lecturers["l1"]["upper_quota"] == 2
            assert reader.lecturers["l1"]["list"] == ["s1", "s2"]
            assert reader.lecturers["l2"]["upper_quota"] == 1
            assert reader.lecturers["l2"]["list"] == ["s2", "s1"]

        def test_builds_students_dictionary(self):
            reader = DictionaryReader(VALID_DICTIONARY)

            self.validate_successful_reader(reader)

        # ideally this responsibility will be moved up out of the readers
        def test_initialises_empty_rank_maps(self):
            reader = DictionaryReader(VALID_DICTIONARY)

            for participant in (
                *reader.students.values(),
                *reader.lecturers.values(),
            ):
                assert participant["rank"] == {}

        def test_accepts_empty_student_preference_lists(self):
            dictionary = build_dictionary(lambda x: x["students"].__setitem__(1, []))

            reader = DictionaryReader(dictionary)

            assert reader.students["s1"]["list"] == []

        def test_accepts_empty_lecturer_preference_lists(self):
            dictionary = build_dictionary(
                lambda x: x["lecturers"][1].__setitem__("preferences", [])
            )

            reader = DictionaryReader(dictionary)

            assert reader.lecturers["l1"]["list"] == []

        def test_accepts_empty_students_dictionary(self):
            dictionary = build_dictionary(lambda x: x.__setitem__("students", {}))

            reader = DictionaryReader(dictionary)

            assert reader.students == {}
            assert len(reader.projects) == 2
            assert len(reader.lecturers) == 2

        def test_accepts_empty_projects_dictionary(self):
            dictionary = build_dictionary(lambda x: x.__setitem__("projects", {}))

            reader = DictionaryReader(dictionary)

            assert reader.projects == {}
            assert len(reader.students) == 2
            assert len(reader.lecturers) == 2

        def test_accepts_empty_lecturers_dictionary(self):
            dictionary = build_dictionary(lambda x: x.__setitem__("lecturers", {}))

            reader = DictionaryReader(dictionary)

            assert reader.lecturers == {}
            assert len(reader.students) == 2
            assert len(reader.projects) == 2

        def test_just_ignores_unknown_keys(self):
            dictionary = build_dictionary(
                lambda x: x.__setitem__("unknown", {"gibberish": ["nonsense"]})
            )

            reader = DictionaryReader(dictionary)

            self.validate_successful_reader(reader)

    class TestStudentIDErrors:
        @pytest.mark.parametrize("id", NON_INTS)
        def test_id_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["students"].__setitem__(id, [1, 2])
            )

            with pytest.raises(IDMisformatError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("id", NON_INTS)
        def test_preference_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["students"].__setitem__(1, [1, id])
            )

            with pytest.raises(PrefListMisformatError):
                DictionaryReader(dictionary)

    class TestProjectIDErrors:
        @pytest.mark.parametrize("id", NON_INTS)
        def test_id_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["projects"].__setitem__(
                    id,
                    {"capacity": 2, "lecturer": 1},
                )
            )

            with pytest.raises(IDMisformatError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("capacity", NON_INTS)
        def test_capacity_not_an_integer(self, capacity):
            dictionary = build_dictionary(
                lambda x: x["projects"][1].__setitem__("capacity", capacity)
            )

            with pytest.raises(CapacityError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("lecturer", NON_INTS)
        def test_lecturer_not_an_integer(self, lecturer):
            dictionary = build_dictionary(
                lambda x: x["projects"][1].__setitem__(
                    "lecturer",
                    lecturer,
                )
            )

            with pytest.raises(OffererError):
                DictionaryReader(dictionary)

    class TestLecturerIDErrors:
        @pytest.mark.parametrize("id", NON_INTS)
        def test_id_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["lecturers"].__setitem__(
                    id,
                    {"capacity": 2, "preferences": [1, 2]},
                )
            )

            with pytest.raises(IDMisformatError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("capacity", NON_INTS)
        def test_capacity_not_an_integer(self, capacity):
            dictionary = build_dictionary(
                lambda x: x["lecturers"][1].__setitem__("capacity", capacity)
            )

            with pytest.raises(CapacityError):
                DictionaryReader(dictionary)

        @pytest.mark.parametrize("id", NON_INTS)
        def test_preference_not_an_integer(self, id):
            dictionary = build_dictionary(
                lambda x: x["lecturers"][1].__setitem__(
                    "preferences",
                    [1, id],
                )
            )

            with pytest.raises(PrefListMisformatError):
                DictionaryReader(dictionary)
