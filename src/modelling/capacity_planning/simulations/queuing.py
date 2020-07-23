from sortedcontainers import SortedList
from sortedcontainers import SortedDict
from typing import List
import numpy as np
from aenum import Enum


class Customer:

    def __init__(self, patience: int, channel: str, language: str = None, retrial: bool = False, id: int = 0):
        """

        :param patience: the patience of this customer
        :param channel
        :param language
        :param retrial: whether he would retrial if he abandons
        :param id:
        """
        self.patience = patience
        self.retrial = retrial
        self.channel = channel
        self.language = language
        self.id = id


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

    def retake_customer(self, customer: Customer):
        pass

    def get_customer(self) -> (float, Customer):
        """

        :return: a tuple of the time that this customers appears since the last customer
        """
        return 1.0, Customer(patience=1, channel=self.channel, language=self.language,
                           retrial=True)


class Worker:

    def __init__(self, work_begin: int, work_end: int, ahts, languages: list, channels: list):
        self.work_begin = work_begin
        self.work_end = work_end
        self.ahts = ahts
        self.languages = languages
        self.channels = channels

    def serve_customer(self, customer: Customer):
        return 0


class Event:

    def __init__(self, event_type, appearance_time, **kwargs):
        self.event_type = event_type
        self.kwargs = kwargs
        self.appearance_time = appearance_time


class EventType(Enum):
    incoming_customer = 0
    abandoned_customer = 1
    worker_finished = 2


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
        self.processes = processes
        self.open_time = open_time
        self.closed_time = closed_time

        self.free_worker_ids = [i for i in range(len(self.worker))]
        self.busy_worker_ids = []

        self.events = SortedList(key=lambda x: x.appearance_time)

        # These two lists held one customer and his appearance time for each process
        self.processes_time_next_customer = [np.NaN for _ in range(len(self.processes))]
        self.processes_next_customer = [None for _ in range(len(self.processes))]
        self.worker_serving_time = [None for _ in range(len(self.worker))]
        self.customer_queue_abandonment = []
        self.customer_queue = []

    def reset_day(self):
        """
        reset all variables for a new. Stats will be saved.

        :return:
        """
        pass

    def get_free_worker_random(self):
        """
        this returns a random worker

        :return:
        """
        if len(self.free_worker_ids) > 0:
            worker_id = int(np.random.choice(self.free_worker_ids))
            self.busy_worker_ids.append(worker_id)
            self.free_worker_ids.remove(worker_id)
            return self.worker[worker_id], worker_id

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

    def create_new_event(self, event_type: EventType, appearance_time: float, func: str, **kwargs: dict):
        pass

    def execute_event(self, event: Event):
        if event.event_type is EventType.incoming_customer:
            self.assign_new_customer(**event.kwargs)
        elif event.event_type is EventType.abandoned_customer:
            self.
        elif event.event_type is EventType.worker_finished:
            pass
        else:
            pass

    def assign_customer_to_worker(self, customer, day_time: float) -> None:
        """
        chooses a random worker and assigns the customer to this worker

        :param customer:
        :param day_time:
        :return:
        """
        worker, worker_id = self.get_free_worker_random()
        time = worker.serve_customer(customer)
        self.worker_serving_time[worker_id] = time + day_time
        event = Event(event_type=EventType.worker_finished, appearance_time=time + day_time)
        self.events.append(event)

    def move_worker_to_free(self, worker_id: int):
        """
        the specified worker has finished his workerd and therefore will be moved to the available agents again

        :return:
        """
        self.worker_serving_time[worker_id] = None
        self.busy_worker_ids.remove(worker_id)
        self.free_worker_ids.append(worker_id)

    def get_next_customer(self) -> (float, Customer):
        next_cust_index = int(np.argmin(self.processes_time_next_customer))
        next_cust_time = self.processes_time_next_customer[next_cust_index]
        next_cust = self.processes_next_customer[next_cust_index]

        self.processes_next_customer[next_cust_index] = None
        self.processes_time_next_customer[next_cust_index] = None

        return next_cust_time, next_cust

    def remove_customer_from_queue(self):
        """
        removes a customer from the waiting queue since the abandoned

        :return:
        """
        pass

    def assign_new_customer(self, day_time: float, next_customer: Customer) -> None:
        """
        this function assigns a new customer to the queue or a worker if this is the next event

        :param day_time:
        :param next_customer:
        :return:
        """
        if self.is_worker_available() and len(self.customer_queue) == 0:
            self.assign_customer_to_worker(next_customer, day_time=day_time)
        else:
            self.customer_queue.append(next_customer)
            self.customer_queue_abandonment.append(next_customer.patience + day_time)
            event = Event(event_type=EventType.abandoned_customer,
                          appearance_time=next_customer.patience + day_time, kwargs={})
            self.events.append(event)
            if self.is_worker_available():
                customer = self.customer_queue.pop()
                _ = self.customer_queue_abandonment.pop()
                self.assign_customer_to_worker(customer, day_time=day_time)

    def run(self):

        finished = False
        day_time = 0.0

        while not finished:
            # update the next customers for each process here. Since each process measures the time in distance to
            # another customers there needs to be only one customer per process rememberd
            for i in range(len(self.processes)):
                if self.processes_next_customer[i] is None:
                    time, cust = self.processes[i].get_customer()
                    self.processes_next_customer[i] = cust
                    self.processes_time_next_customer[i] = time + day_time
                    event = Event(event_type=EventType.incoming_customer, appearance_time=time + day_time, kwargs={"day_time": day_time})
                    self.events.append(event)

                next_event = self.events.pop()
                self.execute_event(next_event)
                day_time = next_event.appearance_time


