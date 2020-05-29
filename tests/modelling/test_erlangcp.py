import unittest

from src.modelling.capacity_planning.erlang.erlanga import ErlangCP

# TODO add the other methods to the tester


class ErlangCPTester(unittest.TestCase):

    def test_erlangb_construction(self):
        erlang = ErlangCP()

    def get_max_waiting_probability(self, lambda_: float, mu: float, number_agents: int, max_waiting_time: int,
                                    nu: float, size_waiting_room: int):
        erlang = ErlangCP()
        return erlang.get_max_waiting_probability(lambda_=lambda_, mu=mu, number_agents=number_agents,
                                                  max_waiting_time=max_waiting_time, nu=nu,
                                                  size_waiting_room=size_waiting_room)

    def get_abort_probability(self, lambda_: float, mu: float, number_agents: int,
                              nu: float, size_waiting_room: int):
        erlang = ErlangCP()
        return erlang.get_prob_for_abort(lambda_=lambda_, mu=mu, number_agents=number_agents, nu=nu,
                                         size_waiting_room=size_waiting_room)

    def get_mean_staying_time(self, lambda_: float, mu: float, number_agents: int,
                              nu: float, size_waiting_room: int):
        erlang = ErlangCP()
        return erlang.get_mean_staying_time(lambda_=lambda_, mu=mu, number_agents=number_agents, nu=nu,
                                            size_waiting_room=size_waiting_room)

    def get_mean_queue_length(self, lambda_: float, mu: float, number_agents: int,
                              nu: float, size_waiting_room: int):
        erlang = ErlangCP()
        return erlang.get_mean_queue_length(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                            size_waiting_room=size_waiting_room)

    def get_mean_number_customer_in_system(self, lambda_: float, mu: float, number_agents: int,
                                           nu: float, size_waiting_room: int):
        erlang = ErlangCP()
        return erlang.get_mean_number_customer_in_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                         size_waiting_room=size_waiting_room)

    def get_number_agents_for_service_level(self, target_sla: float, lambda_: float, mu: float, max_waiting_time: int,
                                            nu: float, size_waiting_room: int):
        erlang = ErlangCP()
        return erlang.get_number_agents_for_service_level(lambda_=lambda_, mu=mu, nu=nu, target_sla=target_sla,
                                                          size_waiting_room=size_waiting_room,
                                                          max_waiting_time=max_waiting_time)

    def test_get_max_waiting_probability(self):
        prob = self.get_max_waiting_probability(lambda_=1/10, mu=1/240, nu=1/300, number_agents=28, max_waiting_time=20,
                                                size_waiting_room=80)
        self.assertEqual(prob, 0.8633721956843062)

        prob = self.get_max_waiting_probability(lambda_=1/11, mu=1/240, nu=1 / 300, number_agents=28,
                                                max_waiting_time=20,
                                                size_waiting_room=80)
        self.assertEqual(prob, 0.9419524522175644)

        prob = self.get_max_waiting_probability(lambda_=1/10, mu=1/240, nu=1/280, number_agents=27, max_waiting_time=22,
                                                size_waiting_room=79)
        self.assertEqual(prob, 0.8275267870257028)

        prob = self.get_max_waiting_probability(lambda_=1/10, mu=1/250, nu=1/290, number_agents=24, max_waiting_time=10,
                                                size_waiting_room=60)
        self.assertEqual(prob, 0.44899132283954957)

