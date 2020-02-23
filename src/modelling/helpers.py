def power_faculty(x: float, n: float) -> float:
    result = 1
    for i in range(1, int(n + 1)):
        result = result * x / i
    return result


def get_p0_for_mmc_system(workload: float, number_agents: int):
    result = 0
    for i in range(number_agents):
        result += power_faculty(workload, i)

    result += power_faculty(workload, number_agents) * number_agents / (number_agents - workload)

    if result > 0:
        return 1 / result
    else:
        return 0