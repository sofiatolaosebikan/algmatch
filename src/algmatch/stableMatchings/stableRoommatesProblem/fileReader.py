"""
Class to read in a file of preferences for the Stable Roommates Problem stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import (
    ParticipantQuantityError,
    IDMisformatError,
    RepeatIDError,
    PrefListMisformatError,
)


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.no_roommates = 0
        self.roommates = {}
        cur_line = 1

        with open(self.data, "r") as file:
            file = file.read().splitlines()

        try:
            [self.no_roommates] = map(int, file[0].split())
        except (ValueError, IndexError):
            raise ParticipantQuantityError()
        if self.no_roommates < 0:
            raise ParticipantQuantityError()

        for elt in file[1 : self.no_roommates + 1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("roommate", cur_line, line=True)
            roommate = f"r{entry[0]}"
            if roommate in self.roommates:
                raise RepeatIDError("roommate", cur_line, line=True)

            for i in entry[1:]:
                if not i.isdigit():
                    raise PrefListMisformatError("roommate", cur_line, i, line=True)
            preferences = [f"r{i}" for i in entry[1:]]

            self.roommates[roommate] = {"list": preferences, "rank": {}}
