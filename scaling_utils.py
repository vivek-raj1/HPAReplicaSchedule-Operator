"""
The scale_hpa function loads the Kubernetes configuration, retrieves an existing HPA resource from the API server, updates its minimum and maximum replica counts, and then replaces the existing HPA resource with the updated one. 
This function is designed to programmatically adjust the scaling parameters of an HPA in a Kubernetes cluster.
"""
from kubernetes import client, config

def scale_hpa(namespace, hpa_name, min_replicas, max_replicas):
    config.load_incluster_config()
    api_instance = client.AutoscalingV1Api()

    hpa = api_instance.read_namespaced_horizontal_pod_autoscaler(name=hpa_name, namespace=namespace)
    hpa.spec.min_replicas = min_replicas
    hpa.spec.max_replicas = max_replicas

    api_instance.replace_namespaced_horizontal_pod_autoscaler(name=hpa_name, namespace=namespace, body=hpa)
