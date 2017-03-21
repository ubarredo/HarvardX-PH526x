import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.decomposition
from matplotlib.colors import ListedColormap
from scipy import stats
from sklearn.neighbors import KNeighborsClassifier


def predict_knn(p, points, types, k):
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = np.sqrt(np.sum(np.power(p - points[i], 2)))
    ind = distances.argsort()
    return stats.mode(types[ind[:k]])[0][0]


data = pd.read_csv('docs/wine.csv')
numeric_data = data.drop('color', 1).drop('high_quality', 1).drop('quality', 1)
numeric_data = numeric_data.sub(numeric_data.mean(0))
numeric_data = numeric_data.div(numeric_data.std(0, ddof=0))

test_ind = random.sample(range(len(data)), round(len(data) * 0.01))
train_ind = [i for i in range(len(data)) if i not in test_ind]
predictors = np.array(numeric_data)
outcomes = np.array(data['high_quality'])

start_t = time.time()
my_predictions = np.array(
    [predict_knn(p, predictors[train_ind], outcomes[train_ind],
                 k=5) for p in predictors[test_ind]])
my_time = time.time() - start_t
my_accuracy = 100 * np.mean([my_predictions == outcomes[test_ind]])

start_t = time.time()
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(predictors[train_ind], outcomes[train_ind])
sk_predictions = knn.predict(predictors[test_ind])
sk_time = time.time() - start_t
sk_accuracy = 100 * np.mean([sk_predictions == outcomes[test_ind]])

comparision = pd.DataFrame(columns=('accuracy', 'time'))
comparision.loc['my_method'] = (my_accuracy, my_time)
comparision.loc['scikit_method'] = (sk_accuracy, sk_time)
print(comparision)

pca = sklearn.decomposition.PCA(n_components=2)
principal_components = pca.fit_transform(numeric_data)
observation_colormap = ListedColormap(['white', 'red'])
plt.title("Principal Components of Wine")
plt.scatter(principal_components[:, 0],
            principal_components[:, 1],
            c=data['high_quality'],
            cmap=observation_colormap,
            alpha=.8,
            edgecolors='black')
plt.xlim(-8, 8)
plt.ylim(-8, 8)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.savefig('plots/wine_classification')
plt.show()
