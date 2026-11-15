from time import perf_counter_ns
from tqdm import tqdm

from tests.integration.abstractTestClasses.abstractSingleVerifier import (
    AbstractSingleVerifier as ASV,
)
from tests.integration.SMTests.SM.smVerifier import SMVerifier as SMV


class SMSingleVerifier(SMV, ASV):
    def __init__(self, total_men, total_women, lower_bound, upper_bound):
        SMV.__init__(self, total_men, total_women, lower_bound, upper_bound)
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
    LOWER_LIST_BOUND = n
    UPPER_LIST_BOUND = n
    REPETITIONS = 40_000

    start = perf_counter_ns()

    verifier = SMSingleVerifier(
        TOTAL_MEN, TOTAL_WOMEN, LOWER_LIST_BOUND, UPPER_LIST_BOUND
    )
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    end = perf_counter_ns()
    print(f"\nFinal Runtime: {(end - start) / 1000**3}s")

    verifier.show_results()


if __name__ == "__main__":
    main()
