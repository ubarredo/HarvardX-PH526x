import matplotlib.pyplot as plt
import numpy as np

for i in range(4):
    x = np.random.normal(0, 1, (2, 1000))
    y = np.cumsum(x, axis=1)
    z = np.concatenate((np.array([[0], [0]]), y), axis=1)
    plt.plot(z[0], z[1], alpha=1)
plt.savefig('plots/random_walks')
plt.show()
