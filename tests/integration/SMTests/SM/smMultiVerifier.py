from multiprocessing import Manager, Process
from time import perf_counter_ns, sleep
from tqdm import tqdm

from tests.integration.SMTests.SM.smVerifier import SMVerifier as SMV
from tests.integration.abstractTestClasses.abstractMultiVerifier import (
    AbstractMultiVerifier as AMV,
)


class SMMultiVerifier(SMV, AMV):
    def __init__(
        self, total_men, total_women, lower_bound, upper_bound, reps, result_dict
    ):
        SMV.__init__(self, total_men, total_women, lower_bound, upper_bound)
        AMV.__init__(self, reps, result_dict)

    def show_results(self):
        print(f"""
            Total men: {self._total_men}
            Total women: {self._total_women}
            Preference list length lower bound: {self._lower_bound}
            Preference list length upper bound: {self._upper_bound}
            Repetitions: {self.result_dict["total"]}

            Correct: {self.result_dict["correct"]}
            Incorrect: {self.result_dict["incorrect"]}
              """)


def main():
    n = 5
    TOTAL_MEN = n
    TOTAL_WOMEN = n
    LOWER_LIST_BOUND = n
    UPPER_LIST_BOUND = n
    REPETITIONS = 10_000  # per thread
    THREADS = 4

    start = perf_counter_ns()

    with Manager() as manager:
        result_dict = manager.dict()
        verifier = SMMultiVerifier(
            TOTAL_MEN,
            TOTAL_WOMEN,
            LOWER_LIST_BOUND,
            UPPER_LIST_BOUND,
            REPETITIONS,
            result_dict,
        )
        v_threads = []
        for _ in range(THREADS):
            thread = Process(target=verifier.run)
            v_threads.append(thread)

        for v_t in v_threads:
            v_t.start()

        with tqdm(total=REPETITIONS * THREADS) as pbar:
            while any(thread.is_alive() for thread in v_threads):
                sleep(0.25)
                pbar.n = verifier.result_dict["total"]
                pbar.last_print_n = pbar.n
                pbar.update(0)

        for v_t in v_threads:
            v_t.join()

        end = perf_counter_ns()
        print(f"\nFinal Runtime: {(end - start) / 1000**3}s")

        verifier.show_results()


if __name__ == "__main__":
    main()
