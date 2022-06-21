import sys
import math
import itertools
import run_subprocess as rs
from numpy import logspace
from profile import run
from plot_results import MyPlot


myPlot = MyPlot()

# Role
role = sys.argv[1]

# Number of nodes to scale
upperbound_no_nodes = int(sys.argv[2])

# Number of containers to scale up to
upperbound_no_containers = int(sys.argv[3])


# Limit the number of nodes to 2^7=64 nodes max
for no_nodes in logspace(0, 7, num=7, base=2, endpoint=False, dtype='int'):
    if no_nodes <= upperbound_no_nodes:
        rs.run("az aks scale --resource-group infra-emea1 --name playing-with-k8s --node-count {} --nodepool-name agentpool".format(no_nodes))
        print("Starting new testing sequence with {} nodes ...".format(no_nodes))

        containers = []
        dts = []
        tts = []
        for no_contaiers in itertools.chain(range(1, 5), range(8, upperbound_no_containers + 1, 4)):
            if no_contaiers <= upperbound_no_containers:
                print("    {} containers ...".format(no_contaiers))
                dt, tt = run(no_contaiers, role)
                containers.append(no_contaiers)
                dts.append(dt)
                tts.append(tt)

        myPlot.add_to_plot_1(containers, dts, "{} nodes".format(no_nodes))
        myPlot.add_to_plot_2(containers, tts, "{} nodes".format(no_nodes))


myPlot.plot_results("No. containers", "Deployment time (s)", "Termination time (s)")
rs.run("az aks scale --resource-group infra-emea1 --name playing-with-k8s --node-count 1 --nodepool-name agentpool")