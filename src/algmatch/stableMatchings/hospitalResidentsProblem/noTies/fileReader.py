"""
Class to read in a file of preferences for the Hospitals/Residents Problem stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import (
    ParticipantQuantityError,
    CapacityError,
    IDMisformatError,
    RepeatIDError,
    PrefListMisformatError,
)


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.no_residents = 0
        self.no_hospitals = 0
        self.residents = {}
        self.hospitals = {}
        cur_line = 1

        with open(self.data, "r") as file:
            file = file.read().splitlines()

        try:
            self.no_residents, self.no_hospitals = map(int, file[0].split())
        except (ValueError, IndexError):
            raise ParticipantQuantityError()
        if self.no_residents < 0 or self.no_hospitals < 0:
            raise ParticipantQuantityError()

        # build residents dictionary
        for elt in file[1 : self.no_residents + 1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("resident", cur_line, line=True)
            resident = f"r{entry[0]}"
            if resident in self.residents:
                raise RepeatIDError("resident", cur_line, line=True)

            for i in entry[1:]:
                if not i.isdigit():
                    raise PrefListMisformatError("resident", cur_line, i, line=True)
            preferences = [f"h{i}" for i in entry[1:]]

            self.residents[resident] = {"list": preferences, "rank": {}}

        # build hospitals dictionary
        for elt in file[
            self.no_residents + 1 : self.no_residents + self.no_hospitals + 1
        ]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("hospital", cur_line, line=True)
            hospital = f"h{entry[0]}"
            if hospital in self.hospitals:
                raise RepeatIDError("hospital", cur_line, line=True)

            if not entry[1].isdigit():
                raise CapacityError("hospital", cur_line, line=True)
            capacity = int(entry[1])

            for i in entry[2:]:
                if not i.isdigit():
                    raise PrefListMisformatError("hospital", cur_line, i, line=True)
            preferences = [f"r{i}" for i in entry[2:]]

            self.hospitals[hospital] = {
                "capacity": capacity,
                "list": preferences,
                "rank": {},
            }
