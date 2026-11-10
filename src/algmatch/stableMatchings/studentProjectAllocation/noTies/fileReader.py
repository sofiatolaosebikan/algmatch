"""
Class to read in a file of preferences for the Student Project Allocation stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import (
    ParticipantQuantityError,
    CapacityError,
    IDMisformatError,
    RepeatIDError,
    PrefListMisformatError,
    OffererError,
)


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.no_students = 0
        self.no_projects = 0
        self.no_lecturers = 0  # assume number of lecturers <= number of projects
        self.students = {}
        self.projects = {}
        self.lecturers = {}
        cur_line = 1

        with open(self.data, "r") as file:
            file = file.read().splitlines()

        try:
            self.no_students, self.no_projects, self.no_lecturers = map(
                int, file[0].split()
            )
        except (ValueError, IndexError):
            raise ParticipantQuantityError()
        if self.no_students < 0 or self.no_projects < 0 or self.no_lecturers < 0:
            raise ParticipantQuantityError()

        # build students dictionary
        for elt in file[1 : self.no_students + 1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("student", cur_line, line=True)
            student = f"s{entry[0]}"
            if student in self.students:
                raise RepeatIDError("student", cur_line, line=True)

            for i in entry[1:]:
                if not i.isdigit():
                    raise PrefListMisformatError("student", cur_line, i, line=True)
            preferences = [f"p{k}" for k in entry[1:]]

            rank = {proj: idx for idx, proj in enumerate(preferences)}
            self.students[student] = {"list": preferences, "rank": rank}

        # build projects dictionary
        for elt in file[self.no_students + 1 : self.no_students + self.no_projects + 1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("project", cur_line, line=True)
            project = f"p{entry[0]}"
            if project in self.projects:
                raise RepeatIDError("project", cur_line, line=True)

            if not entry[1].isdigit():
                raise CapacityError("project", cur_line, line=True)
            capacity = int(entry[1])

            if not entry[2].isdigit():
                raise OffererError("project", "lecturer", cur_line, line=True)
            offerer = f"l{entry[2]}"

            self.projects[project] = {
                "lower_quota": 0,
                "upper_quota": capacity,
                "lecturer": offerer,
            }

        # build lecturers dictionary
        for elt in file[
            self.no_students + self.no_projects + 1 : self.no_students
            + self.no_projects
            + self.no_lecturers
            + 1
        ]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("lecturer", cur_line, line=True)
            lecturer = f"l{entry[0]}"
            if lecturer in self.lecturers:
                raise RepeatIDError("lecturer", cur_line, line=True)

            if not entry[1].isdigit():
                raise CapacityError("lecturer", cur_line, line=True)
            capacity = int(entry[1])

            for i in entry[2:]:
                if not i.isdigit():
                    raise PrefListMisformatError("lecturer", cur_line, i, line=True)
            preferences = [f"s{i}" for i in entry[2:]]

            self.lecturers[lecturer] = {
                "upper_quota": capacity,
                "projects": set(),
                "list": preferences,
                "rank": rank,
            }
