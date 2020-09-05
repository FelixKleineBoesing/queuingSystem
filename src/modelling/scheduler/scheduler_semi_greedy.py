import numpy as np
import datetime
from src.modelling.scheduler.scheduler_greedy import SchedulerGreedy


class SchedulerSemiGreedy(SchedulerGreedy):
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
        self.shifts = np.zeros((len(self.demands), len(self.demands)))

    def solve(self):
        """
        solves the scheduling problem. The description of the solver is annotated in the class doc

        :return:
        """
        demands = np.array(self.demands)
        satisfied = False
        shifts = self.shifts
        while not satisfied:
            shifts = self._assign_agents_until_satisfied(demands=demands, shifts=shifts)
            shifts = self._assign_lunch_times_until_satisfied(demands=demands, shifts=shifts)
            if self._check_demand_satisfied(shifts=shifts, demands=demands):
                satisfied = True
        self.shifts = shifts
        return shifts

    def _assign_agents_until_satisfied(self, demands: np.ndarray, shifts: np.ndarray):
        """
        assigns agents to the shifts array until the demands are satisfied. This is a heuristic that assumes that
        assigning agents in the first timestemp until the demands are satisifed

        :return:
        """
        for i in range(len(self.demands)):
            j = self._get_free_shift(shifts=shifts)
            condition_met = all(demands <= np.sum(shifts, axis=1))
            service_ineffiecency = self.get_service_efficiency(demands, shifts)
            self.log("Service Inefficiency is : {}".format(service_ineffiecency), "debug")
            self.log("Condition met: {}".format(condition_met), "debug")
            sum_agents = np.sum(shifts[i, :])
            if sum_agents < self.demands[i] and \
                    i <= shifts.shape[0] - self.number_intervals_per_agent:
                shifts[i:i + self.number_intervals_per_agent, j] = self.demands[i] - sum_agents
            else:
                if np.sum(shifts[i, :]) < self.demands[i]:
                    condition_met = False
                    while not condition_met:
                        shifts = self._get_optimal_next_agent(demands=demands, shifts=shifts)
                        self.get_service_efficiency(demands, shifts)
                        if np.sum(shifts[i, :]) >= self.demands[i]:

                            condition_met = True

        return shifts


if __name__ == "__main__":
    agents_per_hour = [12, 10, 13, 12, 15, 24, 22, 33, 36, 40, 31, 29, 24, 27, 22, 24, 31, 33, 34, 31, 24, 19, 10,
                       12, 12, 7, 10, 7]
    agents_excel_sheet = [12, 12, 14, 21, 21, 28, 22, 33, 36, 40, 41, 50, 50, 35, 46, 50, 50, 34, 38, 33, 26, 22, 21,
                          17, 17, 14, 10, 7]
    start = datetime.datetime.now()
    scheduler = SchedulerSemiGreedy(demands=agents_per_hour, lunch_time=2,
                                    number_intervals_per_agent=17, lunch_time_border=6)
    resulting_shifts = scheduler.solve()
    print("Took {} time!".format(datetime.datetime.now() - start))
    print(np.sum(resulting_shifts, axis=1))
    print(scheduler.get_service_efficiency(demands=np.array(agents_per_hour), shifts=np.array(agents_excel_sheet)))
    print(scheduler.get_service_efficiency(demands=np.array(agents_per_hour), shifts=resulting_shifts))
    fig = scheduler.plot()
    fig.show()

    agents_per_hour_new = [2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 8, 4, 4, 4, 4, 4, 4, 4, 7]

    start = datetime.datetime.now()
    scheduler = SchedulerSemiGreedy(demands=agents_per_hour_new, lunch_time=2,
                                    number_intervals_per_agent=17, lunch_time_border=6)
    resulting_shifts_new = scheduler.solve()
    print("Took {} time!".format(datetime.datetime.now() - start))
    print(np.sum(resulting_shifts_new, axis=1))
    print(scheduler.get_service_efficiency(demands=np.array(agents_per_hour_new), shifts=resulting_shifts_new))
    figure = scheduler.plot()
    figure.show()
