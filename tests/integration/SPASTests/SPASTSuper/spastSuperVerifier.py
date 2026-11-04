from algmatch import SPAST
from algmatch.utils import SPASTEnumerator, SPASTGenerator

from tests.integration.abstractTestClasses.abstractVerifier import AbstractVerifier


class SPASTSuperVerifier(AbstractVerifier):
    def __init__(
        self, total_students, total_projects, total_lecturers, lower_bound, upper_bound
    ):
        """
        It takes argument as follows (set in init):
            number of students
            number of projects
            number of lecturers
            lower bound of the students' preference list length
            upper bound of the students' preference list length
        """

        self._total_students = total_students
        self._total_projects = total_projects
        self._total_lecturers = total_lecturers
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

        generator = SPASTGenerator(
            total_students,
            total_projects,
            total_lecturers,
            lower_bound,
            upper_bound,
        )

        AbstractVerifier.__init__(
            self,
            SPAST,
            ("students", "lecturers"),
            generator,
            SPASTEnumerator,
            "super",
        )
