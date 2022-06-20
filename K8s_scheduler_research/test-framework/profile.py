import utils.scraper_utils as su
import run_subprocess as rs
import json
import sys


def run(replicas, role):
    rs.scrape_k8s("kubectl apply -f deployment/follower.yml")
    rs.scrape_k8s("kubectl scale deployment/redis-follower --replicas=" + str(replicas))
    m_time = 0
    break_while = 1

    deployment_time = 0
    termination_time = 0
    # get deployment time
    while break_while != 0:
        items = json.loads(rs.scrape_k8s(su.get_pods_info_json(role)))
        all_running = 1

        for item in items:
            status = item["phase"]
            name = item["name"]

            if m_time == 0:
                m_time = su.current_milli_time()

            if status != "Running":
                all_running = 0

            if all_running == 1 and len(items) > 0:
                deployment_time = su.current_milli_time() - m_time
                break_while = 0
                break

            # g.labels(name, status).set_to_current_time()
            # push_to_gateway('localhost:9091', job='scrape_k8s', registry=registry)
    rs.scrape_k8s("kubectl delete deployment -l role=follower")

    # get termination time
    m_time = su.current_milli_time()
    while 1 != 0:
        items = json.loads(rs.scrape_k8s(su.get_pods_info_json(sys.argv[1])))
        if len(items) == 0:
            termination_time = su.current_milli_time() - m_time
            break

    return deployment_time/1000, termination_time/1000
