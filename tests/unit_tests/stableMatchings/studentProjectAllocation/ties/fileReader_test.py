from unittest.mock import mock_open, patch
from typing import Callable
import pytest

from algmatch.errors.ReaderErrors import (
    CapacityError,
    IDMisformatError,
    NestedTiesError,
    OffererError,
    ParticipantQuantityError,
    RepeatIDError,
    UnclosedTieError,
    UnopenedTieError,
)
from algmatch.stableMatchings.studentProjectAllocation.ties.fileReader import (
    FileReader,
)


VALID_CONTENT_LIST = [
    "2 2 2",
    "1 1 (2)",
    "2 2 1",
    "1 2 1",
    "2 1 2",
    "1 2 1 2",
    "2 1 (2 1)",
]


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

            assert reader.students["s1"]["list"] == [{"p1"}, {"p2"}]
            assert reader.students["s2"]["list"] == [{"p2"}, {"p1"}]

            assert reader.projects["p1"]["capacity"] == 2
            assert reader.projects["p1"]["lecturer"] == "l1"

            assert reader.projects["p2"]["capacity"] == 1
            assert reader.projects["p2"]["lecturer"] == "l2"

            assert reader.lecturers["l1"]["capacity"] == 2
            assert reader.lecturers["l1"]["list"] == [{"s1"}, {"s2"}]

            assert reader.lecturers["l2"]["capacity"] == 1
            assert reader.lecturers["l2"]["list"] == [{"s2", "s1"}]

        def test_builds_dictionaries(self):
            content = build_content(lambda x: None)

            reader = read_content(content)

            self.validate_successful_reader(reader)

        # ideally this responsibility will be moved up out of the readers
        def test_initialises_empty_rank_maps(self):
            content = build_content(lambda x: None)

            reader = read_content(content)

            for participant in (*reader.students.values(), *reader.lecturers.values()):
                assert participant["rank"] == {}

        def test_accepts_empty_student_preference_lists(self):
            content = build_content(lambda x: x.__setitem__(1, "1"))

            reader = read_content(content)

            assert len(reader.students["s1"]["list"]) == 0

        def test_accepts_empty_lecturer_preference_lists(self):
            content = build_content(lambda x: x.__setitem__(5, "1 2"))

            reader = read_content(content)

            assert len(reader.lecturers["l1"]["list"]) == 0

        def test_reads_multiple_student_ties(self):
            content = build_content(lambda x: x.__setitem__(1, "1 (1 2) (3 4)"))

            reader = read_content(content)

            assert reader.students["s1"]["list"] == [{"p1", "p2"}, {"p3", "p4"}]

        def test_reads_multiple_lecturer_ties(self):
            content = build_content(lambda x: x.__setitem__(5, "1 2 (1 2) (3 4)"))

            reader = read_content(content)

            assert reader.lecturers["l1"]["list"] == [{"s1", "s2"}, {"s3", "s4"}]

        def test_ignores_leading_whitespaces(self):
            content = "\n".join([f"  {y}" for y in VALID_CONTENT_LIST])

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
        def test_missing_id(self):
            content = build_content(lambda x: x.__setitem__(1, ""))

            with pytest.raises(IDMisformatError):
                read_content(content)

        def test_duplicate_id(self):
            content = build_content(lambda x: x.__setitem__(2, "1 2 1"))

            with pytest.raises(RepeatIDError):
                read_content(content)

    class TestProjectIDErrors:
        def test_missing_id(self):
            content = build_content(lambda x: x.__setitem__(3, ""))

            with pytest.raises(IDMisformatError):
                read_content(content)

        def test_duplicate_id(self):
            content = build_content(lambda x: x.__setitem__(4, "1 1 2"))

            with pytest.raises(RepeatIDError):
                read_content(content)

    class TestProjectCapacityErrors:
        def test_non_digit_capacity(self):
            content = build_content(lambda x: x.__setitem__(3, "1 A 1"))

            with pytest.raises(CapacityError):
                read_content(content)

    class TestProjectOffererErrors:
        def test_non_digit_offerer(self):
            content = build_content(lambda x: x.__setitem__(3, "1 2 A"))

            with pytest.raises(OffererError):
                read_content(content)

    class TestLecturerIDErrors:
        def test_missing_id(self):
            content = build_content(lambda x: x.__setitem__(5, ""))

            with pytest.raises(IDMisformatError):
                read_content(content)

        def test_duplicate_id(self):
            content = build_content(lambda x: x.__setitem__(6, "1 1 2 1"))

            with pytest.raises(RepeatIDError):
                read_content(content)

    class TestStudentTieErrors:
        def test_nested_ties(self):
            content = build_content(lambda x: x.__setitem__(1, "1 (1 (2))"))

            with pytest.raises(NestedTiesError):
                read_content(content)

        def test_unclosed_tie(self):
            content = build_content(lambda x: x.__setitem__(1, "1 (1 2"))

            with pytest.raises(UnclosedTieError):
                read_content(content)

        def test_unopened_tie(self):
            content = build_content(lambda x: x.__setitem__(1, "1 1 2)"))

            with pytest.raises(UnopenedTieError):
                read_content(content)

    class TestLecturerTieErrors:
        def test_nested_ties(self):
            content = build_content(lambda x: x.__setitem__(5, "1 2 (1 (2))"))

            with pytest.raises(NestedTiesError):
                read_content(content)

        def test_unclosed_tie(self):
            content = build_content(lambda x: x.__setitem__(5, "1 2 (1 2"))

            with pytest.raises(UnclosedTieError):
                read_content(content)

        def test_unopened_tie(self):
            content = build_content(lambda x: x.__setitem__(5, "1 2 1 2)"))

            with pytest.raises(UnopenedTieError):
                read_content(content)
