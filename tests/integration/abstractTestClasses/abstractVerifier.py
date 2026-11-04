class AbstractVerifier:
    def __init__(self, problem, sides, gen, brute_force, stability_type=None):
        self.Problem = problem
        self.sides = sides
        self.BruteForce = brute_force
        self.stability_type = stability_type
        self.gen = gen
        self.current_instance = {}

    def generate_instance(self):
        self.current_instance = self.gen.generate_instance()

    def _construct_bruteforcer(self):
        if self.stability_type is None:
            return self.BruteForce(dictionary=self.current_instance)
        return self.BruteForce(
            dictionary=self.current_instance, stability_type=self.stability_type
        )

    def _construct_solver(self, optimal: bool):
        side = 0 if optimal else 1
        if self.stability_type is None:
            return self.Problem(
                dictionary=self.current_instance,
                optimised_side=self.sides[side],
            )
        return self.Problem(
            dictionary=self.current_instance,
            optimised_side=self.sides[side],
            stability_type=self.stability_type,
        )

    def verify_instance(self):
        # optimal and pessimal from man/resident/student side
        optimal_solver = self._construct_solver(True)
        pessimal_solver = self._construct_solver(False)
        bruteforcer = self._construct_bruteforcer()

        m_0 = optimal_solver.get_stable_matching()
        m_z = pessimal_solver.get_stable_matching()
        bruteforcer.find_stable_matchings()

        if not bruteforcer.stable_matching_list:
            return m_z is None and m_0 is None
        return (
            m_z in bruteforcer.stable_matching_list
            and m_0 in bruteforcer.stable_matching_list
        )

    def run(self):
        raise NotImplementedError("No method for processing instances")

    def show_results(self):
        raise NotImplementedError("No method for outputing the results")
