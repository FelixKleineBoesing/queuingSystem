import unittest

from src.modelling.capacity_planning.simulations.queuing import Worker, Process, Event, EventType, Customer


class WorkerTester(unittest.TestCase):

    def test_construction(self):
        worker = Worker(work_begin=8*60*60, work_end=22*60*60, ahts=[180], channels=["CHAT", "PHONE"],
                        languages=["GERMAN"])


class ProcessTester(unittest.TestCase):

    def test_construction(self):
        process = Process(open_from=60*60*8, close_from=22*60*60,
                          incoming_prob=[10],
                          patience_prob=[5],
                          language="GERMAN",
                          channel="PHONE")


class EventTester(unittest.TestCase):

    def test_construction(self):
        event = Event(event_type=EventType.incoming_customer, appearance_time=9*60*60, events_to_remove=[1])


class CustomerTester(unittest.TestCase):

    def test_construction(self):
        customer = Customer(patience=5, channel="PHONE", language="GERMAN", retrial=True)