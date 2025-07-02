"""
    Draw correlation matrix
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats


def plot_cor_matrix(data, variables, fig_name = "corr_mat", size = 4):
    """
    data.shape = m, n; where m: number of measurements, n: number of variables
    """
    ret_table = []
    m, n = data.shape
    assert len(variables) == n

    fig = plt.figure(figsize=(size, size))
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.05, hspace=0.05)
    cmap = plt.cm.get_cmap('bwr')

    for ii in range(n):
        for jj in range(n):
            ax = fig.add_subplot(n, n, ii * n + jj + 1)
            if ii == jj:
                y = data[:, ii]
                y = y[np.isfinite(y)]
                ax.hist(y, color="k")

            elif jj < ii:
                y_ii = data[:, ii]
                y_jj = data[:, jj]
                idx = np.isfinite(y_ii) & np.isfinite(y_jj)
                rCoeff, pValue = stats.pearsonr(y_jj[idx], y_ii[idx])
                color = cmap((-rCoeff + 1) / 2)
                if pValue <= 0.05:
                    plt.scatter(
                        x=[0],  # X souřadnice bodu (jeden bod)
                        y=[0],  # Y souřadnice bodu (jeden bod)
                        s=abs(rCoeff * 500),  # Velikost bodu
                        c=[color],  # Barva bodu (jeden prvek seznamu)
                        alpha=1
                    )

            elif jj > ii:
                y_ii = data[:, ii]
                y_jj = data[:, jj]
                idx = np.isfinite(y_ii) & np.isfinite(y_jj)
                rCoeff, pValue = stats.pearsonr(y_jj[idx], y_ii[idx])
                # rCoeff, pValue = stats.spearmanr( y_jj[idx], y_ii[idx] )#spearmanr
                s = "%0.2f" % rCoeff

                if pValue <= 0.05:
                    ax.text(0.1, 0.5, s, fontweight='bold', color="k")

                ret_table.append([variables[ii], variables[jj], rCoeff, pValue])

            if jj == 0:
                ax.set_ylabel(variables[ii], fontsize=9)
            if ii == n - 1:
                ax.set_xlabel(variables[jj], fontsize=9)

            plt.tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                            labelleft=False)

    # plt.show()
    plt.savefig(fig_name, dpi=500)

    return ret_table
