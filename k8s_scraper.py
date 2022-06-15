import json
import subprocess
import time
import sys

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


registry = CollectorRegistry()
g = Gauge('pod_status', 'Last time a batch job successfully finished', registry=registry, labelnames=["pod_name", "status"])


def get_pods_info_json(role):
    base_command = "kubectl get pods -l role={}".format(role)
    return base_command + ' -o=custom-columns=NAME:.metadata.name,phase:.status.phase | tr -s " \t" | tail -n +2 |  jq -nR \'[inputs | split(" ") | { "name": .[0], "phase": .[1] }]\''


def current_milli_time():
    return round(time.time() * 1000)


def scrape_k8s(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    json_response, err = process.communicate()
    if process.returncode == 0:
        return json_response.decode('utf-8')
    else:
        print("Error:", err)
        return "Error: " + "err"


def run(replicas):
    scrape_k8s("kubectl apply -f follower.yml")
    scrape_k8s("kubectl scale deployment/redis-follower --replicas=" + str(replicas))
    m_time = 0
    break_while = 1

    # get deployment time
    while break_while != 0:
        items = json.loads(scrape_k8s(get_pods_info_json(sys.argv[1])))
        all_running = 1

        for item in items:
            status = item["phase"]
            name = item["name"]

            if m_time == 0:
                m_time = current_milli_time()

            if status != "Running":
                all_running = 0

            if all_running == 1 and len(items) > 0:
                print("Deployment. Replicas: {} Time: {} ".format(replicas, current_milli_time() - m_time))
                break_while = 0
                break

            # g.labels(name, status).set_to_current_time()
            # push_to_gateway('localhost:9091', job='scrape_k8s', registry=registry)
    scrape_k8s("kubectl delete deployment -l role=follower")

    # get termination time
    m_time = current_milli_time()
    while 1 != 0:
        items = json.loads(scrape_k8s(get_pods_info_json(sys.argv[1])))
        if len(items) == 0:
            print("Termination. Replicas: {} Time: {} ".format(replicas, current_milli_time() - m_time))
            break

run(1)
run(2)
run(3)
run(4)
for i in range(6, int(sys.argv[2]) + 1, 4):
    run(i)
