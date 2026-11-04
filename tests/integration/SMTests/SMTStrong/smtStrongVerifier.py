from algmatch import SMT
from algmatch.utils import SMTGenerator, SMTEnumerator

from tests.integration.abstractTestClasses.abstractVerifier import AbstractVerifier


class SMTStrongVerifier(AbstractVerifier):
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

        generator = SMTGenerator(total_men, total_women, lower_bound, upper_bound)

        AbstractVerifier.__init__(
            self,
            SMT,
            ("men", "women"),
            generator,
            SMTEnumerator,
            "strong",
        )
