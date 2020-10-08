import unittest

from src.modelling.capacity_planning.erlang.erlangc import ErlangC, get_p0_for_mmc_system

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
        return erlang.get_average_queue_length(lambda_=lambda_, mu=mu, number_agents=number_agents)

    def get_mean_number_customers_in_system(self, lambda_: float, mu: float, number_agents: int):
        erlang = ErlangC()
        return erlang.get_average_number_customers_in_system(lambda_=lambda_, mu=mu, number_agents=number_agents)

    def get_mean_waiting_time(self, lambda_: float, mu: float, number_agents: int):
        erlang = ErlangC()
        return erlang.get_average_waiting_time(lambda_=lambda_, mu=mu, number_agents=number_agents)

    def get_mean_staying_time(self, lambda_: float, mu: float, number_agents: int):
        erlang = ErlangC()
        return erlang.get_average_staying_time(lambda_=lambda_, mu=mu, number_agents=number_agents)

    def get_number_agents_for_chat(self, lambda_: float, mu: float, service_level: float, max_sessions: int,
                                   share_sequential_work: float, max_waiting_time: int):
        erlang = ErlangC()
        return erlang.get_number_agents_for_chat(lambda_=lambda_, mu=mu,
                                                 service_level=service_level, max_sessions=max_sessions,
                                                 share_sequential_work=share_sequential_work,
                                                 max_waiting_time=max_waiting_time)

    def test_get_max_waiting_probability(self):
        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=35, max_waiting_time=20)
        self.assertAlmostEqual(prob, 0.7710233599946846, places=7)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=35, max_waiting_time=20)
        self.assertAlmostEqual(prob, 0.7710233599946846, places=7)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=135, max_waiting_time=10)
        self.assertAlmostEqual(prob, 1, places=7)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.133, number_agents=50, max_waiting_time=200)
        self.assertAlmostEqual(prob, 1, places=7)

        prob = self.get_max_waiting_probability(lambda_=1, mu=0.0038, number_agents=35, max_waiting_time=20)
        self.assertAlmostEqual(prob, 0, places=7)

        prob = self.get_max_waiting_probability(lambda_=10, mu=0.12, number_agents=35, max_waiting_time=20)
        self.assertAlmostEqual(prob, 0, places=7)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=3.0033, number_agents=35, max_waiting_time=20)
        self.assertAlmostEqual(prob, 1.0, places=7)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=40, max_waiting_time=20)
        self.assertAlmostEqual(prob, 0.9668921807646333, places=7)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=20, max_waiting_time=20)
        self.assertAlmostEqual(prob, 0, places=7)

    def test_get_blocking_probability(self):
        prob = self.get_blocking_probability(lambda_=1/36, mu=1/180, number_agents=10)
        self.assertAlmostEqual(prob, 0.03610535915832015, places=7)

        prob = self.get_blocking_probability(lambda_=0.1, mu=0.0033, number_agents=35)
        self.assertAlmostEqual(prob, 0.3121925015328496, places=7)

        prob = self.get_blocking_probability(lambda_=0.1, mu=0.0033, number_agents=135)
        self.assertAlmostEqual(prob, 3.3170371593189645e-44, places=7)

        prob = self.get_blocking_probability(lambda_=0.1, mu=0.133, number_agents=50)
        self.assertAlmostEqual(prob, 1.010150818440181e-71, places=7)

        prob = self.get_blocking_probability(lambda_=0.001, mu=0.0038, number_agents=35)
        self.assertAlmostEqual(prob, 3.8223562208774564e-61, places=7)

        prob = self.get_blocking_probability(lambda_=120, mu=5, number_agents=35)
        self.assertAlmostEqual(prob, 0.023521116861458607, places=7)

        prob = self.get_blocking_probability(lambda_=90, mu=3.0033, number_agents=35)
        self.assertAlmostEqual(prob, 0.2816872350258893, places=7)

        prob = self.get_blocking_probability(lambda_=0.1, mu=0.0033, number_agents=40)
        self.assertAlmostEqual(prob, 0.06278834613535761, places=7)

        prob = self.get_blocking_probability(lambda_=0.1, mu=0.0033, number_agents=20)
        self.assertAlmostEqual(prob, 0, places=7)

    def test_get_number_agents_for_chat(self):
        number_agents = self.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, service_level=0.8,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=20)
        self.assertAlmostEqual(number_agents, 4.0, places=7)

        number_agents = self.get_number_agents_for_chat(lambda_=20/3600, mu=2/180, service_level=0.5,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=20)
        self.assertAlmostEqual(number_agents, 3.0, places=7)

        number_agents = self.get_number_agents_for_chat(lambda_=2/3600, mu=3/180, service_level=0.8,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=20)
        self.assertAlmostEqual(number_agents, 1.0, places=7)

        number_agents = self.get_number_agents_for_chat(lambda_=24/3600, mu=1/180, service_level=0.9,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=20)
        self.assertAlmostEqual(number_agents, 7.0, places=7)

        number_agents = self.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, service_level=0.85,
                                                        max_sessions=2, share_sequential_work=0.25, max_waiting_time=35)
        self.assertAlmostEqual(number_agents, 3.0, places=7)

        number_agents = self.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, service_level=0.8,
                                                        max_sessions=10, share_sequential_work=0.05, max_waiting_time=60)
        self.assertAlmostEqual(number_agents, 1.0, places=7)

        number_agents = self.get_number_agents_for_chat(lambda_=12/3600, mu=3/180, service_level=0.7,
                                                        max_sessions=2, share_sequential_work=0.15, max_waiting_time=10)
        self.assertAlmostEqual(number_agents, 2.0, places=7)

    def test_get_mean_queue_length(self):
        mean_queue_length = self.get_mean_queue_length(lambda_=7, mu=1, number_agents=9)
        self.assertAlmostEqual(mean_queue_length, 1.3473148295486905, places=7)

    def test_get_mean_number_customers_in_system(self):
        mean_cust_system = self.get_mean_number_customers_in_system(lambda_=7, mu=1, number_agents=9)
        self.assertAlmostEqual(mean_cust_system, 8.34731482954869, places=7)

    def test_get_mean_waiting_time(self):
        mean_waiting_time = self.get_mean_waiting_time(lambda_=0.1, mu=1/300, number_agents=35)
        self.assertAlmostEqual(mean_waiting_time, 17.07494774481045, places=7)

    def test_get_mean_staying_time(self):
        mean_staying_time = self.get_mean_staying_time(lambda_=0.1, mu=1/300, number_agents=35)
        self.assertAlmostEqual(mean_staying_time, 317.07494774481045, places=7)