from multiprocessing import Manager, Process
from time import perf_counter_ns, sleep
from tqdm import tqdm

from tests.integration.abstractTestClasses.abstractMultiVerifier import (
    AbstractMultiVerifier,
)
from tests.integration.SPASTests.SPASTSuper.spastSuperVerifier import SPASTSuperVerifier


class SPASTSuperMultiVerifier(SPASTSuperVerifier, AbstractMultiVerifier):
    def __init__(
        self,
        total_students,
        total_projects,
        total_lecturers,
        lower_bound,
        upper_bound,
        reps,
        result_dict,
    ):
        SPASTSuperVerifier.__init__(
            self,
            total_students,
            total_projects,
            total_lecturers,
            lower_bound,
            upper_bound,
        )
        AbstractMultiVerifier.__init__(self, reps, result_dict)

    def show_results(self):
        print(f"""
            Total students: {self._total_students}
            Total projects: {self._total_projects}
            Total lecturers: {self._total_lecturers}
            Lower list bound: {self._lower_bound}
            Upper list bound: {self._upper_bound}
            Repetitions: {self.result_dict["total"]}

            Correct: {self.result_dict["correct"]}
            Incorrect: {self.result_dict["incorrect"]}
              """)


def main():
    TOTAL_STUDENTS = 12
    TOTAL_PROJECTS = 5
    TOTAL_LECTURERS = 3
    LOWER_BOUND = 0
    UPPER_BOUND = 5
    REPETITIONS = 100  # per thread
    THREADS = 1

    start = perf_counter_ns()

    with Manager() as manager:
        result_dict = manager.dict()
        verifier = SPASTSuperMultiVerifier(
            TOTAL_STUDENTS,
            TOTAL_PROJECTS,
            TOTAL_LECTURERS,
            LOWER_BOUND,
            UPPER_BOUND,
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
