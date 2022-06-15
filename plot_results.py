import sys

import matplotlib.pyplot as plt

# Default - 2 nodes
containers = [1, 2, 3, 4, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 74, 78]
deploy_time = [1.619, 1.613, 1.483, 1.501, 1.439, 3.631, 4.546, 6.319, 9.163, 8.813, 11.342, 9.894, 17.185, 12.487, 10.051, 15.745, 16.391, 9.640, 23.674, 23.230, 15.350, 27.594, 29.312]
deploy_time_improved = [1.377, 1.002, 0.934, 1.570, 1.852, 2.288, 4.100, 7.033, 9.019, 9.797, 10.523, 12.956, 11.545, 12.409, 16.602, 18.138, 17.486, 21.860, 14.098, 21.001, 32.772, 34.739, 28.700]


termination_time = [32.959, 33.000, 33.048, 33.018, 33.316, 32.502, 34.821, 36.273, 38.175, 40.427, 41.270, 41.522, 42.280, 45.510, 45.100, 50.124, 49.174, 48.780, 50.638, 53.052, 53.062, 54.859, 56.268]
termination_time_improved = [33.016, 32.984, 33.088, 32.961, 33.211, 34.155, 34.271, 36.408, 37.775, 38.866, 39.887, 42.255, 44.598, 45.622, 51.739, 48.159, 48.825, 50.523, 51.810, 52.951, 55.842, 56.381, 56.960]

plt.xlabel('No. of containers')

# plt.plot(containers, deploy_time, marker=".", markersize=5, label = "baseline")
# plt.plot(containers, deploy_time_improved, marker=".", markersize=5, label = "improved")
# plt.ylabel('Deployment time (s)')

plt.plot(containers, termination_time, marker=".", markersize=5, label = "baseline")
plt.plot(containers, termination_time_improved, marker=".", markersize=5, label = "improved")
plt.ylabel('Termination time (s)')

plt.legend(loc="upper left")
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.show()
