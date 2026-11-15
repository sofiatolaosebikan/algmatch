from numpy import arange

from tests.integration.SMTests.SM.smSingleVerifier import SMSingleVerifier
from tests.integration.SMTests.SMTStrong.smtStrongSingleVerifier import (
    SMTStrongSingleVerifier,
)
from tests.integration.SMTests.SMTSuper.smtSuperSingleVerifier import (
    SMTSuperSingleVerifier,
)


class TestSM:
    n = 6
    M = n
    W = n
    LB = 0
    UB = n

    def test_random_SM(self):
        REPETITIONS = 5_000

        verifier = SMSingleVerifier(self.M, self.W, self.LB, self.UB)
        for _ in range(REPETITIONS):
            verifier.run()

        assert REPETITIONS == verifier._correct_count

    def test_random_SMT_strong(self):
        TIE_DENSITY_STEPS = 10
        REPS_PER_TDS = 500

        td_step_size = 1 / TIE_DENSITY_STEPS
        td_values = arange(0, 1 + td_step_size / 2, td_step_size)

        verifier = SMTStrongSingleVerifier(self.M, self.W, self.LB, self.UB)
        for td in td_values:
            verifier.gen.set_tie_density(td)
            for _ in range(REPS_PER_TDS):
                verifier.run()

        assert REPS_PER_TDS * (TIE_DENSITY_STEPS + 1) == verifier._correct_count

    def test_random_SMT_super(self):
        TIE_DENSITY_STEPS = 10
        REPS_PER_TDS = 500

        td_step_size = 1 / TIE_DENSITY_STEPS
        td_values = arange(0, 1 + td_step_size / 2, td_step_size)

        verifier = SMTSuperSingleVerifier(self.M, self.W, self.LB, self.UB)
        for td in td_values:
            verifier.gen.set_tie_density(td)
            for _ in range(REPS_PER_TDS):
                verifier.run()

        assert REPS_PER_TDS * (TIE_DENSITY_STEPS + 1) == verifier._correct_count
