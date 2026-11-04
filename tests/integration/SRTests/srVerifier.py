from algmatch import SR
from algmatch.utils import SREnumerator, SRGenerator


class SRVerifier:
    def __init__(self, no_roommates, lower_bound, upper_bound):
        self._total_roommates = no_roommates
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self.gen = SRGenerator(no_roommates, lower_bound, upper_bound)
        self.current_instance = {}

    def generate_instance(self):
        self.current_instance = self.gen.generate_instance()

    def verify_instance(self):
        bruteforcer = SREnumerator(dictionary=self.current_instance)
        solver = SR(dictionary=self.current_instance)

        bruteforcer.find_stable_matchings()
        matching = solver.get_stable_matching()

        if not bruteforcer.stable_matching_list:
            if matching is None:
                return True
            return False

        if matching not in bruteforcer.stable_matching_list:
            return False
        return True

    def run(self):
        raise NotImplementedError("No method for processing instances")

    def show_results(self):
        raise NotImplementedError("No method for outputing the results")
