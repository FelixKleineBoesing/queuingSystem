import numpy as np
import plotly.graph_objects as go
import logging
import abc

from typing import Tuple, Dict


class Scheduler(abc.ABC):
    """
    A Scheduler that inherits from this scheduler must have the attribute shifts.
    Shifts must be a 2D numpy array that has the single shifts in the columns and
    """

    def __init__(self, demands: list, lunch_time: int = 1,
                 number_intervals_per_agent: int = 17, lunch_time_border: int = 6, verbose: bool = True):
        assert isinstance(demands, list)
        assert isinstance(lunch_time, int)
        assert isinstance(number_intervals_per_agent, int)
        assert isinstance(lunch_time_border, int)
        assert isinstance(verbose, bool)
        assert number_intervals_per_agent <= len(demands), "number_intervals_per_agent must be smaller or equal to " \
                                                           "the length of the demands list."
        assert lunch_time_border * 2 + lunch_time <= number_intervals_per_agent, "the lunch_time_border x 2 + lunch_" \
                                                                                 "time has to be smaller or equal " \
                                                                                 "to the number_intervals_per_agent"

        self.number_intervals_per_agent = number_intervals_per_agent
        self.lunch_time = lunch_time
        self.lunch_time_border = lunch_time_border
        self.demands = demands
        self.verbose = verbose
        self.shifts: np.ndarray

    def __getattr__(self, item):
        if item == "shifts" and not hasattr(self, "shifts"):
            raise NotImplementedError("shifts is not implemented for this scheduler! Please add shifts array!")

    @abc.abstractmethod
    def solve(self):
        pass

    def log(self, message: str, level: str = "info"):
        """
        if the scheduler attribute verbose is set to true it will log with the defined logging level

        :param message: message that should be logged
        :param level: default level is info. The levels are possible that are attributes of the logging package
        :return:
        """
        if hasattr(logging, level):
            logging_func = getattr(logging, level)
        else:
            raise ValueError("Wrong logging level!")
        if self.verbose:
            logging_func(message)

    def plot(self, shifts: np.ndarray = None):
        """
        creates a plotly figure which can be shown with .plot().show()

        :return:
        """
        if shifts is None:
            shifts = self.shifts
        fig = go.Figure()
        x = list(range(len(self.demands)))
        fig.add_trace(go.Scatter(x=x, y=self.demands, name="Demands", line={"width": 10, "color": "black"}))
        y = np.zeros((len(x)))
        for index, i in enumerate(self._get_assigned_shifts(shifts=shifts)):
            y += shifts[:, i]
            if index == 0:
                fig.add_trace(go.Scatter(x=x, y=y, fill="tozeroy", name="Shift No. {}".format(index)))
            else:
                fig.add_trace(go.Scatter(x=x, y=y, fill="tonexty", name="Shift No. {}".format(index)))

        return fig

    def _check_lunch_time_constraint(self, shifts: np.ndarray):
        """
        checks if all agents have a lunch_time assigned

        :param shifts:
        :return:
        """
        number_lunch_times = self._check_number_of_lunch_times_to_assign(shifts=shifts)
        return np.all(number_lunch_times == 0)

    @staticmethod
    def _check_demand_satisfied(shifts: np.ndarray, demands: np.ndarray):
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
                k = shifts.shape[0] - 1 - j
                if lower is None:
                    if shifts[j, i] > 0 and j == 0:
                        lower = j
                    elif shifts[j, i] == 0 and shifts[j + 1, i] > 0:
                        lower = j + 1
                if upper is None:
                    if shifts[k, i] > 0 and k == (shifts.shape[0] - 1):
                        upper = k
                    elif shifts[k, i] > 0 and shifts[k + 1, i] == 0:
                        upper = k
                if upper is not None and lower is not None:
                    break
            bounds[i] = (lower, upper)
        return bounds

    @staticmethod
    def _get_assigned_shifts(shifts: np.ndarray):
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

    @staticmethod
    def _get_cost_differential_for_lunch_time_assignment(old_shifts: np.ndarray, new_shifts: np.ndarray,
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
        return service_inefficiency - sum_condition

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