"""
Class to read in a file of preferences for the Stable Marriage Problem stable matching algorithm.
"""

from re import findall

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import (
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

    def regex_split(self, line):
        # Read as: find cases of more than one digit or either '(' or ')'
        return findall(r"\d+|[\(\)]", line)

    def _scan_preference_tokens(self, token_list, side):
        preferences = []
        in_tie = False
        cur_set = set()

        if side == "man":
            pref_char = "w"
        else:
            pref_char = "m"

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
        self.no_men = 0
        self.no_women = 0
        self.men = {}
        self.women = {}
        self.cur_line = 1

        with open(self.data, "r") as file:
            file = file.read().splitlines()

        try:
            self.no_men, self.no_women = map(int, file[0].split())
        except ValueError:
            raise ParticipantQuantityError()
        if self.no_men < 0 or self.no_women < 0:
            raise ParticipantQuantityError()

        # build men dictionary
        for elt in file[1 : self.no_men + 1]:
            self.cur_line += 1
            entry = self.regex_split(elt)

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("man", self.cur_line, line=True)
            man = f"m{entry[0]}"
            if man in self.men:
                raise RepeatIDError("man", self.cur_line, line=True)

            preferences = self._scan_preference_tokens(entry[1:], "man")
            self.men[man] = {"list": preferences, "rank": {}}

        # build women dictionary
        for elt in file[self.no_men + 1 : self.no_men + self.no_women + 1]:
            self.cur_line += 1
            entry = self.regex_split(elt)

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("woman", self.cur_line, line=True)
            woman = f"w{entry[0]}"
            if woman in self.women:
                raise RepeatIDError("woman", self.cur_line, line=True)

            preferences = self._scan_preference_tokens(entry[1:], "woman")
            self.women[woman] = {"list": preferences, "rank": {}}
