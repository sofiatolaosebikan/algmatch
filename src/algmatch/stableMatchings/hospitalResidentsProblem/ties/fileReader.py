"""
Class to read in a dictionary of preferences for the Hospital/Residents Problem stable matching algorithm.
"""

from re import findall

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import (
    CapacityError,
    IDMisformatError,
    NestedTiesError,
    ParticipantQuantityError,
    RepeatIDError,
    UnclosedTieError,
    UnopenedTieError,
)


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    # Read as: find cases of more than one digit or either '(' or ')'
    def regex_split(self, line):
        return findall(r"\d+|[\(\)]", line)

    def _scan_preference_tokens(self, token_list, side):
        preferences = []
        in_tie = False
        cur_set = set()

        if side == "resident":
            pref_char = "h"
        else:
            pref_char = "r"

        for token in token_list:
            if token == "(":
                if in_tie:
                    raise NestedTiesError(side, self.cur_line)
                in_tie = True
            elif token == ")":
                if not in_tie:
                    raise UnopenedTieError(side, self.cur_line)
                in_tie = False
                preferences.append(cur_set.copy())
                cur_set.clear()
            else:
                cur_set.add(pref_char + token)
                if not in_tie:
                    preferences.append(cur_set.copy())
                    cur_set.clear()
        if in_tie:
            raise UnclosedTieError(side, self.cur_line)
        return preferences

    def _read_data(self) -> None:
        self.no_residents = 0
        self.no_hospitals = 0
        self.residents = {}
        self.hospitals = {}
        self.cur_line = 1

        with open(self.data, "r") as file:
            file = file.read().splitlines()

        try:
            self.no_residents, self.no_hospitals = map(int, file[0].split())
        except ValueError:
            raise ParticipantQuantityError()
        if self.no_residents < 0 or self.no_hospitals < 0:
            raise ParticipantQuantityError()

        # build resident dictionary
        for elt in file[1 : self.no_residents + 1]:
            self.cur_line += 1
            entry = self.regex_split(elt)

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("resident", self.cur_line, line=True)
            resident = f"r{entry[0]}"
            if resident in self.residents:
                raise RepeatIDError("resident", self.cur_line, line=True)

            preferences = self._scan_preference_tokens(entry[1:], "resident")
            self.residents[resident] = {"list": preferences, "rank": {}}

        # build hospital dictionary
        for elt in file[
            self.no_residents + 1 : self.no_residents + self.no_hospitals + 1
        ]:
            self.cur_line += 1
            entry = self.regex_split(elt)

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("hospital", self.cur_line, line=True)
            hospital = f"h{entry[0]}"
            if hospital in self.hospitals:
                raise RepeatIDError("hospital", self.cur_line, line=True)

            if not entry[1].isdigit():
                raise CapacityError("hospital", self.cur_line, line=True)
            capacity = int(entry[1])

            preferences = self._scan_preference_tokens(entry[2:], "hospital")
            self.hospitals[hospital] = {
                "capacity": capacity,
                "list": preferences,
                "rank": {},
            }
