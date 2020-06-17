import unittest

from src.modelling.capacity_planning.erlang.erlanga import ErlangA, get_cn_for_mmckm_system, \
    get_prob_for_pn_in_mmckm_system


# TODO add the other methods to the tester


class ErlangATester(unittest.TestCase):

    def test_erlangb_construction(self):
        erlang = ErlangA()

    def get_max_waiting_probability(self, lambda_: float, mu: float, number_agents: int, max_waiting_time: int,
                                    nu: float, size_waiting_room: int):
        erlang = ErlangA()
        return erlang.get_max_waiting_probability(lambda_=lambda_, mu=mu, number_agents=number_agents,
                                                  max_waiting_time=max_waiting_time, nu=nu,
                                                  size_waiting_room=size_waiting_room)

    def get_abort_probability(self, lambda_: float, mu: float, number_agents: int,
                              nu: float, size_waiting_room: int):
        erlang = ErlangA()
        return erlang.get_prob_for_abort(lambda_=lambda_, mu=mu, number_agents=number_agents, nu=nu,
                                         size_waiting_room=size_waiting_room)

    def get_mean_staying_time(self, lambda_: float, mu: float, number_agents: int,
                              nu: float, size_waiting_room: int):
        erlang = ErlangA()
        return erlang.get_average_staying_time(lambda_=lambda_, mu=mu, number_agents=number_agents, nu=nu,
                                               size_waiting_room=size_waiting_room)

    def get_mean_waiting_time(self, lambda_: float, mu: float, number_agents: int,
                              nu: float, size_waiting_room: int):
        erlang = ErlangA()
        return erlang.get_average_waiting_time(lambda_=lambda_, mu=mu, number_agents=number_agents, nu=nu,
                                               size_waiting_room=size_waiting_room)

    def get_mean_queue_length(self, lambda_: float, mu: float, number_agents: int,
                              nu: float, size_waiting_room: int):
        erlang = ErlangA()
        return erlang.get_average_queue_length(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                               size_waiting_room=size_waiting_room)

    def get_mean_number_customer_in_system(self, lambda_: float, mu: float, number_agents: int,
                                           nu: float, size_waiting_room: int):
        erlang = ErlangA()
        return erlang.get_average_number_customers_in_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                             size_waiting_room=size_waiting_room)

    def get_number_agents_for_service_level(self, target_sla: float, lambda_: float, mu: float, max_waiting_time: int,
                                            nu: float, size_waiting_room: int):
        erlang = ErlangA()
        return erlang.get_number_agents_for_service_level(lambda_=lambda_, mu=mu, nu=nu, target_sla=target_sla,
                                                          size_waiting_room=size_waiting_room,
                                                          max_waiting_time=max_waiting_time)

    def test_get_prob_for_pn_in_mmckm_system(self):
        prob = get_prob_for_pn_in_mmckm_system(lambda_=0.1, mu=1/240, nu=1/300, number_agents=28,
                                               size_waiting_room=80, persons_in_system=30)
        self.assertEqual(prob, 0.03655086716188359)

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

    def test_get_abort_probability(self):
        prob = self.get_abort_probability(lambda_=1/10, mu=1/240, nu=1/30, number_agents=25, size_waiting_room=80)
        self.assertEqual(prob, 0.09759081562546817)

    def test_mean_queue_length(self):
        mean_queue = self.get_mean_queue_length(lambda_=0.1, mu=1/240, nu=1/300, number_agents=28,
                                                size_waiting_room=80)
        self.assertEqual(mean_queue, 0.6833261838358367)

    def test_mean_customers_in_system(self):
        mean_custs = self.get_mean_number_customer_in_system(lambda_=0.1, mu=1/240, nu=1/300, number_agents=28,
                                                             size_waiting_room=80)
        self.assertEqual(mean_custs, 24.136665236767172)

    def test_get_mean_waiting_time(self):
        mean_waiting_time = self.get_mean_waiting_time(lambda_=0.1, mu=1/240, nu=1/300, number_agents=28,
                                                       size_waiting_room=80)
        self.assertEqual(mean_waiting_time, 6.833261838358366)

    def test_get_staying_time(self):
        mean_staying_time = self.get_mean_staying_time(lambda_=0.1, mu=1/240, nu=1/300, number_agents=28,
                                                       size_waiting_room=80)
        self.assertEqual(mean_staying_time, 241.36665236767172)