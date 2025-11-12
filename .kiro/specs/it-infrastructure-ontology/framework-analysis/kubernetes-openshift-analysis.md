# Kubernetes and OpenShift API Analysis

## Overview

This document provides a comprehensive analysis of Kubernetes and OpenShift APIs, extracting entity types, attributes, and relationships for the Container and Orchestration layer (Layer 3) of the IT Infrastructure and Application Dependency Ontology.

**Kubernetes Version**: 1.28+
**OpenShift Version**: 4.14+
**API Sources**: Kubernetes API Reference, OpenShift API Extensions
**Analysis Date**: 2025-11-09

---

## Part 1: Kubernetes Core API Analysis

### Kubernetes Overview

Kubernetes is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications. The Kubernetes API defines resources (objects) that represent the desired state of the cluster.

---

### 1. Pod

**Kubernetes Definition**: The smallest deployable unit in Kubernetes, representing one or more containers that share storage and network resources.

**API Group**: `core/v1`
**Kind**: `Pod`

**Attributes**:
- `metadata.name` (string, mandatory): Pod name
- `metadata.namespace` (string, mandatory): Namespace containing the pod
- `metadata.labels` (map[string]string, optional): Key-value labels for organization
- `metadata.annotations` (map[string]string, optional): Non-identifying metadata
- `spec.containers` (array, mandatory): List of containers in the pod
- `spec.containers[].name` (string, mandatory): Container name
- `spec.containers[].image` (string, mandatory): Container image reference
- `spec.containers[].ports` (array, optional): Exposed container ports
- `spec.containers[].resources.requests` (object, optional): Minimum resource requirements
- `spec.containers[].resources.limits` (object, optional): Maximum resource limits
- `spec.volumes` (array, optional): Volumes available to containers
- `spec.nodeName` (string, optional): Node where pod is scheduled
- `spec.restartPolicy` (enum: Always, OnFailure, Never, optional): Container restart policy
- `status.phase` (enum: Pending, Running, Succeeded, Failed, Unknown, mandatory): Pod lifecycle phase
- `status.conditions` (array, optional): Current pod conditions
- `status.podIP` (string, optional): IP address allocated to pod
- `status.hostIP` (string, optional): IP address of host node
- `status.startTime` (timestamp, optional): Pod start time

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Pod
- Core orchestration unit that groups containers

---

### 2. Deployment

**Kubernetes Definition**: A controller that provides declarative updates for Pods and ReplicaSets.

**API Group**: `apps/v1`
**Kind**: `Deployment`

**Attributes**:
- `metadata.name` (string, mandatory): Deployment name
- `metadata.namespace` (string, mandatory): Namespace containing the deployment
- `metadata.labels` (map[string]string, optional): Key-value labels
- `spec.replicas` (integer, optional, default: 1): Desired number of pod replicas
- `spec.selector` (object, mandatory): Label selector for pods
- `spec.template` (object, mandatory): Pod template specification
- `spec.strategy.type` (enum: RollingUpdate, Recreate, optional): Deployment strategy
- `spec.strategy.rollingUpdate.maxUnavailable` (int/string, optional): Max unavailable pods during update
- `spec.strategy.rollingUpdate.maxSurge` (int/string, optional): Max extra pods during update
- `spec.minReadySeconds` (integer, optional): Minimum ready time before considering pod available
- `spec.revisionHistoryLimit` (integer, optional): Number of old ReplicaSets to retain
- `status.replicas` (integer, optional): Total number of replicas
- `status.availableReplicas` (integer, optional): Number of available replicas
- `status.readyReplicas` (integer, optional): Number of ready replicas
- `status.conditions` (array, optional): Deployment conditions

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Deployment
- Manages pod lifecycle and scaling

---

### 3. Service

**Kubernetes Definition**: An abstract way to expose an application running on a set of Pods as a network service.

**API Group**: `core/v1`
**Kind**: `Service`

