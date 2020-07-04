from src.modelling.capacity_planning.optimizer_arguments import OptimizerArguments, ArgumentParams


class OutboundArgumentsMixin(OptimizerArguments):

    def __init__(self):
        self._start_functions = {}
        self.argument_params = {
            "lambda_": ArgumentParams(lower_bound=0),
            "dialing_time": ArgumentParams(lower_bound=0),
            "nett_contact_rate": ArgumentParams(lower_bound=0, upper_bound=1),
            "right_person_contact_rate": ArgumentParams(lower_bound=0, upper_bound=1),
            "mu_right_person": ArgumentParams(lower_bound=0),
            "mu_wrong_person": ArgumentParams(lower_bound=0),
            "number_agents": ArgumentParams(lower_bound=1)
        }
        super().__init__()

