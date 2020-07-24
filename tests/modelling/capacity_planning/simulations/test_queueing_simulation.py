import unittest

from src.modelling.capacity_planning.simulations.queuing import System, Process, Worker


class QueueingSimulationTester(unittest.TestCase):

    def test_construction(self):
        processes = [Process(open_from=60*60*8, close_from=22*60*60, incoming_prob=[10],
                          patience_prob=[5], language="GERMAN", channel="PHONE")]

        workers = [Worker(work_begin=8*60*60, work_end=22*60*60, ahts=[180], channels=["CHAT", "PHONE"],
                        languages=["GERMAN"])]

        callcenter = System(open_time=60*60*8, closed_time=60*60*22, worker=workers,
                            processes=processes, size_waiting_room=None)