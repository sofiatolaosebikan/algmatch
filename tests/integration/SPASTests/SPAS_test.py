from tests.integration.SPASTests.SPAS.spasSingleVerifier import SPASSingleVerifier


class TestSPAS:
    S = 6
    P = 3
    L = 2
    LB = 0
    UB = 3

    def test_random_SPAS(self):
        REPETITIONS = 5_000

        verifier = SPASSingleVerifier(self.S, self.P, self.L, self.LB, self.UB)
        for _ in range(REPETITIONS):
            verifier.run()

        assert REPETITIONS == verifier._correct_count
