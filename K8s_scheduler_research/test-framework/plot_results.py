import sys

import matplotlib.pyplot as plt


def plot_results(x, x_label, y, y_label):
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc="upper left")
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    plt.plot(x, y, marker=".", markersize=5, label="baseline")
    # plt.plot(x, y2, marker=".", markersize=5, label="improved")

    plt.show()
