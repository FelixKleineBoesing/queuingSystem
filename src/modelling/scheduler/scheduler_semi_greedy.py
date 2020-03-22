import logging

import numpy as np
from src.modelling.scheduler.scheduler_base import Scheduler


class SchedulerSemiGreedy(Scheduler):
    """
    This scheduler is semi greedy as it assigns shifts first by starting with the first timestep and assigns a shift
    with as much agents as necessary to fulfill the demand. It then switches to the next timestep and checks
    whether the demand is higher than the actual number of planned agents. If its the case a new shift will be added
    that adds up the difference that is necessary for demand  to fullfill. This will be done until the last timestep
    is reached in which a shift may be added. Afterwards a greedy algorithm will a an agent to that shift that
    minimizes the cost the most.
    """

    def __init__(self, number_agents_per_half_hour: list, lunch_time: int = 1, lunch_time_border: int = 6,
                 number_intervals_per_agent: int = 17, verbose: bool = True):
        """

        :param number_agents_per_half_hour: a list of demands for agents
        :param lunch_time: the length of the lunch
        :param lunch_time_border: describes the distance that a lunch must have from beginning and end of a shift
        :param number_intervals_per_agent: the number of intervals that an agent has to work
        """
        super().__init__(number_intervals_per_agent=number_intervals_per_agent,
                         number_agents_per_half_hour=number_agents_per_half_hour,
                         lunch_time=lunch_time,
                         lunch_time_border=lunch_time_border,
                         verbose=verbose)
        self.shifts = None
        self._build_model()

    def _build_model(self):
        """
        intialised parameters that are necessary for the model

        :return:
        """
        self.shifts = np.zeros((len(self.number_agents_per_half_hour), len(self.number_agents_per_half_hour)))

    def solve(self):
        """
        solves the scheduling problem. The description of the solver is annotated in the class doc

        :return:
        """
        demands = np.array(self.number_agents_per_half_hour)
        shifts = self._assign_agents_until_satisfied(demands=demands, shifts=self.shifts)

        # TODO add lunch time
        # TODO add part times

        self.shifts = shifts

    def _check_lunch_time_constraint(self, shifts: np.ndarray):
        """
        checks if all agents have a lunch_time assigned

        :param shifts:
        :return:
        """
        number_lunch_times = self._check_number_of_lunch_times_to_assign(shifts=shifts)
        return np.all(number_lunch_times == 0)

    def _check_demand_satisfied(self, shifts: np.ndarray, demands: np.ndarray):
        """
        checks if the demand is satisfied by shifts

        :param shifts:
        :param demands:
        :return:
        """
        return np.all(np.sum(shifts, axis=1) >= demands)

    def _check_number_of_lunch_times_to_assign(self, shifts: np.ndarray):
        """
        checks for the shifts matrix in which shift how much lunches have to be assigned

        :param shifts:
        :return:
        """
        max_agents_per_shift = np.max(shifts, axis=0)
        sum_agents_per_shift = np.sum(shifts, axis=0)
        return sum_agents_per_shift - (max_agents_per_shift * self.number_intervals_per_agent -
                                       max_agents_per_shift * self.lunch_time)

    def _get_next_optimal_lunch_time(self, demands: np.ndarray, shifts: np.ndarray):
        """
        assigns the next optimal lunch time to a shift. The number of agent available will be reduced by 1 for
        the given lunch time

        :param demands: demands of agents
        :param shifts: array of shifts and timesteps
        :return:
        """
        #TODO
        pass

    def _get_optimal_next_agent(self, demands: np.ndarray, shifts: np.ndarray):
        """
        assingns an agent to a new or existing shift

        :param demands:
        :param shifts:
        :return:
        """
        shifts = shifts.copy()
        results = []
        shift_sums = np.sum(shifts, axis=0)
        for i in range(shifts.shape[0]):
            if shift_sums[i] > 0:
                service_inefficiency = self._get_service_inefficiency_by_condition(shifts=shifts, demands=demands,
                                                                                   column=i, indices=shifts[:, i] > 0)
                results.append(service_inefficiency)
            else:
                results.append(np.NaN)

        if np.all(~np.isfinite(results)):
            shifts = self._assign_agent_to_existing_shift(demands=demands, shifts=shifts)
        else:
            index = np.nanargmin(results)
            shifts[shifts[:, index] > 0, index] = shifts[shifts[:, index] > 0, index] + 1
        return shifts

    def _assign_agent_to_existing_shift(self, demands: np.ndarray, shifts: np.ndarray):
        results = []
        column = self._get_free_shift(shifts=shifts)
        for i in range(shifts.shape[0]):
            if i <= shifts.shape[0] - self.number_intervals_per_agent:
                indices = list(range(i, i + self.number_intervals_per_agent))
                service_inefficiency = self._get_service_inefficiency_by_condition(shifts=shifts, demands=demands,
                                                                                   column=column, indices=indices)
                results.append(service_inefficiency)
            else:
                results.append(np.NaN)
        index = np.nanargmin(results)
        shifts[index:index + self.number_intervals_per_agent, column] = \
            shifts[index:index + self.number_intervals_per_agent, column] + 1
        return shifts

    def _assign_agents_until_satisfied(self, demands: np.ndarray, shifts: np.ndarray):
        """
        assigns agents to the shifts array until the demands are satisfied

        :return:
        """
        j = 0
        for i in range(len(self.number_agents_per_half_hour)):
            condition_met = all(demands <= np.sum(shifts, axis=1))
            service_ineffiecency = self.get_service_efficiency(demands, shifts)
            self.log("Service Inefficiency is : {}".format(service_ineffiecency), "debug")
            self.log("Condition met: {}".format(condition_met), "debug")
            sum_agents = np.sum(shifts[i, :])
            if sum_agents < self.number_agents_per_half_hour[i] and \
                    i <= shifts.shape[0] - self.number_intervals_per_agent:
                shifts[i:i + self.number_intervals_per_agent, j] = self.number_agents_per_half_hour[i] - sum_agents
                j += 1
            else:
                if np.sum(shifts[i, :]) < self.number_agents_per_half_hour[i]:
                    condition_met = False
                    while not condition_met:
                        shifts = self._get_optimal_next_agent(demands=demands, shifts=shifts)
                        self.get_service_efficiency(demands, shifts)
                        if np.sum(shifts[i, :]) >= self.number_agents_per_half_hour[i]:
                            condition_met = True

        return shifts



    def _get_free_shift(self, shifts: np.ndarray):
        """
        return the index of a column where no shift is assigned. If all shifts are assigned. This will return None

        :param shifts:
        :return:
        """
        for i in range(shifts.shape[1]):
            if np.all(shifts[:, i] == 0):
                return i

    def _get_service_inefficiency_by_condition(self, shifts, demands, column, indices :list):
        """
        divides the service inefficiency by the number of demand that can be covered additionaly

        :return:
        """
        tmp = shifts.copy()
        tmp[indices, column] = tmp[indices, column] + 1
        service_inefficiency = self.get_service_efficiency(demands, tmp)
        condition = np.logical_and.reduce((np.sum(shifts, axis=1) < demands, np.sum(tmp, axis=1) <= demands,
                                           np.sum(shifts, axis=1) < np.sum(tmp, axis=1)))
        sum_condition = np.sum(condition)
        if sum_condition == 0:
            return np.inf
        else:
            return service_inefficiency / sum_condition

    @staticmethod
    def get_service_efficiency(demands: np.ndarray, shifts: np.ndarray):
        sum_shifts = np.sum(shifts)
        if sum_shifts == 0:
            return np.Inf
        else:
            return 1 - (sum(demands) / sum_shifts)


if __name__ == "__main__":
    agents_per_hour = [12, 10, 13, 12, 15, 24, 22, 33, 36, 40, 31, 29, 24, 27, 22, 24, 31, 33, 34, 31, 24, 19, 10,
                       12, 12, 7, 10, 7]
    agents_excel_sheet = [12, 12, 14, 21, 28, 22, 33, 36, 40, 41, 50, 50, 35, 46, 50, 50,
                          34, 38, 33, 26, 22, 21, 17, 17, 14, 10, 7]

    scheduler = SchedulerSemiGreedy(number_agents_per_half_hour=agents_per_hour, lunch_time=1,
                                    number_intervals_per_agent=17)
    shifts = scheduler.solve()
    print(np.sum(shifts, axis=1))
    print(scheduler.get_service_efficiency(demands=agents_per_hour, shifts=agents_excel_sheet))
