from typing import List

import numpy as np
from sortedcontainers import SortedList

from src.modelling.capacity_planning.simulations.custom.events import Event, EventType
from src.modelling.capacity_planning.simulations.custom.sim_parts import Customer, Process, Worker


class CallCenterSimulation:
    """
    Callcenter representation of a day
    """
    def __init__(self,  open_time: int, closed_time: int, worker: List[Worker], processes: List[Process],
                 size_waiting_room: int = None, stopping_criterita: dict = None):
        """

        :param open_time: the time in seconds of day when the System begins to work (8 am == 60 * 60 * 8
        :param closed_time: same as open_time but the second the system is closed
        :param worker:
        :param processes:
        :param stopping_criterita: This parameter controls the length of the Simulation.
            If None it will stop after 10.000 events. The possible keys are:
            - max_events
            - max_days
            - max_customer
            - max_seconds

            This can be combined with a bottom limit which must be reached for to exit the simulation
            - min_day
            - min_events
            - min_customer
            - min_seconds

            For example should a simulation finish after 10000 events, but be at least one day. The lower limit has
            to be achieved for a simulation exit.


            This dictionary can contain several stopping criterias but the simulation stopps of one of these criteria
            is hit
        """
        self.worker = worker
        self.processes = processes
        self.processes_mapping = {process.id: value for value, process in enumerate(self.processes)}
        self.open_time = open_time
        self.closed_time = closed_time
        self.size_waiting_room = size_waiting_room

        self.free_worker_ids = [i for i in range(len(self.worker))]
        self.busy_worker_ids = []

        # These two lists held one customer and his appearance time for each process
        self.processes_has_next_customer = None
        self.worker_serving_time = None

        self.customer_queue = None
        self.customers = None
        self.customer_id = None

        self.events = None
        self.events_queue = None
        self.customer_event_table = None

        self.day_time = 0
        self.days_simulated = 0

        if stopping_criterita is None:
            stopping_criterita = {"max_events": 10000}
        self.stopping_criteria = stopping_criterita
        self.reset_day()

        self.statistics = {"number_customers":  0,
                           "number_events": 0,
                           "number_days": 0,
                           "number_seconds": 0,
                           "events": {
                               "time": [],
                               "variable": [],
                               "value": []
                           }}

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

        self.customer_queue = []
        self.customers = {}
        self.customer_id = 0

        self.events = {}
        self.events_queue = SortedList(key=lambda x: x[1])

        self.customer_event_table = {}

        self.day_time = 0

    def run(self):

        finished = False
        self.day_time = 0.0
        j = 0
        while not finished:
            # update the next customers for each process here. Since each process measures the time in distance to
            # another customers there needs to be only one customer per process rememberd
            for i in range(len(self.processes)):
                if self.processes_has_next_customer[i] is False:
                    time, cust = self.processes[i].get_customer()
                    event = self.append_new_event(event_type=EventType.incoming_customer,
                                                  appearance_time=time + self.day_time,
                                                  kwargs={"customer": cust})
                    self.track_customer_related_events(customer_id=cust.id, event=event)
                    self.processes_has_next_customer[i] = True

            next_event = self.get_next_event()
            if j % 1000 == 0.0:
                print("Number iterations: {}".format(j))
            if next_event.appearance_time >= 24 * 60 * 60:
                self.reset_day()
                self.days_simulated += 1
                self.statistics["number_days"] = self.days_simulated
                print("Reset Day")
            else:
                self.execute_event(next_event)
                self.day_time = next_event.appearance_time
            self.statistics["number_seconds"] = self.days_simulated * 24 * 60 * 60 + self.day_time
            j += 1
            finished = self.check_if_finished()

    def append_event(self, time: float, variable: str, value):
        """
        tracks a statistic

        :param time: appearance time
        :param variable: Can be one of:
            - waiting_time
            - incoming_customer
            - abandoned_customer
            - queue_length
            - served_customer
        :param value:
        :return:
        """
        self.statistics["events"]["time"].append(time)
        self.statistics["events"]["variable"].append(variable)
        self.statistics["events"]["value"].append(value)

    def check_if_finished(self):
        finished = False
        if "max_events" in self.stopping_criteria:
            if self.statistics["number_events"] >= self.stopping_criteria["max_events"]:
                finished = finished or True
        if "max_days" in self.stopping_criteria:
            if self.statistics["number_events"] >= self.stopping_criteria["max_days"]:
                finished = finished or True
        if "max_customer" in self.stopping_criteria:
            if self.statistics["number_events"] >= self.stopping_criteria["max_customer"]:
                finished = finished or True
        if "max_seconds" in self.stopping_criteria:
            if self.statistics["number_events"] >= self.stopping_criteria["max_seconds"]:
                finished = finished or True
        if "min_events" in self.stopping_criteria:
            if self.statistics["number_events"] >= self.stopping_criteria["min_events"]:
                finished = finished and True
        if "min_days" in self.stopping_criteria:
            if self.statistics["number_days"] >= self.stopping_criteria["min_days"]:
                finished = finished and True
        if "min_customer" in self.stopping_criteria:
            if self.statistics["number_customers"] >= self.stopping_criteria["min_customer"]:
                finished = finished and True
        if "min_seconds" in self.stopping_criteria:
            if self.statistics["number_seconds"] >= self.stopping_criteria["min_seconds"]:
                finished = finished and True

        return finished

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

    def abandon_customer(self, event_time: float, customer_id: str):
        customer = self.customers[customer_id]
        self.append_event(time=event_time, variable="abandoned_customer", value=0)
        self.append_event(time=event_time, variable="waiting_time", value=customer.patience)
        if customer.retrial:
            process_id = self.processes_mapping[customer.comes_from_process]
            new_customer = self.processes[process_id].retake_abandoned_customer(customer)
            self.assign_new_customer(event_time=event_time, customer=new_customer)

        del self.customers[customer_id]
        del self.customer_event_table[customer_id]

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
            if customer is None:
                return
            self.append_event(time=event_time, variable="waiting_time", value=event_time - customer.call_time)
            self.assign_customer_to_worker(customer=customer, day_time=event_time)
            if customer.id in self.customer_event_table:
                customer_events = self.customer_event_table[customer.id]
                abandond_event = customer_events.get(EventType.abandoned_customer)
                if abandond_event is not None:
                    del self.customer_event_table[customer.id]
                    del self.events[abandond_event]

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
        self.append_new_event(event_type=EventType.worker_finished, appearance_time=time + day_time,
                              kwargs={"worker_id": worker_id})

    def remove_customer_from_queue(self, customer_id):
        """
        removes a customer from the waiting queue since he abandoned

        :return:
        """
        del self.customers[customer_id]

    def get_next_customer_from_queue(self):
        if len(self.customer_queue) > 0:
            customer_id = self.customer_queue.pop()
            if customer_id in self.customers:
                return self.customers[customer_id]
            else:
                return self.get_next_customer_from_queue()

    def assign_new_customer(self, event_time: float, customer: Customer) -> None:
        """
        this function assigns a new customer to the queue or a worker if this is the next event

        :param event_time:
        :param customer:
        :return:
        """
        self.append_event(time=event_time, variable="incoming_customer", value=0)
        customer.id = self.get_next_customer_id()
        if self.is_worker_available() and len(self.customer_queue) == 0:
            self.append_event(time=event_time, variable="waiting_time", value=0)
            self.append_event(time=event_time, variable="queue_length", value=0)
            self.assign_customer_to_worker(customer, day_time=event_time)
        else:
            customer.call_time = event_time
            self.customers[customer.id] = customer
            self.customer_queue.append(customer.id)
            event = self.append_new_event(event_type=EventType.abandoned_customer,
                                          appearance_time=customer.patience + event_time,
                                          kwargs={"customer_id": customer.id})
            self.track_customer_related_events(customer_id=customer.id, event=event)
            self.append_event(time=event_time, variable="queue_length", value=len(self.customer_queue))
            if self.is_worker_available():
                customer_id = self.customer_queue.pop()
                customer = self.customers[customer_id]
                del self.customers[customer_id]
                self.assign_customer_to_worker(customer, day_time=event_time)
        process_id = self.processes_mapping[customer.comes_from_process]
        self.processes_has_next_customer[process_id] = False

    def get_next_customer_id(self):
        self.customer_id += 1
        return self.customer_id

    def get_next_event(self):
        """

        :return:
        """
        event_id, appearance_time = self.events_queue.pop(index=0)
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
        self.events_queue.add((event.id, event.appearance_time))
        self.events[event.id] = event
        return event

    def remove_event(self, event_id: str):
        del self.events[event_id]

    def track_customer_related_events(self, customer_id: str, event: Event):
        self.customer_event_table[customer_id] = {event.event_type: event.id}

    def execute_event(self, event: Event):
        self.statistics["number_events"] += 1
        if event.event_type is EventType.incoming_customer:
            self.assign_new_customer(event_time=event.appearance_time, **event.kwargs)
            self.statistics["number_customers"] += 1
        elif event.event_type is EventType.abandoned_customer:
            self.abandon_customer(event_time=event.appearance_time, **event.kwargs)
        elif event.event_type is EventType.worker_finished:
            self.move_worker_to_free(event_time=event.appearance_time, **event.kwargs)
        else:
            raise NotImplementedError("No other event type are yet implemented")
        del self.events[event.id]