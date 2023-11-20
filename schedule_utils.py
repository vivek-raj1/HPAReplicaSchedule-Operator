"""
This code continuously checks for scheduled events defined in the CRD, and when the current time matches a scheduled event time, it verifies the scaling parameters, compares them with the HPA, and performs scaling operations if necessary. 
The script then waits for a brief interval before checking again.
"""

import time, logging
from kubernetes import client, config
from scaling_utils import scale_hpa
from next_schedule_utils import get_next_event_time
from datetime import datetime, timezone, timedelta
from day_range_validation import is_valid_day_range

logging.basicConfig(filename='/dev/stdout', filemode='w', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
def hpa_replica_operator():
    config.load_incluster_config()
    custom_api = client.CustomObjectsApi()

    group, version = "api.techsre.io", "v1alpha1"
    plural = "hpareplicaschedules"

    hpa_last_patched = {}  # Dictionary to store the last patched time for each HPA

    while True:
        logging.info("Checking for HPAReplicaSchedule matches...")
        response = custom_api.list_cluster_custom_object(group, version, plural)
        for item in response.get("items", []):
            spec = item.get("spec", {})
            for schedule in spec.get("schedules", []):
                schedule_hour = schedule["hour"]
                schedule_minute = schedule["minute"]
                min_replicas = schedule["minReplicas"]
                max_replicas = schedule["maxReplicas"]
                days_range = schedule["daysOfWeek"]
                # Check if the current day is within the specified range
                if is_valid_day_range(days_range):
                    # Calculate the next event time
                    next_event_time = get_next_event_time(schedule_hour, schedule_minute)
                    logging.info("Scheduled HPA: " + spec["hpaName"] + " MinReplica is " + str(min_replicas) + " and MaxReplica is " + str(max_replicas) + " Next Schedule is: " + str(next_event_time))

                    # Check if the current time matches the schedule time (without milliseconds)
                    if datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%H:%M") == next_event_time.time().strftime("%H:%M"):
                        namespace = spec["namespace"]
                        hpa_name = spec["hpaName"]

                        # Check if min_replicas and max_replicas are equal
                        if min_replicas != max_replicas:
                            # Check if the HPA was patched within the current minute
                            current_minute = datetime.now().strftime("%M")
                            last_patched_minute = hpa_last_patched.get(hpa_name)

                            # Read the current HPA to compare min_replicas and max_replicas
                            config.load_incluster_config()
                            api_instance = client.AutoscalingV1Api()
                            hpa = api_instance.read_namespaced_horizontal_pod_autoscaler(name=hpa_name, namespace=namespace)

                            # Compare the values from CR with the current HPA
                            if hpa.spec.min_replicas != min_replicas or hpa.spec.max_replicas != max_replicas:
                                scale_hpa(namespace, hpa_name, min_replicas, max_replicas)
                                hpa_last_patched[hpa_name] = current_minute

                                logging.info(f"Scaled HPA {hpa_name} to minReplicas: {min_replicas}, maxReplicas: {max_replicas} at {next_event_time.strftime('%Y-%m-%dT%H:%M:%SZ')}")
                            else:
                                logging.info(f"Skipping HPA scaling for {hpa_name} as minReplicas and maxReplicas are already set as specified.")
                        else:
                            logging.info(f"Skipping HPA scaling for {hpa_name} as minReplicas and maxReplicas are equal.")
                else:
                    logging.info(f"Today ({spec['hpaName']}) is not within the specified day range - {days_range}.")
        time.sleep(20)