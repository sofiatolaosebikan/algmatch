import numpy as np
from time import perf_counter_ns
from tqdm import tqdm

from tests.integration.abstractTestClasses.abstractSingleVerifier import (
    AbstractSingleVerifier as ASV,
)
from tests.integration.SMTests.SMTStrong.smtStrongVerifier import (
    SMTStrongVerifier as SMTStrongV,
)


class SMTStrongSingleVerifier(SMTStrongV, ASV):
    def __init__(self, total_men, total_women, lower_bound, upper_bound):
        SMTStrongV.__init__(self, total_men, total_women, lower_bound, upper_bound)
        ASV.__init__(self)

    def show_results(self):
        print(f"""
            Total men: {self._total_men}
            Total women: {self._total_women}
            Preference list length lower bound: {self._lower_bound}
            Preference list length upper bound: {self._upper_bound}
            Repetitions: {self._total_count}

            Correct: {self._correct_count}
            Incorrect: {self._incorrect_count}
              """)


def main():
    n = 5
    TOTAL_MEN = n
    TOTAL_WOMEN = n
    LOWER_LIST_BOUND = 0
    UPPER_LIST_BOUND = n
    TIE_DENSITY_STEPS = 10
    REPS_PER_TDS = 1000

    td_step_size = 1 / TIE_DENSITY_STEPS
    td_values = np.arange(0, 1 + td_step_size / 2, td_step_size)

    start = perf_counter_ns()

    verifier = SMTStrongSingleVerifier(
        TOTAL_MEN, TOTAL_WOMEN, LOWER_LIST_BOUND, UPPER_LIST_BOUND
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
