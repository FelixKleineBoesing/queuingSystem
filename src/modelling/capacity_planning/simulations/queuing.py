import uuid

from sortedcontainers import SortedList
from typing import List
import numpy as np
from aenum import Enum


class Customer:

    def __init__(self, patience: float, channel: str, language: str = None, retrial: bool = False):
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
        self.id = str(uuid.uuid1())


class Process:
    """
    This class generate Customer based on a given probability
    """
    def __init__(self, open_from: int, close_from: int, incoming_prob, patience_prob, language: str, channel: str):
        """

        :param open_from:
        :param close_from:
        :param incoming_prob: prob density function for incoming interval
        :param patience_prob:  prob density function for patience interval
        :param language: language of this process
        :param channel: channel of this process
        """
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

    def __init__(self, event_type, appearance_time, events_to_remove: list = None, **kwargs):
        """

        :param event_type:
        :param appearance_time:
        :param events_to_remove: list of event id that should be removed when this event occurs
        :param kwargs:
        """
        if events_to_remove is None:
            events_to_remove = []
        self.event_type = event_type
        self.kwargs = kwargs
        self.appearance_time = appearance_time
        self.events_to_remove = events_to_remove
        self.id = str(uuid.uuid1())

    def append_events_to_remove(self, event_id: int):
        self.events_to_remove.append(event_id)


class EventType(Enum):
    incoming_customer = 0
    abandoned_customer = 1
    worker_finished = 2


class System:
    """
    Callcenter represantation of a day
    """
    def __init__(self,  open_time: int, closed_time: int, worker: List[Worker], processes: List[Process],
                 size_waiting_room: int = None):
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
        self.size_waiting_room = size_waiting_room

        self.free_worker_ids = [i for i in range(len(self.worker))]
        self.busy_worker_ids = []

        # These two lists held one customer and his appearance time for each process
        self.processes_has_next_customer = None
        self.worker_serving_time = None

        self.customer_queue_abandonment = None
        self.customer_queue = None
        self.customers = None
        self.customer_id = None

        self.events = None
        self.events_queue = None
        self.reset_day()
        self.customer_event_table = None

    def reset_day(self):
        """
        reset all variables for a new. Stats will be saved.

        :return:
        """
        self.free_worker_ids = [i for i in range(len(self.worker))]
        self.busy_worker_ids = []

        # These two lists held one customer and his appearance time for each process
        self.processes_has_next_customer = [False for _ in range(len(self.processes))]
        self.worker_serving_time = [None for _ in range(len(self.worker))]

        self.customer_queue_abandonment = []
        self.customer_queue = []
        self.customers = {}
        self.customer_id = 0

        self.events = {}
        self.events_queue = SortedList(key=lambda x: x[1])

        self.customer_event_table = {}

    def track_customer_related_events(self, customer_id: str, event_id: str, event_type: EventType):
        self.customer_event_table[customer_id] = {event_type: event_id}

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
        raise NotImplementedError()

    def is_worker_available(self):
        """
        tells you if any worker is available

        :return:
        """
        return len(self.free_worker_ids) > 0

    def execute_event(self, event: Event):
        if event.event_type is EventType.incoming_customer:
            self.assign_new_customer(event_time=event.appearance_time, **event.kwargs)
        elif event.event_type is EventType.abandoned_customer:
            pass
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
        self.append_new_event(event_type=EventType.worker_finished, appearance_time=time + day_time, kwargs={})

    def get_next_customer_from_queue(self):
        if len(self.customer_queue) > 0:
            customer_id = self.customer_queue.pop()[0]
            if customer_id in self.customers:
                return self.customers[customer_id]
            else:
                return self.get_next_customer_from_queue()

    def move_worker_to_free(self, event_time: float, worker_id: int):
        """
        the specified worker has finished his workerd and therefore will be moved to the available agents again

        :return:
        """
        self.worker_serving_time[worker_id] = None
        self.busy_worker_ids.remove(worker_id)
        self.free_worker_ids.append(worker_id)
        if len(self.customer_queue) > 0:
            customer = self.get_next_customer_from_queue()
            self.assign_customer_to_worker(customer=customer, day_time=event_time)
            if customer.id in self.customer_event_table:
                customer_events = self.customer_event_table[customer.id]
                abandond_event = customer_events.get(EventType.abandoned_customer)
                if abandond_event is not None:
                    del self.customer_event_table[customer.id]
                    del self.events[abandond_event.id]

    def remove_customer_from_queue(self, customer_id):
        """
        removes a customer from the waiting queue since he abandoned

        :return:
        """
        del self.customers[customer_id]

    def assign_new_customer(self, event_time: float, customer: Customer) -> None:
        """
        this function assigns a new customer to the queue or a worker if this is the next event

        :param event_time:
        :param customer:
        :return:
        """
        customer.id = self.get_next_customer_id()
        if self.is_worker_available() and len(self.customer_queue) == 0:
            self.assign_customer_to_worker(customer, day_time=event_time)
        else:
            self.customers[customer.id] = customer
            self.customer_queue.append(customer.id)
            self.customer_queue_abandonment.append(customer.patience + event_time)
            self.append_new_event(event_type=EventType.abandoned_customer,
                                  appearance_time=customer.patience + event_time,
                                  kwargs={})
            if self.is_worker_available():
                customer_id = self.customer_queue.pop()
                _ = self.customer_queue_abandonment.pop()
                customer = self.customers[customer_id]
                del self.customers[customer_id]
                self.assign_customer_to_worker(customer, day_time=event_time)

    def run(self):

        finished = False
        day_time = 0.0

        while not finished:
            # update the next customers for each process here. Since each process measures the time in distance to
            # another customers there needs to be only one customer per process rememberd
            for i in range(len(self.processes)):
                if self.processes_has_next_customer[i] is False:
                    time, cust = self.processes[i].get_customer()
                    self.append_new_event(event_type=EventType.incoming_customer,
                                          appearance_time=time + day_time,
                                          kwargs={"customer": cust})

            next_event = self.get_next_event()
            self.execute_event(next_event)
            day_time = next_event.appearance_time

    def get_next_customer_id(self):
        self.customer_id += 1
        return self.customer_id

    def get_next_event(self):
        """

        :return:
        """
        event_id, appearance_time = self.events_queue.pop()
        if event_id in self.events:
            return self.events[event_id]
        else:
            return self.get_next_event()

    def append_new_event(self, event_type: EventType, appearance_time: float, kwargs: dict,
                         events_to_remove: list = None):
        """

        :param event_type:
        :param appearance_time: The time in seconds of day when the event will appear
        :param kwargs: the arguments to the corresponding event
        :param events_to_remove:
        :return:
        """
        if events_to_remove is None:
            events_to_remove = []
        event = Event(event_type=event_type, appearance_time=appearance_time, kwargs=kwargs,
                      events_to_remove=events_to_remove)
        self.events_queue.append((event.id, event.appearance_time))
        self.events[event.id] = event

    def remove_event(self, event_id: str):
        del self.events[event_id]
