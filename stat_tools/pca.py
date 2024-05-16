"""
    Principal Component Analysis
"""
import sys
import csv

import numpy as np
from matplotlib import pyplot as plt

from sklearn import decomposition
from sklearn.preprocessing import StandardScaler


def save_pca_data():
    pass


def read_data(file_name):
    with open(file_name) as data_csv:
        reader = csv.reader(data_csv, delimiter=',')
        header = None
        labels = []
        data = []
        for line in reader:
            if not header:
                header = line[1:]
                continue
            labels.append(line[0])
            data.append([float(num) for num in line[1:]])

    return data, labels, header


def draw_pca_3d(x, y, z, variants=None):
    fig = plt.figure(1, figsize=(4, 3))
    plt.clf()

    ax = fig.add_subplot(111, projection="3d", elev=48, azim=134)
    ax.set_position([0, 0, 0.95, 1])
    plt.cla()

    if variants:
        if not isinstance(variants, np.ndarray):
            variants = np.asarray(variants)
        color = ["b", "r", "g", "y", "k"]  # TODO add some color generator
        for ii, item in enumerate(set(variants)):
            x_i = x[variants == item]
            y_i = y[variants == item]
            z_i = z[variants == item]
            ax.scatter(x_i, y_i, z_i, c=color[ii], label=item)

        plt.legend()
    else:
        ax.scatter(x, y, z)
    plt.show()


def perform_pca(data, variants=None, normalize_data=True, draw=True):
    """
    :param data
    :param variants
    :return: (pc_1, pc_2, pc_3), pca_object
    """
    if not isinstance(data, np.ndarray):
        data = np.asarray(data)
    if normalize_data:
        # Standardize features by removing the mean and scaling to unit variance, z = (x - u) / s
        data = StandardScaler().fit_transform(data)

    pca = decomposition.PCA(n_components=3)
    pca.fit(data)
    data_fitted = pca.transform(data)
    assert data_fitted.shape == (data.shape[0], 3), data_fitted.shape

    pc_1 = data_fitted[:, 0]
    pc_2 = data_fitted[:, 1]
    pc_3 = data_fitted[:, 2]
    # TODO save_pca_data()

    print("components_")
    print(pca.components_)
    print("explained_variance_")
    print(pca.explained_variance_)
    print("explained_variance_ratio_")
    print(pca.explained_variance_ratio_)
    print("singular_values_")
    print(pca.singular_values_)
    print("mean_")
    print(pca.mean_)
    print("n_components_")
    print(pca.n_components_)
    print("noise_variance_")
    print(pca.noise_variance_)

    if draw:
        draw_pca_3d(pc_1, pc_2, pc_3, variants = variants)

    return (pc_1, pc_2, pc_3), pca


if __name__ == "__main__":
    data, labels, header = read_data(sys.argv[1])
    perform_pca(data, variants=labels)