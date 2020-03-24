import logging

import numpy as np
from typing import Dict, Tuple
import datetime
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

    def __init__(self, demands: list, lunch_time: int = 1, lunch_time_border: int = 6,
                 number_intervals_per_agent: int = 17, verbose: bool = True):
        """

        :param demands: a list of demands for agents
        :param lunch_time: the length of the lunch
        :param lunch_time_border: describes the distance that a lunch must have from beginning and end of a shift
        :param number_intervals_per_agent: the number of intervals that an agent has to work
        """
        super().__init__(number_intervals_per_agent=number_intervals_per_agent,
                         demands=demands,
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
        satisfied = False
        shifts = self.shifts
        while not satisfied:
            shifts = self._assign_agents_until_satisfied(demands=demands, shifts=shifts)
            shifts = self._assign_lunch_times_until_satisfied(demands=demands, shifts=shifts)
            if self._check_demand_satisfied(shifts=shifts, demands=demands):
                satisfied = True
            print(demands)
            print(np.sum(shifts, axis=1))
        # TODO add lunch time
        # TODO add part times

        self.shifts = shifts
        return shifts

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

    def _assign_lunch_times_until_satisfied(self, demands: np.ndarray, shifts: np.ndarray):
        """
        assigns lunch time greedily until lunch time is satisfied

        :return:
        """
        satisfied = False
        while not satisfied:
            shifts = self._get_next_optimal_lunch_time(demands=demands, shifts=shifts)
            if self._check_lunch_time_constraint(shifts=shifts):
                satisfied = True

        return shifts

    def _get_next_optimal_lunch_time(self, demands: np.ndarray, shifts: np.ndarray):
        """
        assigns the next optimal lunch time to a shift. The number of agent available will be reduced by 1 for
        the given lunch time

        :param demands: demands of agents
        :param shifts: array of shifts and timesteps
        :return:
        """
        results = []
        chosen_shifts = []
        chosen_indices = []

        bounds = self._get_lunch_time_bounds(shifts=shifts)
        shift_indices = list(bounds.keys())
        min_bound = np.min(list(bounds.values()))
        max_bound = np.max(list(bounds.values()))
        necessary_lunch_times = self._check_number_of_lunch_times_to_assign(shifts=shifts)
        shift_indices = [i for i in shift_indices if necessary_lunch_times[i] > 0]
        for i in range(min_bound, max_bound + 1):
            for j in shift_indices:
                if bounds[j][1] >= i >= bounds[j][0] and np.all(shifts[i:(i+self.lunch_time), j] > 0):
                    tmp = shifts.copy()
                    tmp[i:(i+self.lunch_time), j] = tmp[i:(i+self.lunch_time), j] - 1
                    service_ineffiency = self._get_cost_differential_for_lunch_time_assignment(old_shifts=shifts,
                                                                                               new_shifts=tmp,
                                                                                               demands=demands)
                    results.append(service_ineffiency)
                    chosen_shifts.append(j)
                    chosen_indices.append(i)
                    break

        index = int(np.nanargmin(results))
        shifts[chosen_indices[index]:(chosen_indices[index]+self.lunch_time), chosen_shifts[index]] -= 1
        return shifts

    def _get_lunch_time_bounds(self, shifts: np.ndarray):
        """
        returns the lunch time bounds (upper and lower) in which the lunch_time may be placed

        :param shifts:
        :return:
        """
        bounds = self._get_bounds(shifts=shifts)
        lunch_time_bounds = {}
        for col in bounds:
            lunch_time_bounds[col] = (bounds[col][0] + self.lunch_time_border,
                                      bounds[col][1] - self.lunch_time_border - self.lunch_time + 1)

        return lunch_time_bounds

    def _get_bounds(self, shifts) -> Dict[int, Tuple]:
        """
        returns the bounds of each shifts in a tuple: (lower, upper)

        :param shifts:
        :return:
        """
        indices = self._get_assigned_shifts(shifts=shifts)
        bounds = {}
        for i in indices:
            lower = None
            upper = None
            for j in range(shifts.shape[0]):
                if lower is None:
                    if shifts[j, i] > 0 and j == 0:
                        lower = j
                    elif shifts[j, i] == 0 and shifts[j + 1, i] > 0:
                        lower = j + 1
                if upper is None:
                    if shifts[j, i] > 0 and j == (shifts.shape[0] - 1):
                        upper = j
                    elif shifts[j, i] > 0 and shifts[j + 1, i] == 0:
                        upper = j
                if upper is not None and lower is not None:
                    break
            bounds[i] = (lower, upper)
        return bounds

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
                tmp = shifts.copy()
                tmp[shifts[:, i] > 0, i] = tmp[shifts[:, i] > 0, i] + 1
                service_inefficiency = self._get_cost_differential_for_agent_assignment(new_shifts=tmp, old_shifts=shifts,
                                                                                        demands=demands)
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
        """
        assigns one agent to an existing shift based on which shift adds least inefficiency

        :param demands:
        :param shifts:
        :return:
        """
        results = []
        column = self._get_free_shift(shifts=shifts)
        for i in range(shifts.shape[0]):
            if i <= shifts.shape[0] - self.number_intervals_per_agent:
                indices = list(range(i, i + self.number_intervals_per_agent))
                tmp = shifts.copy()
                tmp[indices, column] = tmp[indices, column] + 1
                service_inefficiency = self._get_cost_differential_for_agent_assignment(new_shifts=tmp, old_shifts=shifts,
                                                                                        demands=demands)
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
        for i in range(len(self.number_agents_per_half_hour)):
            j = self._get_free_shift(shifts=shifts)
            condition_met = all(demands <= np.sum(shifts, axis=1))
            service_ineffiecency = self.get_service_efficiency(demands, shifts)
            self.log("Service Inefficiency is : {}".format(service_ineffiecency), "debug")
            self.log("Condition met: {}".format(condition_met), "debug")
            sum_agents = np.sum(shifts[i, :])
            if sum_agents < self.number_agents_per_half_hour[i] and \
                    i <= shifts.shape[0] - self.number_intervals_per_agent:
                shifts[i:i + self.number_intervals_per_agent, j] = self.number_agents_per_half_hour[i] - sum_agents
            else:
                if np.sum(shifts[i, :]) < self.number_agents_per_half_hour[i]:
                    condition_met = False
                    while not condition_met:
                        shifts = self._get_optimal_next_agent(demands=demands, shifts=shifts)
                        self.get_service_efficiency(demands, shifts)
                        if np.sum(shifts[i, :]) >= self.number_agents_per_half_hour[i]:
                            condition_met = True

        return shifts

    def _get_assigned_shifts(self, shifts: np.ndarray):
        """
        get the indices of the shifts that are already assigned in the shifts array

        :param shifts:
        :return:
        """
        shifts_indices = np.where(np.sum(shifts, axis=0) > 0)
        return shifts_indices[0]

    def _get_free_shift(self, shifts: np.ndarray):
        """
        return the index of a column where no shift is assigned. If all shifts are assigned. This will return None

        :param shifts:
        :return:
        """
        for i in range(shifts.shape[1]):
            if np.all(shifts[:, i] == 0):
                return i

    def _get_cost_differential_for_lunch_time_assignment(self, old_shifts: np.ndarray, new_shifts: np.ndarray,
                                                         demands: np.ndarray):
        """
        divides the service inefficiency by the number of demand that can be covered additionaly. This is the
        cost function that should be optimized. The lesser the added service inefficiency the better.

        :return:
        """
        differences = demands - np.sum(new_shifts, axis=1)
        differences[(np.sum(old_shifts, axis=1) - np.sum(new_shifts, axis=1)) == 0] = 0
        return np.sum(differences)

    def _get_cost_differential_for_agent_assignment(self, old_shifts: np.ndarray, new_shifts: np.ndarray,
                                                    demands: np.ndarray):
        """
        divides the service inefficiency by the number of demand that can be covered additionaly. This is the
        cost function that should be optimized. The lesser the added service inefficiency the better.

        :return:
        """
        service_inefficiency = self.get_service_efficiency(demands, new_shifts)
        condition = np.logical_and.reduce((np.sum(old_shifts, axis=1) < demands, np.sum(new_shifts, axis=1) <= demands,
                                           np.sum(old_shifts, axis=1) < np.sum(new_shifts, axis=1)))
        sum_condition = np.sum(condition)
        if sum_condition == 0:
            return np.inf
        else:
            return service_inefficiency / sum_condition


    @staticmethod
    def get_service_efficiency(demands: np.ndarray, shifts: np.ndarray):
        """
        calculates the service inefficency for a given demand and shift array

        :param demands:
        :param shifts:
        :return:
        """
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
    start = datetime.datetime.now()
    scheduler = SchedulerSemiGreedy(demands=agents_per_hour, lunch_time=2,
                                    number_intervals_per_agent=17, lunch_time_border=6)
    resulting_shifts = scheduler.solve()
    print("Took {} time!".format(datetime.datetime.now() - start))
    print(np.sum(resulting_shifts, axis=1))
    print(scheduler.get_service_efficiency(demands=np.array(agents_per_hour), shifts=np.array(agents_excel_sheet)))
    print(scheduler.get_service_efficiency(demands=np.array(agents_per_hour), shifts=resulting_shifts))
