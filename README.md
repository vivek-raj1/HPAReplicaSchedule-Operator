# HPAReplicaSchedule Operator #

The HPAReplicaSchedule Operator is a Kubernetes operator designed to automate the scaling of Horizontal Pod Autoscalers (HPAs) based on a custom resource definition (CRD) called "HPAReplicaSchedule." This operator allows you to define schedules for adjusting the minimum and maximum replica counts of HPAs, providing an automated way to manage your application's resources according to predefined time-based rules.

### Table of Contents ###

* Overview
* Prerequisites
* Installation
* Usage
* Configuration
* Contributing
* Who do I talk to?

### Overview ###

The HPAReplicaSchedule Operator automates the scaling of HPAs by utilizing a CRD named "HPAReplicaSchedule." This CRD allows you to define schedules with the following parameters:

* Hour and minute of the day to trigger the scaling
* Minimum and maximum replica counts for the HPA

The operator's Python script interacts with the Kubernetes API, monitors the defined schedules, and scales the HPAs accordingly.

### Prerequisites ###
* Kubernetes cluster with RBAC enabled.
* Python 3.x installed.
* Kubernetes Python client library (kubernetes).

### Installation ###

```
helm install [RELEASE NAME] ./odin/charts/hpareplicaschedules -n [NAMESPACE]
```


### Usage ###
1. Create an instance of the HPAReplicaSchedule custom resource to define your scaling schedules. For example:
```
apiVersion: api.techsre.io/v1alpha1
kind: HPAReplicaSchedule
metadata:
  name: example-schedule
spec:
  namespace: prod   #HPA namespace
  hpaName: example-schedule  #HPA Name
  schedules:
    - daysOfWeek: Mon-Sun # You don't need to sepicfy the days of week here. By default this will enable for Mon-Sun (7 days). If you need to schedule hpa based on weekdays like: Mon-Fri, then you have to specify days of week (daysOfWeek: Mon-Fri)
      hour: 17
      maxReplicas: 12
      minReplicas: 4
      minute: 19
    - daysOfWeek: Mon-Sun
      hour: 17
      maxReplicas: 10
      minReplicas: 1
      minute: 20
```
2. The operator will monitor the schedules and scale the HPAs based on the specified timings.

### Configuration ###
The `hpa_replica_operator.py` script may need configuration based on your environment and requirements. Open the script and look for the configuration section to adjust parameters such as sleep interval, time zone, and Kubernetes API access.

### Test ###

1. Get CRD status
```
kubectl get crd hpareplicaschedules.api.techsre.io -o yaml 
```

2. To view deployed `HPAReplicaSchedule` resources
```
kubectl get hrs -n <namespace>
```

### Contribution guidelines ###

* Contributions are welcome! If you find issues, have suggestions, or want to contribute, please open an issue or a pull request in this repository.