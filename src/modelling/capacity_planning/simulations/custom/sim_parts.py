import uuid

import numpy as np

from src.modelling.capacity_planning.simulations.probability_classes import Probability


class Customer:

    def __init__(self, patience: float, channel: str, language: str = None, retrial: bool = False):
        """

        :param patience: the patience of this customer
        :param channel
        :param language
        :param retrial: whether he would retrial if he abandons
        :param id:
        """
        self.comes_from_process = None
        self.patience = patience
        self.retrial = retrial
        self.channel = channel
        self.language = language
        self.id = str(uuid.uuid1())
        self.call_time = None


class Process:
    """
    This class generate Customer based on a given probability
    """
    def __init__(self, open_from: int, close_from: int, incoming_prob: Probability, patience_prob: list, language: str,
                 channel: str):
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
        self.id = str(uuid.uuid1())

    def retake_abandoned_customer(self, customer: Customer):
        # TODO create a new customer with possibly other stats
        return customer

    def get_customer(self, day_time: int = 0) -> (float, Customer):
        """

        :param day_time

        :return: a tuple of the time that this customers appears since the last customer
        """
        customer = Customer(patience=np.random.choice(self.patience), channel=self.channel, language=self.language,
                            retrial=False)
        customer.comes_from_process = self.id
        return self.incoming_prob.draw(), customer


class Worker:

    def __init__(self, work_begin: int, work_end: int, ahts, languages: list, channels: list):
        self.work_begin = work_begin
        self.work_end = work_end
        self.ahts = ahts
        self.languages = languages
        self.channels = channels

    def serve_customer(self, customer: Customer):
        return np.random.choice(self.ahts)

