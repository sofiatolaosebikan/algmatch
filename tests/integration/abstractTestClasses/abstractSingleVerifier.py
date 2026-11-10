from tests.integration.abstractTestClasses.abstractVerifier import AbstractVerifier


class AbstractSingleVerifier(AbstractVerifier):
    def __init__(self):
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