**Attributes**:
- `metadata.name` (string, mandatory): Service name
- `metadata.namespace` (string, mandatory): Namespace containing the service
- `metadata.labels` (map[string]string, optional): Key-value labels
- `spec.selector` (map[string]string, mandatory): Label selector for pods
- `spec.type` (enum: ClusterIP, NodePort, LoadBalancer, ExternalName, mandatory): Service type
- `spec.clusterIP` (string, optional): Internal cluster IP address
- `spec.ports` (array, mandatory): Service port specifications
- `spec.ports[].name` (string, optional): Port name
- `spec.ports[].protocol` (enum: TCP, UDP, SCTP, optional, default: TCP): Protocol
- `spec.ports[].port` (integer, mandatory): Service port
- `spec.ports[].targetPort` (int/string, mandatory): Target pod port
- `spec.ports[].nodePort` (integer, optional): Node port for NodePort/LoadBalancer types
- `spec.sessionAffinity` (enum: None, ClientIP, optional): Session affinity type
- `spec.externalIPs` (array, optional): External IP addresses
- `spec.loadBalancerIP` (string, optional): Load balancer IP address
- `status.loadBalancer.ingress` (array, optional): Load balancer ingress points

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Service
- Exposes pods as network services

---

### 4. Namespace

**Kubernetes Definition**: A mechanism for isolating groups of resources within a single cluster.

**API Group**: `core/v1`
**Kind**: `Namespace`

**Attributes**:
- `metadata.name` (string, mandatory): Namespace name
- `metadata.labels` (map[string]string, optional): Key-value labels
- `spec.finalizers` (array, optional): Finalizers for namespace deletion
- `status.phase` (enum: Active, Terminating, mandatory): Namespace phase

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Namespace
- Provides logical isolation and resource quotas

---

### 5. Ingress

**Kubernetes Definition**: An API object that manages external access to services, typically HTTP/HTTPS.

**API Group**: `networking.k8s.io/v1`
**Kind**: `Ingress`

**Attributes**:
- `metadata.name` (string, mandatory): Ingress name
- `metadata.namespace` (string, mandatory): Namespace containing the ingress
- `metadata.annotations` (map[string]string, optional): Ingress controller configuration
- `spec.ingressClassName` (string, optional): Ingress controller class
- `spec.defaultBackend` (object, optional): Default backend service
- `spec.tls` (array, optional): TLS configuration
- `spec.tls[].hosts` (array, optional): Hostnames for TLS certificate
- `spec.tls[].secretName` (string, optional): Secret containing TLS certificate
- `spec.rules` (array, optional): Ingress routing rules
- `spec.rules[].host` (string, optional): Hostname for routing
- `spec.rules[].http.paths` (array, mandatory): HTTP path routing rules
- `spec.rules[].http.paths[].path` (string, mandatory): URL path
- `spec.rules[].http.paths[].pathType` (enum: Exact, Prefix, ImplementationSpecific, mandatory): Path matching type
- `spec.rules[].http.paths[].backend.service.name` (string, mandatory): Backend service name
- `spec.rules[].http.paths[].backend.service.port` (object, mandatory): Backend service port
- `status.loadBalancer.ingress` (array, optional): Ingress load balancer addresses

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): IngressController
- Manages external HTTP/HTTPS access to services

---

### 6. ConfigMap

**Kubernetes Definition**: An API object used to store non-confidential configuration data in key-value pairs.

**API Group**: `core/v1`
**Kind**: `ConfigMap`

**Attributes**:
- `metadata.name` (string, mandatory): ConfigMap name
- `metadata.namespace` (string, mandatory): Namespace containing the ConfigMap
- `data` (map[string]string, optional): Configuration data
- `binaryData` (map[string][]byte, optional): Binary configuration data

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Configuration resource
- Stores application configuration

---

### 7. Secret

**Kubernetes Definition**: An API object used to store sensitive information such as passwords, tokens, or keys.

**API Group**: `core/v1`
**Kind**: `Secret`

