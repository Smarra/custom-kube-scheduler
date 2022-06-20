import sys

import matplotlib.pyplot as plt


class MyPlot:
    fig, (ax1, ax2) = plt.subplots(1, 2)

    def add_to_plot_1(self, x, y, label):
        self.ax1.plot(x, y, marker=".", markersize=5, label=label)

    def add_to_plot_2(self, x, y, label):
        self.ax2.plot(x, y, marker=".", markersize=5, label=label)

    def plot_results(self, x_label, y1_label, y2_label):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        self.ax1.set_xlabel(x_label)
        self.ax1.set_ylabel(y1_label)
        self.ax1.legend(loc="upper left")
        self.ax2.set_xlabel(x_label)
        self.ax2.set_ylabel(y2_label)
        self.ax2.legend(loc="upper left")

        plt.show()


# plot = MyPlot()
# plot.add_to_plot_1([1,2], [1,2], "1 nodes")
# plot.add_to_plot_1([1,2], [3,4], "2 nodes")
#
# plot.add_to_plot_2([1,2], [1,2], "1 node")
# plot.add_to_plot_2([1,2], [3,4], "2 nodes")
# plot.plot_results("No. containers", "Deployment time (s)", "Termination time (s)")
