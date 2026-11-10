from time import perf_counter_ns
from tqdm import tqdm

from tests.integration.SRTests.srVerifier import SRVerifier


class SRSingleVerifier(SRVerifier):
    def __init__(self, no_roommates, lower_bound, upper_bound):
        SRVerifier.__init__(self, no_roommates, lower_bound, upper_bound)
        self._correct_count = 0
        self._incorrect_count = 0
        self._total_count = 0

    def run(self):
        self.generate_instance()
        if self.verify_instance():
            self._correct_count += 1
            self._total_count += 1
        else:
            self._incorrect_count += 1
            self._total_count += 1

    def show_results(self):
        print(f"""
            Total roommates: {self._total_roommates}
            Repetitions: {self._total_count}

            Correct: {self._correct_count}
            Incorrect: {self._incorrect_count}
              """)


def main():
    TOTAL_ROOMMATES = 12
    LOWER_BOUND = 0
    UPPER_BOUND = TOTAL_ROOMMATES - 1
    REPETITIONS = 50_000

    start = perf_counter_ns()

    verifier = SRSingleVerifier(TOTAL_ROOMMATES, LOWER_BOUND, UPPER_BOUND)
    for _ in tqdm(range(REPETITIONS)):
        verifier.run()

    end = perf_counter_ns()
    print(f"\nFinal Runtime: {(end - start) / 1000**3}s")

    verifier.show_results()


if __name__ == "__main__":
    main()
