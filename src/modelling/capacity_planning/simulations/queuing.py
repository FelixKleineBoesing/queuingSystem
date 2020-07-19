from sortedcontainers import SortedList
from typing import List
import numpy as np


class Process:
    pass


class Worker:

    def __init__(self, work_begin: int, work_end: int, ahts):
        self.work_begin = work_begin
        self.work_end = work_end
        self.ahts = ahts

    def execute_task(self):
        pass


class Customer:

    def __init__(self):
        pass


class Task:

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
        self.free_worker_ids = [i for i in range(len(worker))]
        self.busy_worker_ids = []
        self.events = []
        self.processes = processes

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

        while not finished:
            task = self.get_new_task()


