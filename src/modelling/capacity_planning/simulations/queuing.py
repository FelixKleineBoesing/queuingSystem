from sortedcontainers import SortedList
from typing import List
import numpy as np


class Customer:

    def __init__(self, patience: int, channel: str, language: str = None, retrial: bool = False):
        """

        :param patience: the patience of this customer
        :param retrial: whether he would retrial if he abandons
        """
        self.patience = patience
        self.retrial = retrial
        self.channel = channel
        self.language = language


class Process:
    """
    This class generate Customer based on a given probability
    """
    def __init__(self, open_from: int, close_from: int, incoming_prob, patience_prob, language: str, channel: str):
        self.open_from = open_from
        self.close_from = close_from
        self.incoming_prob = incoming_prob
        self.patience = patience_prob
        self.language = language
        self.channel = channel

    def retake_customer(self):
        pass

    def get_customer(self) -> Customer:
        pass


class Worker:

    def __init__(self, work_begin: int, work_end: int, ahts, languages: list, channels: list):
        self.work_begin = work_begin
        self.work_end = work_end
        self.ahts = ahts
        self.languages = languages
        self.channels = channels

    def execute_task(self):
        pass


class Event:

    def __init__(self):
        pass


class System:
    """
    Callcenter represantation of a day
    """
    def __init__(self,  open_time: int, closed_time: int, worker: List[Worker], processes: List[Process]):
        """

        :param open_time: the time in seconds of day when the System begins to work (8 am == 60 * 60 * 8
        :param closed_time: same as open_time but the second the system is closed
        :param worker:
        :param processes:
        """
        self.worker = worker
        self.open_time = open_time
        self.closed_time = closed_time
        self.free_worker_ids = [i for i in range(len(worker))]
        self.busy_worker_ids = []
        self.events = []
        self.processes = processes
        self.processes_time_next_cust = [np.NaN for _ in range(len(self.processes))]
        self.processes_next_customer = [None for _ in range(len(self.processes))]

    def reset(self):
        pass

    def get_free_worker_random(self):
        """
        this returns a random worker

        :return:
        """
        id = np.random.choice(self.free_worker_ids)
        self.busy_worker_ids.append(id)
        self.free_worker_ids.remove(id)
        return self.worker[id]

    def get_free_worker_best(self):
        """
        this returns the best worker for this task based on the average handling time

        :return:
        """
        pass

    def is_worker_available(self):
        """
        tells you if any worker is available

        :return:
        """
        return len(self.free_worker_ids) > 0

    def get_new_task(self):
        pass

    def run(self):

        finished = False
        i = 0.0

        while not finished:
            for processes in self.processes:
                pass




