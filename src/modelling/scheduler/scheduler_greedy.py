import datetime

import numpy as np

from src.modelling.scheduler.scheduler_base import Scheduler


class SchedulerGreedy(Scheduler):

    def __init__(self, demands: list, lunch_time: int = 1,
                 number_intervals_per_agent: int = 17, lunch_time_border: int = 6, verbose: bool = True,
                 search_depth: int = 1):
        super().__init__(demands=demands, lunch_time=lunch_time, number_intervals_per_agent=number_intervals_per_agent,
                         lunch_time_border=lunch_time_border, verbose=verbose)
        self.shifts = np.zeros((len(self.demands), len(self.demands)))
        self.search_depth: int = search_depth

    def solve(self):
        """
        solves the scheduling problem. The description of the solver is annotated in the class doc

        :return:
        """
        demands = np.array(self.demands)
        satisfied = False
        shifts = self.shifts
        n = 1
        while not satisfied:
            print("{}th run!".format(n))
            print("Start agents")
            shifts = self._assign_agents_until_satisfied(shifts=shifts, demands=demands)
            print("Start lunch times")
            shifts = self._assign_lunch_times_until_satisfied(demands=demands, shifts=shifts)
            if self._check_demand_satisfied(shifts=shifts, demands=demands):
                satisfied = True
            n+=1
        self.shifts = shifts
        return shifts

    def _get_next_optimal_lunch_time(self, demands: np.ndarray, shifts: np.ndarray, current_search_depth: int = 1):
        """
        assigns the next optimal lunch time to a shift. The number of agent available will be reduced by 1 for
        the given lunch time

        :param demands: demand of agents
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
                    if current_search_depth == self.search_depth or self._check_lunch_time_constraint(shifts=tmp):
                        service_ineffiency = self._get_cost_differential_for_lunch_time_assignment(old_shifts=shifts,
                                                                                                   new_shifts=tmp,
                                                                                                   demands=demands)
                    else:
                        optimal_shifts = self._get_next_optimal_lunch_time(demands=demands, shifts=tmp,
                                                                           current_search_depth=current_search_depth+1)
                        service_ineffiency = \
                            self._get_cost_differential_for_lunch_time_assignment(demands=demands,
                                                                                  new_shifts=optimal_shifts,
                                                                                  old_shifts=shifts)
                    results.append(service_ineffiency)
                    chosen_shifts.append(j)
                    chosen_indices.append(i)
                    break

        index = int(np.nanargmin(results))
        shifts[chosen_indices[index]:(chosen_indices[index]+self.lunch_time), chosen_shifts[index]] -= 1
        return shifts

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

    def _get_optimal_next_agent(self, demands: np.ndarray, shifts: np.ndarray, current_search_depth: int = 1):
        """
        assingns an agent to a new or existing shift

        :param demands:
        :param shifts:
        :return:
        """
        shifts = shifts.copy()
        results = []
        chosen_indices = []
        chosen_columns = []
        bounds_shifts = self._get_bounds(shifts=shifts)
        lower_bounds = {b[0]: key for key, b in bounds_shifts.items()}
        column = self._get_free_shift(shifts=shifts)
        for i in range(shifts.shape[0]):
            if i in lower_bounds:
                j = lower_bounds[i]
                tmp = shifts.copy()
                bounds = bounds_shifts[j]
                tmp[bounds[0]:(bounds[1] + 1), j] += 1
                if current_search_depth == self.search_depth or self._check_demand_satisfied(shifts=tmp,
                                                                                             demands=demands):
                    service_inefficiency = self._get_cost_differential_for_agent_assignment(new_shifts=tmp,
                                                                                            old_shifts=shifts,
                                                                                            demands=demands)
                else:
                    optimal_shifts = self._get_optimal_next_agent(demands=demands, shifts=tmp,
                                                                  current_search_depth=current_search_depth+1)
                    service_inefficiency = self._get_cost_differential_for_agent_assignment(
                        demands=demands, new_shifts=optimal_shifts, old_shifts=shifts)
                results.append(service_inefficiency)
                chosen_indices.append(list(range(bounds[0], (bounds[1] + 1))))
                chosen_columns.append(j)
            else:
                if i <= shifts.shape[0] - self.number_intervals_per_agent:
                    indices = list(range(i, i + self.number_intervals_per_agent))
                    tmp = shifts.copy()
                    tmp[indices, column] = tmp[indices, column] + 1
                    if current_search_depth == self.search_depth or self._check_demand_satisfied(shifts=tmp,
                                                                                                 demands=demands):
                        service_inefficiency = self._get_cost_differential_for_agent_assignment(new_shifts=tmp,
                                                                                                old_shifts=shifts,
                                                                                                demands=demands)
                    else:
                        optimal_shifts = self._get_optimal_next_agent(demands=demands, shifts=tmp,
                                                                      current_search_depth=current_search_depth+1)
                        service_inefficiency = self._get_cost_differential_for_agent_assignment(
                            demands=demands, new_shifts=optimal_shifts, old_shifts=shifts)
                    results.append(service_inefficiency)
                    chosen_indices.append(indices)
                    chosen_columns.append(column)

        index = int(np.nanargmin(results))

        chosen_index = chosen_indices[index]
        chosen_column = chosen_columns[index]

        shifts[chosen_index, chosen_column] += 1

        return shifts

    def _assign_agents_until_satisfied(self, demands: np.ndarray, shifts: np.ndarray):
        """
        assigns lunch time greedily until lunch time is satisfied

        :return:
        """
        satisfied = False
        while not satisfied:
            shifts = self._get_optimal_next_agent(demands=demands, shifts=shifts)
            if self._check_demand_satisfied(shifts=shifts, demands=demands):
                satisfied = True

        return shifts


if __name__ == "__main__":
    agents_per_hour = [12, 10, 13, 12, 15, 24, 22, 33, 36, 40, 31, 29, 24, 27, 22, 24, 31, 33, 34, 31, 24, 19, 10,
                       12, 12, 7, 10, 7]
    agents_excel_sheet = [12, 12, 14, 21, 21, 28, 22, 33, 36, 40, 41, 50, 50, 35, 46, 50, 50, 34, 38, 33, 26, 22, 21,
                          17, 17, 14, 10, 7]
    start = datetime.datetime.now()
    scheduler = SchedulerGreedy(demands=agents_per_hour, lunch_time=2,
                                number_intervals_per_agent=17, lunch_time_border=6,
                                search_depth=1)
    resulting_shifts = scheduler.solve()
    print("Took {} time!".format(datetime.datetime.now() - start))
    print(np.sum(resulting_shifts, axis=1))
    print(scheduler.get_service_efficiency(demands=np.array(agents_per_hour), shifts=np.array(agents_excel_sheet)))
    print(scheduler.get_service_efficiency(demands=np.array(agents_per_hour), shifts=resulting_shifts))
    fig = scheduler.plot()
    fig.show()