**Attributes**:
- `metadata.name` (string, mandatory): Secret name
- `metadata.namespace` (string, mandatory): Namespace containing the secret
- `type` (string, optional): Secret type (Opaque, kubernetes.io/tls, etc.)
- `data` (map[string][]byte, optional): Base64-encoded secret data
- `stringData` (map[string]string, optional): Plain text secret data

**Ontology Mapping**:
- Layer 6 (Security Infrastructure): Certificate, credentials
- Stores sensitive configuration data

---

### 8. PersistentVolume (PV)

**Kubernetes Definition**: A piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned.

**API Group**: `core/v1`
**Kind**: `PersistentVolume`

**Attributes**:
- `metadata.name` (string, mandatory): PV name
- `spec.capacity.storage` (string, mandatory): Storage capacity (e.g., "10Gi")
- `spec.accessModes` (array, mandatory): Access modes (ReadWriteOnce, ReadOnlyMany, ReadWriteMany)
- `spec.persistentVolumeReclaimPolicy` (enum: Retain, Recycle, Delete, optional): Reclaim policy
- `spec.storageClassName` (string, optional): Storage class name
- `spec.volumeMode` (enum: Filesystem, Block, optional): Volume mode
- `spec.nfs` (object, optional): NFS volume configuration
- `spec.iscsi` (object, optional): iSCSI volume configuration
- `spec.csi` (object, optional): CSI volume configuration
- `status.phase` (enum: Pending, Available, Bound, Released, Failed, mandatory): PV phase

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): StorageVolume
- Represents cluster storage resources

---

### 9. PersistentVolumeClaim (PVC)

**Kubernetes Definition**: A request for storage by a user.

**API Group**: `core/v1`
**Kind**: `PersistentVolumeClaim`

**Attributes**:
- `metadata.name` (string, mandatory): PVC name
- `metadata.namespace` (string, mandatory): Namespace containing the PVC
- `spec.accessModes` (array, mandatory): Requested access modes
- `spec.resources.requests.storage` (string, mandatory): Requested storage size
- `spec.storageClassName` (string, optional): Storage class name
- `spec.volumeName` (string, optional): Specific PV to bind to
- `spec.volumeMode` (enum: Filesystem, Block, optional): Volume mode
- `status.phase` (enum: Pending, Bound, Lost, mandatory): PVC phase
- `status.capacity.storage` (string, optional): Actual allocated storage

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Storage claim
- Links pods to persistent storage

---

### 10. StatefulSet

**Kubernetes Definition**: A controller for managing stateful applications with stable network identities and persistent storage.

**API Group**: `apps/v1`
**Kind**: `StatefulSet`

**Attributes**:
- `metadata.name` (string, mandatory): StatefulSet name
- `metadata.namespace` (string, mandatory): Namespace containing the StatefulSet
- `spec.replicas` (integer, optional, default: 1): Desired number of replicas
- `spec.selector` (object, mandatory): Label selector for pods
- `spec.serviceName` (string, mandatory): Headless service name
- `spec.template` (object, mandatory): Pod template specification
- `spec.volumeClaimTemplates` (array, optional): PVC templates for each replica
- `spec.podManagementPolicy` (enum: OrderedReady, Parallel, optional): Pod creation policy
- `spec.updateStrategy.type` (enum: RollingUpdate, OnDelete, optional): Update strategy
- `status.replicas` (integer, optional): Total number of replicas
- `status.readyReplicas` (integer, optional): Number of ready replicas

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Deployment (stateful variant)
- Manages stateful application pods

---

### 11. DaemonSet

**Kubernetes Definition**: A controller that ensures all (or some) nodes run a copy of a pod.

**API Group**: `apps/v1`
**Kind**: `DaemonSet`

