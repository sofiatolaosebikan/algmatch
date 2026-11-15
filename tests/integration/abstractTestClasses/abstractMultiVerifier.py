from multiprocessing import Lock

from tests.integration.abstractTestClasses.abstractVerifier import AbstractVerifier


class AbstractMultiVerifier(AbstractVerifier):
    def __init__(self, reps, result_dict):
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
