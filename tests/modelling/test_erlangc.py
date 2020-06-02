import unittest

from src.modelling.capacity_planning.erlang.erlangc import ErlangC

# TODO add the other method to the tester


class ErlangCTester(unittest.TestCase):

    def test_erlangb_construction(self):
        erlang = ErlangC()

    def get_max_waiting_probability(self, lambda_: float, mu: float, number_agents: int, max_waiting_time: int):
        erlang = ErlangC()
        return erlang.get_max_waiting_probability(lambda_=lambda_, mu=mu, number_agents=number_agents,
                                                  max_waiting_time=max_waiting_time)

    def get_blocking_probability(self, lambda_: float, mu: float, number_agents: int):
        erlang = ErlangC()
        return erlang.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents)

    def get_mean_queue_length(self, lambda_: float, mu: float, number_agents: int):
        erlang = ErlangC()
        return erlang.get_mean_queue_length(lambda_=lambda_, mu=mu, number_agents=number_agents)

    def get_mean_number_customers_in_system(self, lambda_: float, mu: float, number_agents: int):
        erlang = ErlangC()
        return erlang.get_mean_number_customers_in_system(lambda_=lambda_, mu=mu, number_agents=number_agents)

    def get_mean_waiting_time(self, lambda_: float, mu: float, number_agents: int):
        erlang = ErlangC()
        return erlang.get_mean_waiting_time(lambda_=lambda_, mu=mu, number_agents=number_agents)

    def get_number_agents_for_chat(self, lambda_: float, mu: float, abort_prob: float, max_sessions: int,
                                   share_sequential_work: float, max_waiting_time: int):
        erlang = ErlangC()
        return erlang.get_number_agents_for_chat(lambda_=lambda_, mu=mu,
                                                 abort_prob=abort_prob, max_sessions=max_sessions,
                                                 share_sequential_work=share_sequential_work,
                                                 max_waiting_time=max_waiting_time)

    def test_get_max_waiting_probability(self):
        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=35, max_waiting_time=20)
        self.assertEqual(prob, 0.7710233599946846)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=135, max_waiting_time=10)
        self.assertEqual(prob, 1)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.133, number_agents=50, max_waiting_time=200)
        self.assertEqual(prob, 1)

        prob = self.get_max_waiting_probability(lambda_=1, mu=0.0038, number_agents=35, max_waiting_time=20)
        self.assertEqual(prob, 0)

        prob = self.get_max_waiting_probability(lambda_=10, mu=0.12, number_agents=35, max_waiting_time=20)
        self.assertEqual(prob, 0)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=3.0033, number_agents=35, max_waiting_time=20)
        self.assertEqual(prob, 1.0)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=40, max_waiting_time=20)
        self.assertEqual(prob, 0.9668921807646333)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=20, max_waiting_time=20)
        self.assertEqual(prob, 0)

    def test_get_blocking_probability(self):
        prob = self.get_blocking_probability(lambda_=0.1, mu=0.0033, number_agents=35)
        self.assertEqual(prob, 0.3121925015328496)

        prob = self.get_blocking_probability(lambda_=0.1, mu=0.0033, number_agents=135)
        self.assertEqual(prob, 3.3170371593189645e-44)

        prob = self.get_blocking_probability(lambda_=0.1, mu=0.133, number_agents=50)
        self.assertEqual(prob, 1.010150818440181e-71)

        prob = self.get_blocking_probability(lambda_=0.001, mu=0.0038, number_agents=35)
        self.assertEqual(prob, 3.8223562208774564e-61)

        prob = self.get_blocking_probability(lambda_=120, mu=5, number_agents=35)
        self.assertEqual(prob, 0.023521116861458607)

        prob = self.get_blocking_probability(lambda_=90, mu=3.0033, number_agents=35)
        self.assertEqual(prob, 0.2816872350258893)

        prob = self.get_blocking_probability(lambda_=0.1, mu=0.0033, number_agents=40)
        self.assertEqual(prob, 0.06278834613535761)

        prob = self.get_blocking_probability(lambda_=0.1, mu=0.0033, number_agents=20)
        self.assertEqual(prob, 0)

    def test_get_number_agents_for_chat(self):
        number_agents = self.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, abort_prob=0.2,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=20)
        self.assertEqual(number_agents, 2.5)

        number_agents = self.get_number_agents_for_chat(lambda_=20/3600, mu=2/180, abort_prob=0.2,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=20)
        self.assertEqual(number_agents, 2.0)

        number_agents = self.get_number_agents_for_chat(lambda_=2/3600, mu=3/180, abort_prob=0.2,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=20)
        self.assertEqual(number_agents, 0.5)

        number_agents = self.get_number_agents_for_chat(lambda_=24/3600, mu=1/180, abort_prob=0.1,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=20)
        self.assertEqual(number_agents, 4.5)

        number_agents = self.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, abort_prob=0.15,
                                                        max_sessions=2, share_sequential_work=0.25, max_waiting_time=35)
        self.assertEqual(number_agents, 1.0)

        number_agents = self.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, abort_prob=0.2,
                                                        max_sessions=10, share_sequential_work=0.05, max_waiting_time=60)
        self.assertEqual(number_agents, 0.1)

        number_agents = self.get_number_agents_for_chat(lambda_=12/3600, mu=3/180, abort_prob=0.3,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=10)
        self.assertEqual(number_agents, 1.0)