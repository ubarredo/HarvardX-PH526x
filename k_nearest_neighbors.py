import random

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss
from matplotlib.colors import ListedColormap
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier


def find_majority(votes):
    vote_dict = {}
    for i in votes:
        if i in vote_dict:
            vote_dict[i] += 1
        else:
            vote_dict[i] = 1
    winners = []
    max_count = max(vote_dict.values())
    for i, j in vote_dict.items():
        if vote_dict[i] == max_count:
            winners.append(i)
    return random.choice(winners)


def predict_knn(p, points, types, k):
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = np.sqrt(np.sum(np.power(p - points[i], 2)))
    ind = distances.argsort()
    return find_majority(types[ind[:k]])


def make_prediction_grid(points, types, k, h=50):
    xs = np.linspace(min(points[:, 0]), max(points[:, 0]), h)
    ys = np.linspace(min(points[:, 1]), max(points[:, 1]), h)
    xx, yy = np.meshgrid(xs, ys)
    grid = np.zeros(xx.shape, dtype=int)
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            p = np.array([x, y])
            grid[j, i] = predict_knn(p, points, types, k)
    return xx, yy, grid


def plot_prediction_grid(points, types, k):
    xx, yy, grid = make_prediction_grid(points, types, k)
    colormap = ListedColormap(['red', 'blue', 'green'])
    plt.pcolormesh(xx, yy, grid, cmap=colormap, alpha=0.4)
    plt.scatter(points[:, 0], points[:, 1], c=types, cmap=colormap, s=50)
    plt.xlabel("Variable 1")
    plt.ylabel("Variable 2")
    plt.xticks(())
    plt.yticks(())
    plt.xlim(np.min(xx), np.max(xx))
    plt.ylim(np.min(yy), np.max(yy))


def generate_synth_data(n=50):
    points = np.concatenate((ss.norm(0, 1).rvs((n, 2)),
                             ss.norm(1, 1).rvs((n, 2))), axis=0)
    types = np.concatenate((np.repeat([0], n), np.repeat([1], n)))
    return points, types


plt.figure(figsize=(11, 5))
plt.subplot(121)
plt.title("Synth data")
predictors, outcomes = generate_synth_data()
plot_prediction_grid(predictors, outcomes, k=5)

plt.subplot(122)
plt.title("Iris data")
iris = datasets.load_iris()
predictors = iris.data[:, 0:2]
outcomes = iris.target
plot_prediction_grid(predictors, outcomes, k=5)
plt.savefig('plots/k_nearest_neighbors')

selection = random.sample(range(len(predictors)), round(len(predictors) * 0.2))
training_indices = [i for i in range(len(predictors)) if i not in selection]
my_predictions = np.array(
    [predict_knn(p, predictors[training_indices], outcomes[training_indices],
                 k=5) for p in predictors[selection]])
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(predictors[training_indices], outcomes[training_indices])
sk_predictions = knn.predict(predictors[selection])
print("My method accuracy:")
print(round(100 * np.mean([my_predictions == outcomes[selection]]), 1), "%")
print("Scikit method accuracy:")
print(round(100 * np.mean([sk_predictions == outcomes[selection]]), 1), "%")
print("Method comparison:")
print(round(100 * np.mean([my_predictions == sk_predictions]), 1), "%")

plt.show()
