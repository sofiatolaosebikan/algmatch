from algmatch import HRT
from algmatch.utils import HRTEnumerator, HRTGenerator

from tests.integration.abstractTestClasses.abstractVerifier import AbstractVerifier


class HRTSuperVerifier(AbstractVerifier):
    def __init__(self, total_residents, total_hospitals, lower_bound, upper_bound):
        """
        It takes argument as follows (set in init):
            number of residents
            number of hospitals
            lower bound of the preference list length
            upper bound of the preference list length
        """

        self._total_residents = total_residents
        self._total_hospitals = total_hospitals
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

        generator = HRTGenerator(
            total_residents, total_hospitals, lower_bound, upper_bound
        )

        AbstractVerifier.__init__(
            self,
            HRT,
            ("residents", "hospitals"),
            generator,
            HRTEnumerator,
            "super",
        )
