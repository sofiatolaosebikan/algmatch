from unittest.mock import mock_open, patch
from typing import Callable
import pytest

from algmatch.errors.ReaderErrors import (
    ParticipantQuantityError,
    CapacityError,
    IDMisformatError,
    RepeatIDError,
    PrefListMisformatError,
)
from algmatch.stableMatchings.hospitalResidentsProblem.noTies.fileReader import (
    FileReader,
)


VALID_CONTENT_LIST = [
    "2 2",
    "1 1 2",
    "2 2 1",
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
            assert reader.no_residents == 2
            assert reader.no_hospitals == 2

            assert reader.residents["r1"]["list"] == ["h1", "h2"]
            assert reader.residents["r2"]["list"] == ["h2", "h1"]

            assert reader.hospitals["h1"]["capacity"] == 2
            assert reader.hospitals["h1"]["list"] == ["r1", "r2"]

            assert reader.hospitals["h2"]["capacity"] == 1
            assert reader.hospitals["h2"]["list"] == ["r2", "r1"]

        def test_builds_dictionaries(self):
            content = build_content(lambda x: None)

            reader = read_content(content)

            self.validate_successful_reader(reader)

        # ideally this responsibility will be moved up out of the readers
        def test_initialises_empty_rank_maps(self):
            content = build_content(lambda x: None)

            reader = read_content(content)

            for participant in (*reader.residents.values(), *reader.hospitals.values()):
                assert participant["rank"] == {}

        def test_accepts_empty_resident_preference_lists(self):
            content = build_content(lambda x: x.__setitem__(1, "1"))

            reader = read_content(content)

            assert len(reader.residents["r1"]["list"]) == 0

        def test_accepts_empty_hospital_preference_lists(self):
            content = build_content(lambda x: x.__setitem__(3, "1 2"))

            reader = read_content(content)

            assert len(reader.hospitals["h1"]["list"]) == 0

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
            "first_line", ["", "1", "1 1 1", "-1 1", "1 -1", "1,1"]
        )
        def test_missing_count_line(self, first_line: str):
            content = build_content(lambda x: x.__setitem__(0, first_line))

            with pytest.raises(ParticipantQuantityError):
                read_content(content)

    class TestResidentIDErrors:
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

    class TestHospitalIDErrors:
        @pytest.mark.parametrize("id", NON_DIGITS)
        def test_id_not_a_digit(self, id: str):
            content = build_content(lambda x: x.__setitem__(3, f"{id} 2 1 2"))

            with pytest.raises(IDMisformatError):
                read_content(content)

        def test_duplicate_id(self):
            content = build_content(lambda x: x.__setitem__(4, "1 1 2 1"))

            with pytest.raises(RepeatIDError):
                read_content(content)

        @pytest.mark.parametrize("capacity", NON_DIGITS)
        def test_capacity_not_a_digit(self, capacity: str):
            content = build_content(lambda x: x.__setitem__(3, f"1 {capacity} 1 2"))

            with pytest.raises(CapacityError):
                read_content(content)

        @pytest.mark.parametrize("id", NON_DIGITS)
        def test_preference_not_a_digit(self, id: str):
            content = build_content(lambda x: x.__setitem__(3, f"1 2 1 {id}"))

            with pytest.raises(PrefListMisformatError):
                read_content(content)
