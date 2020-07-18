from sortedcontainers import SortedList
from typing import List
import numpy as np


class Worker:

    def __init__(self, ahts):
        self.ahts = ahts

    def execute_task(self):
        pass


class Caller:

    def __init__(self):
        pass


class Task:

    def __init__(self):
        pass


class System:
    """
    Callcenter represantation
    """

    def __init__(self, worker: List[Worker], incoming_caller_prob):
        self.worker = worker
        self.free_worker_ids = [i for i in range(len(worker))]
        self.busy_worker_ids = []
        self.events = []

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


