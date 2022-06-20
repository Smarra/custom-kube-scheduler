import time

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


registry = CollectorRegistry()
g = Gauge('pod_status', 'Last time a batch job successfully finished', registry=registry, labelnames=["pod_name", "status"])


def get_pods_info_json(role):
    base_command = "kubectl get pods -l role={}".format(role)
    return base_command + ' -o=custom-columns=NAME:.metadata.name,phase:.status.phase | tr -s " \t" | tail -n +2 |  jq -nR \'[inputs | split(" ") | { "name": .[0], "phase": .[1] }]\''


def current_milli_time():
    return round(time.time() * 1000)
