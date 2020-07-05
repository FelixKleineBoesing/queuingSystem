

class BackOfficeCalculator:

    def get_required_agents(self, lambdas: list, mus: list, open_index: int, closed_index: int,
                            backlog_within: int, occupancy: float):
        assert len(lambdas) == len(mus)
        assert closed_index < len(lambdas)
        assert open_index < len(lambdas)
        assert open_index < closed_index
        assert closed_index - open_index + 1 == len(mus), "mus must be as long as the interval from open to closed"
        
        pass