**Attributes**:
- `metadata.name` (string, mandatory): DaemonSet name
- `metadata.namespace` (string, mandatory): Namespace containing the DaemonSet
- `spec.selector` (object, mandatory): Label selector for pods
- `spec.template` (object, mandatory): Pod template specification
- `spec.updateStrategy.type` (enum: RollingUpdate, OnDelete, optional): Update strategy
- `status.numberReady` (integer, optional): Number of ready pods
- `status.desiredNumberScheduled` (integer, optional): Desired number of pods

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Deployment (daemon variant)
- Ensures pod runs on each node

---

### 12. Node

**Kubernetes Definition**: A worker machine in Kubernetes, either a virtual or physical machine.

**API Group**: `core/v1`
**Kind**: `Node`

**Attributes**:
- `metadata.name` (string, mandatory): Node name
- `metadata.labels` (map[string]string, optional): Node labels
- `spec.podCIDR` (string, optional): Pod IP range for this node
- `spec.taints` (array, optional): Node taints for pod scheduling
- `status.capacity` (object, optional): Total node resources (cpu, memory, pods)
- `status.allocatable` (object, optional): Allocatable node resources
- `status.conditions` (array, optional): Node conditions (Ready, MemoryPressure, etc.)
- `status.addresses` (array, optional): Node addresses (InternalIP, ExternalIP, Hostname)
- `status.nodeInfo.kubeletVersion` (string, optional): Kubelet version
- `status.nodeInfo.containerRuntimeVersion` (string, optional): Container runtime version
- `status.nodeInfo.operatingSystem` (string, optional): Operating system
- `status.nodeInfo.architecture` (string, optional): CPU architecture

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): VirtualMachine or PhysicalServer
- Represents cluster compute nodes

---

## Part 2: OpenShift API Extensions

### OpenShift Overview

OpenShift is Red Hat's enterprise Kubernetes platform that adds developer and operational tools on top of Kubernetes. OpenShift extends the Kubernetes API with additional resources.

---

### 1. Route

**OpenShift Definition**: An OpenShift-specific resource that exposes a service at a hostname for external access.

**API Group**: `route.openshift.io/v1`
**Kind**: `Route`

**Attributes**:
- `metadata.name` (string, mandatory): Route name
- `metadata.namespace` (string, mandatory): Namespace containing the route
- `spec.host` (string, optional): External hostname (auto-generated if not specified)
- `spec.path` (string, optional): URL path prefix
- `spec.to.kind` (string, mandatory): Target resource kind (typically "Service")
- `spec.to.name` (string, mandatory): Target service name
- `spec.to.weight` (integer, optional): Traffic weight for load balancing
- `spec.port.targetPort` (string, mandatory): Target service port
- `spec.tls.termination` (enum: edge, passthrough, reencrypt, optional): TLS termination type
- `spec.tls.certificate` (string, optional): TLS certificate
- `spec.tls.key` (string, optional): TLS private key
- `spec.tls.caCertificate` (string, optional): CA certificate
- `spec.tls.destinationCACertificate` (string, optional): Destination CA certificate (for reencrypt)
- `spec.tls.insecureEdgeTerminationPolicy` (enum: None, Allow, Redirect, optional): HTTP behavior
- `spec.wildcardPolicy` (enum: None, Subdomain, optional): Wildcard hostname support
- `status.ingress` (array, optional): Route ingress status

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Route
- OpenShift-specific external access mechanism

**Key Differences from Kubernetes Ingress**:
- Simpler configuration for basic use cases
- Native TLS termination types (edge, passthrough, reencrypt)
- Automatic hostname generation
- Per-route configuration vs. Ingress controller-wide configuration

---

### 2. DeploymentConfig

**OpenShift Definition**: An OpenShift-specific deployment resource with additional features beyond Kubernetes Deployments.

**API Group**: `apps.openshift.io/v1`
**Kind**: `DeploymentConfig`

