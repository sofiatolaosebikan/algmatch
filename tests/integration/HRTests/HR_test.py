from numpy import arange

from tests.integration.HRTests.HR.hrSingleVerifier import HRSingleVerifier
from tests.integration.HRTests.HRTStrong.hrtStrongSingleVerifier import (
    HRTStrongSingleVerifier,
)
from tests.integration.HRTests.HRTSuper.hrtSuperSingleVerifier import (
    HRTSuperSingleVerifier,
)


class TestHR:
    R = 7
    H = 3
    LB = 0
    UB = 3

    def test_random_HR(self):
        REPETITIONS = 5_000

        verifier = HRSingleVerifier(self.R, self.H, self.LB, self.UB)
        for _ in range(REPETITIONS):
            verifier.run()

        assert REPETITIONS == verifier._correct_count

    def test_random_HRT_strong(self):
        TIE_DENSITY_STEPS = 10
        REPS_PER_TDS = 500

        td_step_size = 1 / TIE_DENSITY_STEPS
        td_values = arange(0, 1 + td_step_size / 2, td_step_size)

        verifier = HRTStrongSingleVerifier(self.R, self.H, self.LB, self.UB)
        for td in td_values:
            verifier.gen.set_tie_density(td)
            for _ in range(REPS_PER_TDS):
                verifier.run()

        assert REPS_PER_TDS * (TIE_DENSITY_STEPS + 1) == verifier._correct_count

    def test_random_HRT_super(self):
        TIE_DENSITY_STEPS = 10
        REPS_PER_TDS = 500

        td_step_size = 1 / TIE_DENSITY_STEPS
        td_values = arange(0, 1 + td_step_size / 2, td_step_size)

        verifier = HRTSuperSingleVerifier(self.R, self.H, self.LB, self.UB)
        for td in td_values:
            verifier.gen.set_tie_density(td)
            for _ in range(REPS_PER_TDS):
                verifier.run()

        assert REPS_PER_TDS * (TIE_DENSITY_STEPS + 1) == verifier._correct_count
