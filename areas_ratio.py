import math
import random

import matplotlib.pyplot as plt


def calc_ratio(r, n):
    in_points = []
    out_points = []
    for i in range(n):
        point = (random.uniform(-r, r), random.uniform(-r, r))
        distance = math.sqrt((point[0]) ** 2 + point[1] ** 2)
        if distance < r:
            in_points.append(point)
        else:
            out_points.append(point)
    ratio = len(in_points) / n
    return ratio, in_points, out_points


R = 10
N = 10000
results = calc_ratio(R, N)
print("The ratio of the areas of a circle and the square inscribing it is:")
print(results[0])

fig = plt.figure(figsize=(11, 5))

plt.subplot(121)
plt.xlim(-R, R)
plt.ylim(-R, R)
plt.title("Areas R=%s N=%s" % (R, N))
plt.xlabel("R")
plt.ylabel("R")
plt.scatter(*zip(*results[1]), color='orange', alpha=0.5)
plt.scatter(*zip(*results[2]), color='purple', alpha=0.5)

x1 = range(100, N + 100, 100)
x2 = range(1, R + 1, 1)
y1 = [calc_ratio(R, i)[0] for i in x1]
y2 = [calc_ratio(i, N)[0] for i in x2]
ax1 = fig.add_subplot(122)
ax2 = ax1.twiny()
line1, = ax1.plot(x1, y1, c='blue')
line2, = ax2.plot(x2, y2, c='red')
plt.ylim(0.6, 1.0)
ax1.set_xlabel("N")
ax2.set_xlabel("R")
ax1.set_xlim(100, N)
ax2.set_xlim(1, R)
plt.legend((line1, line2), ("N", "R"))
plt.savefig('plots/areas_ratio')
plt.show()
