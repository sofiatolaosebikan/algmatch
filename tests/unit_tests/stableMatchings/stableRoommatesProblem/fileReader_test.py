from unittest.mock import mock_open, patch
from typing import Callable
import pytest

from algmatch.errors.ReaderErrors import (
    ParticipantQuantityError,
    IDMisformatError,
    RepeatIDError,
    PrefListMisformatError,
)
from algmatch.stableMatchings.stableRoommatesProblem.fileReader import FileReader

VALID_CONTENT_LIST = [
    "3",
    "1 2 3",
    "2 1 3",
    "3 1 2",
]

NON_DIGITS = ["A", "2.5"]


def build_content(mutation: Callable[[list[str]], None]) -> str:
    content_list = VALID_CONTENT_LIST.copy()
    mutation(content_list)
    return "\n".join(content_list)


def read_content(content: str) -> FileReader:
    "Creating a real file take ages, never do it."
    filename = "preferences.txt"
    with patch("builtins.open", mock_open(read_data=content)) as mocked_open:
        reader = FileReader(filename)
        mocked_open.assert_called_once_with(filename, "r")

    return reader


class TestFileReader:
    class TestSuccessfulReading:
        def validate_successful_reader(self, reader: FileReader):
            assert reader.no_roommates == 3
            assert reader.roommates["r1"]["list"] == ["r2", "r3"]
            assert reader.roommates["r2"]["list"] == ["r1", "r3"]
            assert reader.roommates["r3"]["list"] == ["r1", "r2"]

        def test_builds_dictionaries(self):
            content = build_content(lambda x: None)

            reader = read_content(content)

            self.validate_successful_reader(reader)

        # ideally this responsibility will be moved up out of the readers
        def test_initialises_empty_rank_maps(self):
            content = build_content(lambda x: None)

            reader = read_content(content)

            for participant in reader.roommates.values():
                assert participant["rank"] == {}

        def test_accepts_empty_preference_lists(self):
            content = build_content(lambda x: x.__setitem__(1, "1"))

            reader = read_content(content)

            assert len(reader.roommates["r1"]["list"]) == 0

        def test_ignores_leading_whitespaces(self):
            content = "\n".join([f"  {y}" for y in VALID_CONTENT_LIST])

            reader = read_content(content)

            self.validate_successful_reader(reader)

        def test_ignores_lines_after_declared_participants(self):
            content = build_content(lambda x: x.append("comment"))

            reader = read_content(content)

            self.validate_successful_reader(reader)

    class TestParticipantQuantityErrors:
        @pytest.mark.parametrize("first_line", ["", "1 1", "-1"])
        def test_missing_count_line(self, first_line: str):
            content = build_content(lambda x: x.__setitem__(0, first_line))

            with pytest.raises(ParticipantQuantityError):
                read_content(content)

    class TestRoommateIDErrors:
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
