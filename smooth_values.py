import random

import matplotlib.pyplot as plt


def moving_window_average(n_list, sm=1):
    width = 1 + 2 * sm
    n_list_ext = sm * [n_list[0]] + n_list + sm * [n_list[-1]]
    return [sum(n_list_ext[i:i + width]) / width for i in range(len(n_list))]


numbers = 100
points = [random.uniform(0, 1) for i in range(numbers)]
y = [points] + [moving_window_average(points, i) for i in range(1, 100)]
ranges = [max(e) - min(e) for e in y]

plt.figure(figsize=(10, 4))
plt.subplot(121)
plt.plot(y[0], label="sm=0")
plt.plot(y[round(len(y) / 10)], label="sm=" + str(round(len(y) / 10)))
plt.plot(y[-1], label="sm=" + str(len(y)))
plt.legend()
plt.xlabel("point")
plt.ylabel("value")
plt.subplot(122)
plt.plot(ranges)
plt.xlabel("sm")
plt.ylabel("range")
plt.savefig('plots/smooth_values')
plt.show()