**Attributes**:
- `metadata.name` (string, mandatory): DeploymentConfig name
- `metadata.namespace` (string, mandatory): Namespace containing the DeploymentConfig
- `spec.replicas` (integer, optional, default: 1): Desired number of replicas
- `spec.selector` (map[string]string, mandatory): Label selector for pods
- `spec.template` (object, mandatory): Pod template specification
- `spec.strategy.type` (enum: Rolling, Recreate, Custom, optional): Deployment strategy
- `spec.triggers` (array, optional): Automatic deployment triggers
- `spec.triggers[].type` (enum: ConfigChange, ImageChange, optional): Trigger type
- `spec.triggers[].imageChangeParams` (object, optional): Image change trigger configuration
- `spec.revisionHistoryLimit` (integer, optional): Number of old ReplicationControllers to retain
- `status.replicas` (integer, optional): Total number of replicas
- `status.availableReplicas` (integer, optional): Number of available replicas
- `status.latestVersion` (integer, optional): Latest deployment version

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Deployment
- OpenShift-specific deployment controller

**Key Differences from Kubernetes Deployment**:
- Automatic triggers for image changes and config changes
- Custom deployment strategies
- Lifecycle hooks (pre, mid, post deployment)

---

### 3. ImageStream

**OpenShift Definition**: An abstraction for referencing container images within OpenShift.

**API Group**: `image.openshift.io/v1`
**Kind**: `ImageStream`

**Attributes**:
- `metadata.name` (string, mandatory): ImageStream name
- `metadata.namespace` (string, mandatory): Namespace containing the ImageStream
- `spec.lookupPolicy.local` (boolean, optional): Enable local image lookup
- `spec.tags` (array, optional): Image tags
- `spec.tags[].name` (string, mandatory): Tag name
- `spec.tags[].from.kind` (string, mandatory): Source kind (DockerImage, ImageStreamTag, etc.)
- `spec.tags[].from.name` (string, mandatory): Source image reference
- `spec.tags[].importPolicy.scheduled` (boolean, optional): Periodic import
- `status.dockerImageRepository` (string, optional): Internal registry repository
- `status.tags` (array, optional): Tag status information

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): ContainerImage
- OpenShift-specific image management

---

### 4. BuildConfig

**OpenShift Definition**: Defines a build process for creating container images.

**API Group**: `build.openshift.io/v1`
**Kind**: `BuildConfig`

**Attributes**:
- `metadata.name` (string, mandatory): BuildConfig name
- `metadata.namespace` (string, mandatory): Namespace containing the BuildConfig
- `spec.source.type` (enum: Git, Binary, Dockerfile, Image, optional): Source type
- `spec.source.git.uri` (string, optional): Git repository URI
- `spec.source.git.ref` (string, optional): Git branch/tag reference
- `spec.strategy.type` (enum: Source, Docker, Custom, Pipeline, mandatory): Build strategy
- `spec.output.to.kind` (string, mandatory): Output kind (ImageStreamTag, DockerImage)
- `spec.output.to.name` (string, mandatory): Output image reference
- `spec.triggers` (array, optional): Build triggers
- `status.lastVersion` (integer, optional): Last build version

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Build pipeline
- Not a primary entity type but informs CI/CD processes

---

### 5. Project

**OpenShift Definition**: An OpenShift-specific extension of Kubernetes Namespace with additional metadata and RBAC.

**API Group**: `project.openshift.io/v1`
**Kind**: `Project`

**Attributes**:
- `metadata.name` (string, mandatory): Project name
- `metadata.annotations.openshift.io/description` (string, optional): Project description
- `metadata.annotations.openshift.io/display-name` (string, optional): Display name
- `metadata.annotations.openshift.io/requester` (string, optional): Project creator
- `status.phase` (enum: Active, Terminating, mandatory): Project phase

**Ontology Mapping**:
- Layer 3 (Container & Orchestration): Namespace
- OpenShift-specific namespace with additional metadata

---

## Part 3: Container Orchestration Attributes Summary

### Core Attributes for Layer 3 Entities

