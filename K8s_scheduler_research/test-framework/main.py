import sys
import math
import itertools
from numpy import logspace
from profile import run
from plot_results import plot_results

# Role
role = sys.argv[1]

# Number of nodes to scale
upperbound_no_nodes = int(sys.argv[2])

# Number of containers to scale up to
upperbound_no_containers = int(sys.argv[3])


# Limit the number of nodes to 2^7=64 nodes max
for no_nodes in logspace(0, 7, num=7, base=2, endpoint=False, dtype='int'):
    if no_nodes <= upperbound_no_nodes:
        print("Starting new testing sequence with {} nodes ...".format(no_nodes))

        containers = []
        dts = []
        tts = []
        for no_contaiers in itertools.chain(range(1, 5), range(8, upperbound_no_containers, 4)):
            if no_contaiers <= upperbound_no_containers:
                print("    {} containers ...".format(no_contaiers))
                dt, tt = run(no_contaiers, role)
                containers.append(no_contaiers)
                dts.append(dt)
                tts.append(tt)

        plot_results(containers, 'No. of containers', dts, 'Deployment time (s)')
        plot_results(containers, 'No. of containers', tts, 'Termination time (s)')
