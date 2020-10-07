import unittest
import numpy as np

from src.modelling.capacity_planning.simulations.custom.sim_parts import Process, Worker
from src.modelling.capacity_planning.simulations.custom.simulation import CallCenterSimulation
from src.modelling.capacity_planning.simulations.probability_classes import ErlangDistribution


class SystemTester(unittest.TestCase):

    def test_construction(self):
        processes = [Process(open_from=60*60*8, close_from=22*60*60, incoming_prob=ErlangDistribution(lambda_=10),
                             patience_prob=[5], language="GERMAN", channel="PHONE")]

        workers = [Worker(work_begin=8*60*60, work_end=22*60*60, ahts=[180], channels=["CHAT", "PHONE"],
                          languages=["GERMAN"])]

        callcenter = CallCenterSimulation(open_time=60 * 60 * 8, closed_time=60 * 60 * 22, worker=workers,
                                          processes=processes, size_waiting_room=None)

    def test_run(self):
        processes = [Process(open_from=60*60*8, close_from=22*60*60, incoming_prob=ErlangDistribution(lambda_=8),
                             patience_prob=[0], language="GERMAN", channel="PHONE")]

        workers = [Worker(work_begin=8*60*60, work_end=22*60*60, ahts=[180], channels=["CHAT", "PHONE"],
                          languages=["GERMAN"]) for _ in range(10)]

        callcenter = CallCenterSimulation(open_time=60 * 60 * 8, closed_time=60 * 60 * 22, worker=workers,
                                          processes=processes, size_waiting_room=None,
                                          stopping_criterita={"max_events": 30000})

        callcenter.run()
        stats = callcenter.statistics
        event_variables = stats["events"]["variable"]
        unique, counts = np.unique(event_variables, return_counts=True)
        numbers = dict(zip(unique, counts))
        if "abandoned_customer" not in numbers:
            numbers["abandoned_customer"] = 0
        service_level = numbers["abandoned_customer"] / numbers["incoming_customer"]
        print(service_level)
