import utils.scraper_utils as su
import run_subprocess as rs
import json
import sys


def run(replicas, role):
    rs.run("./bin/spark-submit     --master k8s://http://127.0.0.1:8001     --deploy-mode cluster     --name music-stats     --executor-memory 512m     --num-executors {}     --conf spark.driver.memory=512m     --conf spark.executor.memory=512m     --conf spark.executor.instances=1     --conf spark.executor.cores=1     --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark     --conf spark.kubernetes.container.image=smarra/spark-py:spark-3.1    --conf spark.hadoop.fs.azure.account.key.test0playwithkubernetes.blob.core.windows.net=qbPuTE...    --packages org.apache.hadoop:hadoop-azure:3.2.1,org.apache.hadoop:hadoop-azure-datalake:3.2.1     --conf spark.driver.extraJavaOptions='-Divy.cache.dir=/tmp -Divy.home=/tmp'     --conf spark.kubernetes.executor.scheduler.name=my-scheduler     --conf spark.kubernetes.file.upload.path=wasbs://container@test0playwithkubernetes.blob.core.windows.net/    analyze_songs.py songs-1gb.csv ".format(replicas), 0)
    m_time = 0
    break_while = 1

    deployment_time = 0
    total_time = 0
    # get deployment time
    while break_while != 0:
        itms = rs.run(su.get_pods_info_json(role))
        items = json.loads(itms)
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

    # get termination time
    while 1 != 0:
        items = json.loads(rs.run(su.get_pods_info_json(role)))
        if len(items) == 0:
            total_time = su.current_milli_time() - m_time
            break

    rs.run("kubectl delete pods -l spark-role=driver")
    return deployment_time/1000, total_time/1000

