from algmatch.stableMarriageProblem import StableMarriageProblem

from tests.integration.abstractTestClasses.abstractVerifier import AbstractVerifier
from algmatch.utils import SMGenerator
from algmatch.utils import SMEnumerator


class SMVerifier(AbstractVerifier):
    def __init__(self, total_men, total_women, lower_bound, upper_bound):
        """
        It takes argument as follows (set in init):
            number of men
            number of women
            lower bound of the preference list length
            upper bound of the preference list length
        """

        self._total_men = total_men
        self._total_women = total_women
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

        generator = SMGenerator(total_men, total_women, lower_bound, upper_bound)

        AbstractVerifier.__init__(
            self,
            StableMarriageProblem,
            ("men", "women"),
            generator,
            SMEnumerator,
        )
