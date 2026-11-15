import numpy as np
from time import perf_counter_ns
from tqdm import tqdm

from tests.integration.abstractTestClasses.abstractSingleVerifier import (
    AbstractSingleVerifier,
)
from tests.integration.SPASTests.SPASTSuper.spastSuperVerifier import SPASTSuperVerifier


class SPASTSuperSingleVerifier(SPASTSuperVerifier, AbstractSingleVerifier):
    def __init__(
        self, total_students, total_projects, total_lecturers, lower_bound, upper_bound
    ):
        SPASTSuperVerifier.__init__(
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
    TOTAL_STUDENTS = 6
    TOTAL_PROJECTS = 3
    TOTAL_LECTURERS = 2
    LOWER_BOUND = 0
    UPPER_BOUND = 3
    TIE_DENSITY_STEPS = 10
    REPS_PER_TDS = 5_000

    td_step_size = 1 / TIE_DENSITY_STEPS
    td_values = np.arange(0, 1 + td_step_size / 2, td_step_size)

    start = perf_counter_ns()

    verifier = SPASTSuperSingleVerifier(
        TOTAL_STUDENTS, TOTAL_PROJECTS, TOTAL_LECTURERS, LOWER_BOUND, UPPER_BOUND
    )

    for td in td_values:
        print("-" * 18)
        print(f"With Tie Density: {td}")

        verifier.gen.set_tie_density(td)
        for _ in tqdm(range(REPS_PER_TDS)):
            verifier.run()

    end = perf_counter_ns()
    print(f"\nFinal Runtime: {(end - start) / 1000**3}s")

    verifier.show_results()


if __name__ == "__main__":
    main()
