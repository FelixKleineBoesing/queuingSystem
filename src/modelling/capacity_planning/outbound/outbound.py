from src.modelling.capacity_planning.optimizer import Optimizer
from src.modelling.capacity_planning.outbound.outbound_arguments_mixin import OutboundArgumentsMixin


class OutboundCalculator(Optimizer, OutboundArgumentsMixin):

    def get_number_agents(self, lambda_: float, dialing_time: float, netto_contact_rate: float,
                          right_person_contact_rate: float, mu_correct: float, mu_wrong: float):
        val = (netto_contact_rate * right_person_contact_rate * lambda_) * (1 / mu_correct + 1 / dialing_time) + \
              ((lambda_ * netto_contact_rate) - (netto_contact_rate * right_person_contact_rate * lambda_)) *\
              (1 / mu_wrong + 1 / dialing_time)
        return val

    def get_volume(self, dialing_time: float, netto_contact_rate: float, right_person_contact_rate: float,
                   mu_correct: float, mu_wrong: float, number_agents: float):
        # TODO transform the equation to eliminate interval
        val = number_agents / (((netto_contact_rate * right_person_contact_rate) * (1 / mu_correct + 1 / dialing_time)) +
                               (netto_contact_rate - netto_contact_rate * right_person_contact_rate) * (1 / dialing_time + 1 / mu_wrong))

        return val
