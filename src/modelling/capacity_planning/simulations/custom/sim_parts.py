import uuid
import pandas as pd
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
    def __init__(self, open_from: int, close_from: int, incoming_prob: Probability, patience_prob: Probability,
                 language: str, channel: str):
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
        id = self.id
        return customer

    def get_customer(self, day_time: int = 0) -> (float, Customer):
        """

        :param day_time

        :return: a tuple of the time that this customers appears since the last customer
        """
        customer = Customer(patience=self.patience.draw(1), channel=self.channel, language=self.language,
                            retrial=False)
        customer.comes_from_process = self.id
        return self.incoming_prob.draw(), customer


class Worker:

    def __init__(self, work_begin: int, work_end: int, ahts: Probability, languages: list, channels: list):
        self.work_begin = work_begin
        self.work_end = work_end
        self.ahts = ahts
        self.languages = languages
        self.channels = channels

    def serve_customer(self, customer: Customer):
        return self.ahts.draw(1)


class StatisticsContainer:

    def __init__(self, statistics_data: dict):
        self.data = pd.DataFrame(statistics_data["events"])
        self.number_customer = statistics_data.get("number_customers", 0)
        self.number_events = statistics_data.get("number_events", 0)
        self.number_days = statistics_data.get("number_days", 0)
        self.number_seconds = statistics_data.get("number_seconds", 0)

        self.number_abandoned_customer = None
        self.number_incoming_customer = None
        self.number_served_customers = None
        self.queue_length = None
        self.waiting_time = None
        self.incoming_customer = None
        self.abandoned_customer = None
        self.update()

    def update(self):
        self.number_abandoned_customer = np.sum(self.data["variable"] == "abandoned_customer")
        self.number_incoming_customer = np.sum(self.data["variable"] == "incoming_customer")
        self.number_served_customers = self.data.loc[self.data["variable"] == "served_customer", :]
        self.queue_length = self.data.loc[self.data["variable"] == "queue_length", :]
        self.waiting_time = self.data.loc[self.data["variable"] == "waiting_time", :]
        self.incoming_customer = self.data.loc[self.data["variable"] == "incoming_customer", :]
        self.abandoned_customer = self.data.loc[self.data["variable"] == "abandoned_customer", :]

    def get_waiting_time_dist(self):
        """
        extracts the distribution of waiting times

        :return:
        """
        return self.waiting_time["value"].tolist()

    def get_waiting_time_mean(self):
        """
        extracts the mean waiting time

        :return:
        """
        return np.mean(self.waiting_time["value"])

    def get_queue_length_dist(self):
        """
        extracts the distribution of queue length

        :return:
        """
        return self.queue_length["value"].tolist()

    def get_queue_length_mean(self):
        """
        extracts the average queue length
        :return:
        """
        return np.mean(self.queue_length["value"])

    def get_abort_level(self):
        """
        extracts the share of abortion

        :return:
        """
        return self.number_abandoned_customer / self.number_incoming_customer

    def get_service_level(self, service_time: float):
        """
        calculates the service level based on the supplied service time

        :param service_time:
        :return:
        """
        served_customer_not_in_time = np.sum(self.number_served_customers["value"] > service_time)
        if served_customer_not_in_time == 0:
            rel_not_served = 0
        else:
            rel_not_served = served_customer_not_in_time / self.number_served_customers.shape[0]
        return 1 - self.get_abort_level() - rel_not_served
