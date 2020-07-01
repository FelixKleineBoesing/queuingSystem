from modelling.capacity_planning.optimizer import Optimizer


class OutboundCalculator(Optimizer):

    def get_number_agents(self, lambda_: float, dialing_time: int, netto_contact_rate: float,
                          right_person_contact_rate: float, mu_right_person: float, mu_wrong_person: float):
        ((netto_contact_rate * right_person_contact_rate) / lambda_) * ((1 / mu_right_person + dialing_time))
        pass

    def get_number_contacts(self):
        pass