**Container Entity**:
- `name` (string, mandatory): Container name
- `image` (string, mandatory): Container image reference
- `image_pull_policy` (enum: Always, IfNotPresent, Never, optional): Image pull policy
- `ports` (array, optional): Exposed ports
- `resources.requests.cpu` (string, optional): Minimum CPU (e.g., "100m")
- `resources.requests.memory` (string, optional): Minimum memory (e.g., "128Mi")
- `resources.limits.cpu` (string, optional): Maximum CPU
- `resources.limits.memory` (string, optional): Maximum memory
- `environment_variables` (map, optional): Environment variables
- `volume_mounts` (array, optional): Mounted volumes
- `lifecycle_status` (enum: Waiting, Running, Terminated, mandatory): Container state

**Pod Entity**:
- `name` (string, mandatory): Pod name
- `namespace` (string, mandatory): Namespace
- `labels` (map[string]string, optional): Labels
- `annotations` (map[string]string, optional): Annotations
- `node_name` (string, optional): Scheduled node
- `pod_ip` (string, optional): Pod IP address
- `host_ip` (string, optional): Host node IP
- `restart_policy` (enum: Always, OnFailure, Never, optional): Restart policy
- `lifecycle_status` (enum: Pending, Running, Succeeded, Failed, Unknown, mandatory): Pod phase
- `start_time` (timestamp, optional): Pod start time

**Deployment Entity**:
- `name` (string, mandatory): Deployment name
- `namespace` (string, mandatory): Namespace
- `replica_count` (integer, optional, default: 1): Desired replicas
- `available_replicas` (integer, optional): Available replicas
- `ready_replicas` (integer, optional): Ready replicas
- `strategy_type` (enum: RollingUpdate, Recreate, optional): Deployment strategy
- `max_unavailable` (int/string, optional): Max unavailable during update
- `max_surge` (int/string, optional): Max surge during update
- `revision_history_limit` (integer, optional): Retained old versions

**Service Entity (Kubernetes/OpenShift)**:
- `name` (string, mandatory): Service name
- `namespace` (string, mandatory): Namespace
- `service_type` (enum: ClusterIP, NodePort, LoadBalancer, ExternalName, mandatory): Service type
- `cluster_ip` (string, optional): Internal cluster IP
- `external_ips` (array, optional): External IPs
- `ports` (array, mandatory): Service ports
- `session_affinity` (enum: None, ClientIP, optional): Session affinity
- `load_balancer_ip` (string, optional): Load balancer IP

**Route Entity (OpenShift)**:
- `name` (string, mandatory): Route name
- `namespace` (string, mandatory): Namespace
- `external_hostname` (string, optional): External hostname
- `route_path` (string, optional): URL path prefix
- `target_service` (string, mandatory): Target service name
- `target_port` (string, mandatory): Target service port
- `tls_termination` (enum: edge, passthrough, reencrypt, none, optional): TLS termination type
- `tls_certificate` (string, optional): TLS certificate reference
- `insecure_policy` (enum: None, Allow, Redirect, optional): HTTP behavior
- `wildcard_policy` (enum: None, Subdomain, optional): Wildcard support

**Namespace/Project Entity**:
- `name` (string, mandatory): Namespace name
- `labels` (map[string]string, optional): Labels
- `display_name` (string, optional): Display name (OpenShift)
- `description` (string, optional): Description (OpenShift)
- `requester` (string, optional): Creator (OpenShift)
- `lifecycle_status` (enum: Active, Terminating, mandatory): Namespace phase

**Cluster Entity**:
- `name` (string, mandatory): Cluster name
- `orchestration_platform` (enum: kubernetes, openshift, docker_swarm, ecs, aci, mandatory): Platform type
- `version` (string, mandatory): Platform version
- `api_endpoint` (string, mandatory): API server endpoint
- `total_nodes` (integer, optional): Total cluster nodes
- `total_capacity.cpu` (string, optional): Total CPU capacity
- `total_capacity.memory` (string, optional): Total memory capacity

