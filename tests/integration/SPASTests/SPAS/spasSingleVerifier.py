from time import perf_counter_ns
from tqdm import tqdm

from tests.integration.abstractTestClasses.abstractSingleVerifier import (
    AbstractSingleVerifier,
)
from tests.integration.SPASTests.SPAS.spasVerifier import SPASVerifier


class SPASSingleVerifier(SPASVerifier, AbstractSingleVerifier):
    def __init__(
        self, total_students, total_projects, total_lecturers, lower_bound, upper_bound
    ):
        SPASVerifier.__init__(
            self,
            total_students,
            total_projects,
            total_lecturers,
            lower_bound,
            upper_bound,
        )
        AbstractSingleVerifier.__init__(self)

    def show_results(self):
        print(f"""
            Total students: {self._total_students}
            Total projects: {self._total_projects}
            Total lecturers: {self._total_lecturers}
            Lower list bound: {self._lower_bound}
            Upper list bound: {self._upper_bound}
            Repetitions: {self._total_count}

            Correct: {self._correct_count}
            Incorrect: {self._incorrect_count}
              """)


def main():
    TOTAL_STUDENTS = 12
    TOTAL_PROJECTS = 5
    TOTAL_LECTURERS = 3
    LOWER_BOUND = 0
    UPPER_BOUND = 3
    REPETITIONS = 40_000

    start = perf_counter_ns()

    verifier = SPASSingleVerifier(
        TOTAL_STUDENTS, TOTAL_PROJECTS, TOTAL_LECTURERS, LOWER_BOUND, UPPER_BOUND
    )
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    end = perf_counter_ns()
    print(f"\nFinal Runtime: {(end - start) / 1000**3}s")

    verifier.show_results()


if __name__ == "__main__":
    main()
