"""
Class to read in a dictionary of preferences for the SPAST stable matching algorithms.
"""

from re import findall

from algmatch.abstractClasses.abstractReader import AbstractReader
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


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    # Read as: find cases of more than one digit or either '(' or ')'
    def regex_split(self, line):
        return findall(r"\d+|[\(\)]", line)

    def _scan_preference_tokens(self, token_list, side, pref_char):
        preferences = []
        in_tie = False
        cur_set = set()

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
        self.no_students = 0
        self.no_projects = 0
        self.no_lecturers = 0
        self.students = {}
        self.projects = {}
        self.lecturers = {}  # assume number of lecturers <= number of projects
        self.cur_line = 1

        with open(self.data, "r") as file:
            file = file.read().splitlines()

        try:
            self.no_students, self.no_projects, self.no_lecturers = map(
                int, file[0].split()
            )
        except ValueError:
            raise ParticipantQuantityError()
        if self.no_students < 0 or self.no_projects < 0 or self.no_lecturers < 0:
            raise ParticipantQuantityError()

        # build student dictionary
        for elt in file[1 : self.no_students + 1]:
            self.cur_line += 1
            entry = self.regex_split(elt)

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("student", self.cur_line, line=True)
            student = f"s{entry[0]}"
            if student in self.students:
                raise RepeatIDError("student", self.cur_line, line=True)

            preferences = self._scan_preference_tokens(entry[1:], "student", "p")
            self.students[student] = {"list": preferences, "rank": {}}

        # build projects dictionary
        projects_start = self.no_students + 1
        projects_end = projects_start + self.no_projects
        for elt in file[projects_start:projects_end]:
            self.cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("project", self.cur_line, line=True)
            project = f"p{entry[0]}"
            if project in self.projects:
                raise RepeatIDError("project", self.cur_line, line=True)

            if not entry[1].isdigit():
                raise CapacityError("project", self.cur_line, line=True)
            capacity = int(entry[1])

            if not entry[2].isdigit():
                raise OffererError("project", "lecturer", self.cur_line, line=True)
            offerer = f"l{entry[2]}"

            self.projects[project] = {"capacity": capacity, "lecturer": offerer}

        # build lecturers dictionary
        lecturers_end = projects_end + self.no_lecturers
        for elt in file[projects_end:lecturers_end]:
            self.cur_line += 1
            entry = self.regex_split(elt)

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("lecturer", self.cur_line, line=True)
            lecturer = f"l{entry[0]}"
            if lecturer in self.lecturers:
                raise RepeatIDError("lecturer", self.cur_line, line=True)

            if not entry[1].isdigit():
                raise CapacityError("lecturer", self.cur_line, line=True)
            capacity = int(entry[1])

            preferences = self._scan_preference_tokens(entry[2:], "lecturer", "s")
            self.lecturers[lecturer] = {
                "capacity": capacity,
                "projects": set(),
                "list": preferences,
                "rank": {},
            }
