from time import perf_counter_ns
from tqdm import tqdm

from tests.integration.abstractTestClasses.abstractSingleVerifier import (
    AbstractSingleVerifier as ASV,
)
from tests.integration.HRTests.HR.hrVerifier import HRVerifier as HRV


class HRSingleVerifier(HRV, ASV):
    def __init__(self, total_residents, total_hospitals, lower_bound, upper_bound):
        HRV.__init__(self, total_residents, total_hospitals, lower_bound, upper_bound)
        ASV.__init__(self)

    def show_results(self):
        print(f"""
            Total residents: {self._total_residents}
            Total hospitals: {self._total_hospitals}
            Preferene list length lower bound: {self._lower_bound}
            Preferene list length upper bound: {self._upper_bound}
            Repetitions: {self._total_count}

            Correct: {self._correct_count}
            Incorrect: {self._incorrect_count}
              """)


def main():
    TOTAL_RESIDENTS = 12
    TOTAL_HOSPITALS = 5
    LOWER_LIST_BOUND = 0
    UPPER_LIST_BOUND = 3
    REPETITIONS = 80_000

    start = perf_counter_ns()

    verifier = HRSingleVerifier(
        TOTAL_RESIDENTS, TOTAL_HOSPITALS, LOWER_LIST_BOUND, UPPER_LIST_BOUND
    )
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    end = perf_counter_ns()
    print(f"\nFinal Runtime: {(end - start) / 1000**3}s")

    verifier.show_results()


if __name__ == "__main__":
    main()
