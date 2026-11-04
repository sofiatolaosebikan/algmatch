from multiprocessing import Lock, Manager, Process
from time import perf_counter_ns, sleep
from tqdm import tqdm

from tests.integration.SRTests.srVerifier import SRVerifier


class SRMultiVerifier(SRVerifier):
    def __init__(self, no_roommates, lower_bound, upper_bound, reps, result_dict):
        SRVerifier.__init__(self, no_roommates, lower_bound, upper_bound)
        self._reps = reps  # per thread

        self.result_dict = result_dict
        self.result_dict["correct"] = 0
        self.result_dict["incorrect"] = 0
        self.result_dict["total"] = 0

        self.lock = Lock()

    def run(self):
        local_correct = 0
        local_incorrect = 0
        local_total = 0

        while local_total < self._reps:
            self.generate_instance()
            if self.verify_instance():
                local_correct += 1
                local_total += 1
                with self.lock:
                    self.result_dict["correct"] += 1
                    self.result_dict["total"] += 1
            else:
                local_incorrect += 1
                local_total += 1
                with self.lock:
                    self.result_dict["incorrect"] += 1
                    self.result_dict["total"] += 1

    def show_results(self):
        print(f"""
            Total roommates: {self._total_roommates}
            Repetitions: {self.result_dict["total"]}

            Correct: {self.result_dict["correct"]}
            Incorrect: {self.result_dict["incorrect"]}
              """)


def main():
    TOTAL_ROOMMATES = 10
    LOWER_BOUND = 0
    UPPER_BOUND = TOTAL_ROOMMATES - 1
    REPETITIONS = 84_000  # per thread
    THREADS = 12

    start = perf_counter_ns()

    with Manager() as manager:
        result_dict = manager.dict()
        verifier = SRMultiVerifier(
            TOTAL_ROOMMATES, LOWER_BOUND, UPPER_BOUND, REPETITIONS, result_dict
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
