"""
Class to read in a file of preferences for the Stable Marriage Problem stable matching algorithm.
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
        self.no_men = 0
        self.no_women = 0
        self.men = {}
        self.women = {}
        cur_line = 1

        with open(self.data, "r") as file:
            file = file.read().splitlines()

        try:
            self.no_men, self.no_women = map(int, file[0].split())
        except (ValueError, IndexError):
            raise ParticipantQuantityError()
        if self.no_men < 0 or self.no_women < 0:
            raise ParticipantQuantityError()

        # build men dictionary
        for elt in file[1 : self.no_men + 1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("man", cur_line, line=True)
            man = f"m{entry[0]}"
            if man in self.men:
                raise RepeatIDError("man", cur_line, line=True)

            for i in entry[1:]:
                if not i.isdigit():
                    raise PrefListMisformatError("man", cur_line, i, line=True)
            preferences = [f"w{i}" for i in entry[1:]]

            self.men[man] = {"list": preferences, "rank": {}}

        # build women dictionary
        for elt in file[self.no_men + 1 : self.no_men + self.no_women + 1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("woman", cur_line, line=True)
            woman = f"w{entry[0]}"
            if woman in self.women:
                raise RepeatIDError("woman", cur_line, line=True)

            for i in entry[1:]:
                if not i.isdigit():
                    raise PrefListMisformatError("woman", cur_line, i, line=True)
            preferences = [f"m{i}" for i in entry[1:]]

            self.women[woman] = {"list": preferences, "rank": {}}
