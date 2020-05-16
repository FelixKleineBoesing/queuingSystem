from src.modelling.capacity_planning import ErlangC, ErlangCP


class CapacityPlanningInboundPhone:

    def get_number_agents_for_service_level(self, interval: int, volumne: float, aht: int, service_level: float,
                                            service_time: float, abandonment: float, size_room: int, patience: int,
                                            retrial: float):
        pass

    def get_volume_for_service_level(self, interval: int, number_agents: int, aht: int, service_level: float,
                                     service_time: float, abandonment: float, size_room: int, patience: int,
                                     retrial: float):
        pass

    def get_number_agents_for_average_waiting_time(self):
        pass

    def get_average_waiting_time_for_number_agents(self):
        pass