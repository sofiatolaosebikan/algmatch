from tests.integration.SRTests.srSingleVerifier import SRSingleVerifier


class TestSR:
    def test_random_SR(self):
        TOTAL_ROOMMATES = 12
        LOWER_BOUND = 0
        UPPER_BOUND = TOTAL_ROOMMATES - 1
        REPETITIONS = 5_000

        verifier = SRSingleVerifier(TOTAL_ROOMMATES, LOWER_BOUND, UPPER_BOUND)
        for _ in range(REPETITIONS):
            verifier.run()

        assert REPETITIONS == verifier._correct_count
