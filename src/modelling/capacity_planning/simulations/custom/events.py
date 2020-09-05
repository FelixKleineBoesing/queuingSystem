import uuid

from aenum import Enum


class Event:

    def __init__(self, event_type, appearance_time, events_to_remove: list = None, kwargs: dict = None):
        """

        :param event_type:
        :param appearance_time:
        :param events_to_remove: list of event id that should be removed when this event occurs
        :param kwargs:
        """
        if kwargs is None:
            kwargs = {}
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