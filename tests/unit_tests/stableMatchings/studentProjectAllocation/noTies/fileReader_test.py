from unittest.mock import mock_open, patch
from typing import Callable
import pytest

from algmatch.errors.ReaderErrors import (
    ParticipantQuantityError,
    CapacityError,
    IDMisformatError,
    RepeatIDError,
    PrefListMisformatError,
    OffererError,
)
from algmatch.stableMatchings.studentProjectAllocation.noTies.fileReader import (
    FileReader,
)

VALID_CONTENT_LIST = [
    "2 2 2",
    "1 1 2",
    "2 2 1",
    "1 2 1",
    "2 1 2",
    "1 2 1 2",
    "2 1 2 1",
]

NON_DIGITS = ["A", "2.5"]


def build_content(mutation: Callable[[list[str]], None]) -> str:
    content_list = VALID_CONTENT_LIST.copy()
    mutation(content_list)
    return "\n".join(content_list)


def read_content(content: str) -> FileReader:
    "Creating a real file takes ages, never do it."
    filename = "preferences.txt"
    with patch("builtins.open", mock_open(read_data=content)) as mocked_open:
        reader = FileReader(filename)
        mocked_open.assert_called_once_with(filename, "r")

    return reader


class TestFileReader:
    class TestSuccessfulReading:
        def validate_successful_reader(self, reader: FileReader):
            assert reader.no_students == 2
            assert reader.no_projects == 2
            assert reader.no_lecturers == 2

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

        def test_builds_dictionaries(self):
            content = build_content(lambda x: None)

            reader = read_content(content)

            self.validate_successful_reader(reader)

        def test_accepts_empty_student_preference_lists(self):
            content = build_content(lambda x: x.__setitem__(1, "1"))

            reader = read_content(content)

            assert len(reader.students["s1"]["list"]) == 0

        def test_accepts_empty_lecturer_preference_lists(self):
            content = build_content(lambda x: x.__setitem__(5, "1 2"))

            reader = read_content(content)

            assert len(reader.lecturers["l1"]["list"]) == 0

        def test_ignores_leading_whitespaces(self):
            content = build_content(lambda x: [f"  {y}" for y in x])

            reader = read_content(content)

            self.validate_successful_reader(reader)

        def test_ignores_lines_after_declared_participants(self):
            content = build_content(lambda x: x.append("comment"))

            reader = read_content(content)

            self.validate_successful_reader(reader)

    class TestParticipantQuantityErrors:
        @pytest.mark.parametrize(
            "first_line", ["", "1", "1 1", "1 1 1 1", "-1 1 1", "1,1,1"]
        )
        def test_missing_count_line(self, first_line: str):
            content = build_content(lambda x: x.__setitem__(0, first_line))

            with pytest.raises(ParticipantQuantityError):
                read_content(content)

    class TestStudentIDErrors:
        @pytest.mark.parametrize("id", NON_DIGITS)
        def test_id_not_a_digit(self, id: str):
            content = build_content(lambda x: x.__setitem__(1, f"{id} 1 2"))

            with pytest.raises(IDMisformatError):
                read_content(content)

        def test_duplicate_id(self):
            content = build_content(lambda x: x.__setitem__(2, "1 2 1"))

            with pytest.raises(RepeatIDError):
                read_content(content)

        @pytest.mark.parametrize("id", NON_DIGITS)
        def test_preference_not_a_digit(self, id: str):
            content = build_content(lambda x: x.__setitem__(1, f"1 1 {id}"))

            with pytest.raises(PrefListMisformatError):
                read_content(content)

    class TestProjectIDErrors:
        @pytest.mark.parametrize("id", NON_DIGITS)
        def test_id_not_a_digit(self, id: str):
            content = build_content(lambda x: x.__setitem__(3, f"{id} 2 1"))

            with pytest.raises(IDMisformatError):
                read_content(content)

        def test_duplicate_id(self):
            content = build_content(lambda x: x.__setitem__(4, "1 1 2"))

            with pytest.raises(RepeatIDError):
                read_content(content)

        @pytest.mark.parametrize("capacity", ["A", "a", "2.5"])
        def test_capacity_not_a_digit(self, capacity: str):
            content = build_content(lambda x: x.__setitem__(3, f"1 {capacity} 1"))

            with pytest.raises(CapacityError):
                read_content(content)

        @pytest.mark.parametrize("id", NON_DIGITS)
        def test_lecturer_not_a_digit(self, id: str):
            content = build_content(lambda x: x.__setitem__(3, f"1 2 {id}"))

            with pytest.raises(OffererError):
                read_content(content)

    class TestLecturerIDErrors:
        @pytest.mark.parametrize("id", NON_DIGITS)
        def test_id_not_a_digit(self, id: str):
            content = build_content(lambda x: x.__setitem__(5, f"{id} 2 1 2"))

            with pytest.raises(IDMisformatError):
                read_content(content)

        def test_duplicate_id(self):
            content = build_content(lambda x: x.__setitem__(6, "1 1 2 1"))

            with pytest.raises(RepeatIDError):
                read_content(content)

        @pytest.mark.parametrize("capacity", NON_DIGITS)
        def test_capacity_not_a_digit(self, capacity: str):
            content = build_content(lambda x: x.__setitem__(5, f"1 {capacity} 1 2"))

            with pytest.raises(CapacityError):
                read_content(content)

        @pytest.mark.parametrize("id", NON_DIGITS)
        def test_preference_not_a_digit(self, id: str):
            content = build_content(lambda x: x.__setitem__(5, f"1 2 1 {id}"))

            with pytest.raises(PrefListMisformatError):
                read_content(content)