**IngressController Entity**:
- `name` (string, mandatory): Ingress controller name
- `namespace` (string, mandatory): Namespace
- `ingress_class` (string, optional): Ingress class name
- `default_backend` (string, optional): Default backend service
- `load_balancer_address` (string, optional): Load balancer address

**ContainerImage Entity**:
- `name` (string, mandatory): Image name
- `registry` (string, optional): Container registry
- `repository` (string, mandatory): Image repository
- `tag` (string, optional): Image tag
- `digest` (string, optional): Image digest (SHA256)
- `size` (integer, optional): Image size in bytes
- `created_at` (timestamp, optional): Image creation time

---

## Part 4: Relationship Types

### Kubernetes/OpenShift Relationships

**Orchestration Relationships**:
- `part_of`: Pod → Deployment/StatefulSet/DaemonSet (pod is managed by controller)
- `exposes`: Service → Pod (service exposes pods)
- `routes_to`: Route/Ingress → Service (external access routes to service)
- `runs_in`: Pod → Namespace (pod runs in namespace)
- `scheduled_on`: Pod → Node (pod scheduled on node)
- `uses_image`: Container → ContainerImage (container uses image)
- `mounts`: Container → PersistentVolumeClaim (container mounts storage)
- `bound_to`: PersistentVolumeClaim → PersistentVolume (PVC bound to PV)

**Cross-Layer Relationships**:
- `packages`: Container → Application (Layer 3 → Layer 2)
- `deployed_as`: Application → Pod (Layer 2 → Layer 3)
- `runs_on`: Pod → Node (Layer 3 → Layer 4)
- `hosted_on`: Node → PhysicalServer/VirtualMachine (Layer 4)
- `provisioned_from`: PersistentVolume → StorageArray/CloudStorage (Layer 3 → Layer 4)

---

## Part 5: Framework Mapping to Ontology

### Entity Type Mapping

| Kubernetes/OpenShift Resource | Ontology Entity Type | Ontology Layer |
|-------------------------------|----------------------|----------------|
| Pod | Pod | Layer 3 |
| Deployment | Deployment | Layer 3 |
| StatefulSet | Deployment (stateful) | Layer 3 |
| DaemonSet | Deployment (daemon) | Layer 3 |
| Service | Service | Layer 3 |
| Route (OpenShift) | Route | Layer 3 |
| Ingress | IngressController | Layer 3 |
| Namespace | Namespace | Layer 3 |
| Project (OpenShift) | Namespace | Layer 3 |
| Container | Container | Layer 3 |
| ContainerImage | ContainerImage | Layer 3 |
| ImageStream (OpenShift) | ContainerImage | Layer 3 |
| PersistentVolume | StorageVolume | Layer 4 |
| PersistentVolumeClaim | Storage claim | Layer 3 |
| Node | VirtualMachine/PhysicalServer | Layer 4 |
| ConfigMap | Configuration | Layer 3 |
| Secret | Certificate/Credentials | Layer 6 |
| Cluster | Cluster | Layer 3 |

---

## Conclusion

This analysis of Kubernetes and OpenShift APIs has identified comprehensive attributes and relationships for the Container and Orchestration layer (Layer 3) of the ontology:

**Kubernetes Contributions**:
- Core orchestration entities (Pod, Deployment, Service, Namespace)
- Resource management attributes (CPU, memory limits and requests)
- Networking attributes (service types, ports, IPs)
- Storage abstractions (PersistentVolume, PersistentVolumeClaim)
- Lifecycle states and conditions
- Label-based organization and selection

**OpenShift Contributions**:
- Enhanced external access (Route with TLS termination types)
- Deployment automation (DeploymentConfig with triggers)
- Image management (ImageStream)
- Build pipelines (BuildConfig)
- Enhanced namespace metadata (Project)

These APIs provide the foundation for modeling containerized applications and their orchestration, enabling the ontology to represent modern cloud-native architectures alongside legacy infrastructure.

---

**Analysis Complete**: 2025-11-09
**Next Steps**: Integrate these attributes into the ontology design document and update Layer 3 entity type specifications.
