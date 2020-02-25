def power_faculty(x: float, n: float) -> float:
    result = 1
    for i in range(1, int(n + 1)):
        result = result * x / i
    return result


