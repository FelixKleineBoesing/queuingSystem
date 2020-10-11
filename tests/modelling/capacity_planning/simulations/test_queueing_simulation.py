import unittest
import numpy as np

from src.modelling.capacity_planning.erlang.erlangc import ErlangC
from src.modelling.capacity_planning.simulations.custom.sim_parts import Process, Worker, StatisticsContainer
from src.modelling.capacity_planning.simulations.custom.simulation import CallCenterSimulation
from src.modelling.capacity_planning.simulations.probability_classes import ErlangDistribution, NormalDistribution, \
    ListDrawer


class SystemTester(unittest.TestCase):

    def test_construction(self):
        processes = [Process(open_from=60*60*8, close_from=22*60*60, incoming_prob=ErlangDistribution(lambda_=10),
                             patience_prob=ListDrawer([5]), language="GERMAN", channel="PHONE")]

        workers = [Worker(work_begin=8*60*60, work_end=22*60*60, ahts=NormalDistribution(mean=180, sd=20),
                          channels=["CHAT", "PHONE"], languages=["GERMAN"])]

        callcenter = CallCenterSimulation(open_time=60 * 60 * 8, closed_time=60 * 60 * 22, worker=workers,
                                          processes=processes, size_waiting_room=None)

    def test_run(self):
        processes = [Process(open_from=60*60*8, close_from=22*60*60, incoming_prob=ErlangDistribution(lambda_=10),
                             patience_prob=ListDrawer([999999]), language="GERMAN", channel="PHONE")]

        workers = [Worker(work_begin=8*60*60, work_end=22*60*60, ahts=NormalDistribution(mean=180, sd=10),
                          channels=["CHAT", "PHONE"], languages=["GERMAN"]) for _ in range(20)]

        callcenter = CallCenterSimulation(open_time=60 * 60 * 8, closed_time=60 * 60 * 22, worker=workers,
                                          processes=processes, size_waiting_room=None,
                                          stopping_criterita={"max_events": 10000})

        callcenter.run()
        stats = callcenter.statistics
        stats = StatisticsContainer(stats)

        erlang = ErlangC()
        print(1 - erlang.get_max_waiting_probability(lambda_=1/10, mu=1/180, number_agents=20, max_waiting_time=20))
        print(stats.get_service_level(20))
