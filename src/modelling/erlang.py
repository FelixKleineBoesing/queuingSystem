from src.modelling.helpers import power_faculty


class ErlangB:

    def __init__(self, number_agents: int, workload: float):
        self.a = workload
        self.c = number_agents

    def get_probability(self):
        """
        calculates the probability that there are c number people in the system

        :return:
        """
        sum = 0.0
        for i in range(self.c + 1):
            sum += power_faculty(self.a, i)
        return sum


if __name__ == "__main__":
    print(power_faculty(10, 2))
    erlang = ErlangB(9, 7)
    print(erlang.get_probability())
