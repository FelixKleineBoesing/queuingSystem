from sklearn.neighbors import KernelDensity
import numpy as np


# This module benchmarks the calculation of a pdf and sampling from this vs  drawing a sample from the list
data = np.array([[1] * 2 + [2] * 5 + [3] * 6 + [4] * 3 + [5] * 8 + [6] * 12 + [7] * 9 + [8] * 5])
data = data.reshape(data.shape[1], 1)
model = KernelDensity(kernel="gaussian")
model = model.fit(data)
test_values = [[i for i in range(20)]]
