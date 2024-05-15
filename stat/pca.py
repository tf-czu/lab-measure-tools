"""
    Principal Component Analysis
"""
import numpy as np
import os
import sys
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import cm
import cv2
from scipy import stats, optimize

from sklearn import decomposition
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D


def save_pca_data():
    pass


def read_data(file_name):
    # TODO some standart format
    pass


def tryPCA(data, header = None, variants_data = None, z_color = None, fractions = None, markers_lab = None ):
    """
    :param data
    :param
    :return: None
    """
    jet = cm.get_cmap('jet_r', 100)
#    plot_lab = ["o", "s", "d", "^", "<", ">"]
#    plot_lab = ["o", "s"]
    cmark = ["r^","g^","b^", "ro", "go", "bo"]
    print(data.shape)
    print(header)

    data2 = StandardScaler().fit_transform(data) #Standardize features by removing the mean and scaling to unit variance, z = (x - u) / s
#    data2 = data
    print(np.mean(data2, 0))
    print(np.min(data2, 0))
    print(np.max(data2, 0))

    pca = decomposition.PCA(n_components=3)
    # pca.fit(mData2)
    data_pca = pca.fit_transform(data2)
    print("data_pca")
    print(data_pca.shape)

    xs = data_pca[:, 0]
    ys = data_pca[:, 1]
    zs = data_pca[:, 2]
    save_pca_data(xs, ys, ys)
    scalex = 1.0 / (xs.max() - xs.min())
    scaley = 1.0 / (ys.max() - ys.min())
    scalez = 1.0 / (zs.max() - zs.min())

    fig = plt.figure(figsize=(5, 4))
    fig.subplots_adjust(left=0.2, bottom=0.15)
    ax = fig.add_subplot(111)
#    for ii in range(len(xs)):
#        ax.scatter(xs[ii] * scalex, ys[ii] * scaley, c=jet(z_color[ii]), lw=2, marker = plot_lab[markers_lab[ii]-1] )
#    ax.scatter(xs[:18] * scalex, ys[:18] * scaley, c=jet(z_color[:18]), lw=1, marker="o", label = "Real wooden chips")
#    ax.scatter(xs[18:] * scalex, ys[18:] * scaley, c=jet(z_color[18:]), lw=1, marker="s", label = "Pure wooden chips")

#    ax.scatter(xs[:5] * scalex, ys[:5] * scaley, c=jet(z_color[:5]), lw=1, marker="^", label="P1")
#    ax.scatter(xs[5:11] * scalex, ys[5:11] * scaley, c=jet(z_color[5:11]), lw=1, marker="s", label ="P2")
#    ax.scatter(xs[11:] * scalex, ys[11:] * scaley, c=jet(z_color[11:]), lw=1, marker="o", label="P3")

#    for ii in range(len(xs)):
#        ax.scatter(xs[ii] * scalex, ys[ii] * scaley, lw=2, c = cmark[markers_lab[ii]-1][0], marker = cmark[markers_lab[ii]-1][1] )

    ax.scatter(xs[:6] * scalex, ys[:6] * scaley, lw=2, c="r", marker="^", label="Fraction 1, real")
    ax.plot(xs[:6] * scalex, ys[:6] * scaley, "-r")
    ax.scatter(xs[6:12] * scalex, ys[6:12] * scaley, lw=2, c="g", marker="^", label="Fraction 2, real")
    ax.plot(xs[6:12] * scalex, ys[6:12] * scaley, "-g")
    ax.scatter(xs[12:18] * scalex, ys[12:18] * scaley, lw=2, c="b", marker="^", label="Fraction 3, real")
    ax.plot(xs[12:18] * scalex, ys[12:18] * scaley, "-b")

    ax.scatter(xs[18:23] * scalex, ys[18:23] * scaley, lw=2, c="r", marker="o", label="Fraction 1, pure")
    ax.plot(xs[18:23] * scalex, ys[18:23] * scaley, "-r")
    ax.scatter(xs[23:28] * scalex, ys[23:28] * scaley, lw=2, c="g", marker="o", label="Fraction 2, pure")
    ax.plot(xs[23:28] * scalex, ys[23:28] * scaley, "-g")
    ax.scatter(xs[28:] * scalex, ys[28:] * scaley, lw=2, c="b", marker="o", label="Fraction 3, pure")
    ax.plot(xs[28:] * scalex, ys[28:] * scaley, "-b")

    coeff = np.transpose(pca.components_[0:2, :])
    for ii in range(12):
        ax.arrow(0, 0, coeff[ii, 0], coeff[ii, 1], color='k', alpha=0.3, head_width = 0.01)
        ax.text(coeff[ii, 0] * 1.5, coeff[ii, 1] * 1.0, header[ii], color='k', ha='center', va='center', fontsize = 6)

    plt.legend(loc="best", shadow=False, scatterpoints=1, fontsize = 8)
    plt.axis([-0.3, 0.8, -0.7, 0.7])
    plt.xlabel("PC1 (%0.2f )" % (pca.explained_variance_ratio_[0]), fontsize = 10)
    plt.ylabel("PC2 (%0.2f )" % (pca.explained_variance_ratio_[1]), fontsize = 10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    # plt.show()
    plt.savefig("PCA_1-2_" + label, dpi=800)
    plt.close()
    """
#    fig 2
    plt.figure(figsize=(6, 5))
    for ii in range(len(xs)):
        plt.scatter(xs[ii] * scalex, zs[ii] * scalez, c=jet(z_color[ii]), lw=2, marker=plot_lab[markers_lab[ii] - 1])

    coeff = np.transpose(pca.components_[[0, 2], :])
    for ii in range(12):
        plt.arrow(0, 0, coeff[ii, 0], coeff[ii, 1], color='y', alpha=0.5)
        plt.text(coeff[ii, 0] * 1.2, coeff[ii, 1] * 1.2, header[ii], color='k', ha='center', va='center')

    #    plt.legend(loc="best", shadow=False, scatterpoints=1)
    plt.axis([-1, 1, -1, 1])
    plt.xlabel("PC1 (%0.2f )" % (pca.explained_variance_ratio_[0]))
    plt.ylabel("PC3 (%0.2f )" % (pca.explained_variance_ratio_[2]))
    # plt.show()
    plt.savefig("PCA_1-3_" + label, dpi=800)
    plt.close()

#    3D
    fig = plt.figure(1, figsize=(8, 8))
    plt.clf()
    ax = Axes3D(fig, rect=(0, 0, .95, 1), elev=48, azim=134)
    plt.cla()
    for ii in range(len(xs)):
        ax.scatter(xs[ii], ys[ii], zs[ii], c=jet(z_color[ii]), lw=2, marker=plot_lab[markers_lab[ii] - 1])

    ax.legend(loc="best", shadow=False, scatterpoints=1)
    plt.show()
    """
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


def processing_data(data_file):
    header = None
    data = []
    fractions = []
    mc_data = []
    markers = []
    f = open(data_file)
    for line in f:
        line = line.split(",")
        if header is None:
            header = line[:12]
        else:
            markers.append(int(line[-2]))
            mc_data.append(float(line[12]))  #12 for MC, 14 for AIR, log data: 12 and 13
            data.append([float(x) for x in line[:12]])

    data = np.array(data)
    tryPCA(data, header = header, z_color = mc_data, markers_lab = markers)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit()

    data_file = sys.argv[1]
    label = sys.argv[2]
    processing_data(data_file)