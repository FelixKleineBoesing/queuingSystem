import inspect

from src.controller.capacity_planning.single_skill.helpers import Arguments
from src.controller.internal_helpers import IntList, FloatList, check_length_list_equality
from src.misc.helper_functions import annotation_type_checker
from src.modelling.capacity_planning.naive.outbound import OutboundCalculator


class OutboundPhoneController:

    @annotation_type_checker
    @check_length_list_equality
    def get_number_agents(self, interval: IntList, volume: FloatList, dialing_time: IntList, aht_correct: IntList,
                          aht_wrong: IntList, netto_contact_rate: FloatList,
                          right_person_contact_rate: FloatList) -> FloatList:
        """
        calculates the number of agents that are required to hit the specified values

        :param interval: interval in seconds, that you want to observe
        :param volume: the number of contacts in that interval
        :param dialing_time: number of seconds that are used for dialing
        :param aht_correct: the average handling time for correct contact person
        :param aht_wrong: the average handling time for wrong contact person
        :param netto_contact_rate: the netto percentage of contact
        :param right_person_contact_rate: the number of contacts that are the correct person

        :return: number of required agents
        """
        func_args = locals()
        func_inspect = inspect.getfullargspec(self.get_number_agents).args
        func_inspect.remove("self")
        func_args = {key: value for key, value in func_args.items() if key in func_inspect and value is not None}

        def func(interval: int, volume: float, dialing_time: float, aht_correct: int, aht_wrong: int,
                 netto_contact_rate: float, right_person_contact_rate: float):
            kwargs = {"lambda_": volume / interval, "mu_wrong": 1 / aht_wrong,
                      "mu_correct": 1 / aht_correct, "netto_contact_rate": netto_contact_rate,
                      "right_person_contact_rate": right_person_contact_rate, "dialing_time": 1 / dialing_time}

            outbound = OutboundCalculator()
            number_agents = outbound.get_number_agents(**kwargs)

            return number_agents

        if isinstance(interval, int):
            return func(**func_args)
        else:
            number_agents_list = []
            for i in range(len(interval)):
                args = {key: value[i] for key, value in func_args.items()}
                number_agents_list.append(func(**args))
            return number_agents_list

    @annotation_type_checker
    @check_length_list_equality
    def get_volume(self, interval: IntList, number_agents: IntList, dialing_time: IntList, aht_correct: IntList,
                   aht_wrong: IntList, netto_contact_rate: FloatList, right_person_contact_rate: FloatList) -> FloatList:
        """
        calculates the number of agents that are required to hit the specified values

        :param interval: interval in seconds, that you want to observe
        :param number_agents: the number of agents that are deployed
        :param dialing_time: number of seconds that are used for dialing
        :param aht_correct: the average handling time for correct contact person
        :param aht_wrong: the average handling time for wrong contact person
        :param netto_contact_rate: the netto percentage of contact
        :param right_person_contact_rate: the number of contacts that are the correct person

        :return: number of required agents
        """
        func_args = locals()
        func_inspect = inspect.getfullargspec(self.get_volume).args
        func_inspect.remove("self")
        func_args = {key: value for key, value in func_args.items() if key in func_inspect and value is not None}

        def func(interval: int, number_agents: int, dialing_time: float, aht_correct: int, aht_wrong: int,
                 netto_contact_rate: float, right_person_contact_rate: float):
            kwargs = {"mu_wrong": 1 / aht_wrong, "mu_correct": 1 / aht_correct, "netto_contact_rate": netto_contact_rate,
                      "right_person_contact_rate": right_person_contact_rate, "dialing_time": 1 / dialing_time,
                      "number_agents": number_agents}

            outbound = OutboundCalculator()
            volume = outbound.get_volume(**kwargs)

            return volume * interval

        if isinstance(interval, int):
            return func(**func_args)
        else:
            volume_list = []
            for i in range(len(interval)):
                args = {key: value[i] for key, value in func_args.items()}
                volume_list.append(func(**args))
            return volume_list


class OutboundPhoneArguments(Arguments):
    interval: int
    number_agents: int
    volume: float
    dialing_time: float
    aht_correct: float
    aht_wrong: float
    netto_contact_rate: float
    right_person_contact_rate: float
