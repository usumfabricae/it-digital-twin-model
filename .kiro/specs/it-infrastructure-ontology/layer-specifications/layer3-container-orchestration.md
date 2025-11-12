# Layer 3: Container and Orchestration - Complete Specification

## Overview

This document provides the complete formal specification for Layer 3 (Container and Orchestration) of the IT Infrastructure and Application Dependency Ontology. The Container and Orchestration layer represents containerization technologies and orchestration platforms that package and manage applications.

**Layer Purpose**: Represents containerization and orchestration technologies that package and manage applications.

**Layer Scope**: All container-related resources including containers, pods, orchestration controllers, services, and routing mechanisms. This layer is optional in the decomposition chain - legacy applications bypass this layer entirely.

**Framework Sources**: 
- Kubernetes API (v1.28+)
- OpenShift API (v4.14+)
- Docker Swarm API
- CIM Virtualization schema (CIM_Container)

**Key Characteristics**:
- Optional layer: Not all applications use containers
- Modern cloud-native applications traverse this layer
- Legacy applications skip directly from Application Layer to Physical Infrastructure
- Provides abstraction between application logic and infrastructure

---

## Entity Type Specifications

### 1. Container

**Definition**: A containerized application instance that packages application code with its dependencies.

**OWL Class Definition**:
```turtle
:Container
  rdf:type owl:Class ;
  rdfs:subClassOf :ContainerLayer ;
  rdfs:label "Container" ;
  rdfs:comment "A containerized application instance" ;
  skos:definition "A container is a lightweight, standalone executable package that includes application code and dependencies" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | Kubernetes | Container name |
| image_name | xsd:string | 1..1 | mandatory | Kubernetes | Container image reference (e.g., "nginx:1.21") |
| image_pull_policy | xsd:string | 0..1 | enum | Kubernetes | Image pull policy: Always, IfNotPresent, Never |
| ports | xsd:string | 0..* | optional | Kubernetes | Exposed ports (JSON array format) |
| resources_requests_cpu | xsd:string | 0..1 | optional | Kubernetes | Minimum CPU (e.g., "100m", "0.5") |
| resources_requests_memory | xsd:string | 0..1 | optional | Kubernetes | Minimum memory (e.g., "128Mi", "1Gi") |
| resources_limits_cpu | xsd:string | 0..1 | optional | Kubernetes | Maximum CPU |
| resources_limits_memory | xsd:string | 0..1 | optional | Kubernetes | Maximum memory |
| environment_variables | xsd:string | 0..1 | optional | Kubernetes | Environment variables (JSON format) |
| volume_mounts | xsd:string | 0..* | optional | Kubernetes | Mounted volumes (JSON array format) |
| lifecycle_status | xsd:string | 1..1 | enum | Kubernetes | Current state: Waiting, Running, Terminated |
| restart_count | xsd:integer | 0..1 | optional | Kubernetes | Number of container restarts |

**Enumeration Values**:
- **image_pull_policy**: `Always`, `IfNotPresent`, `Never`
- **lifecycle_status**: `Waiting`, `Running`, `Terminated`, `Unknown`

**SHACL Validation Shape**:
```turtle
:ContainerShape
  a sh:NodeShape ;
  sh:targetClass :Container ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
  ] ;
  sh:property [
    sh:path :image_name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:pattern "^[a-z0-9]+(\\.[a-z0-9]+)*(/[a-z0-9._-]+)*(:[a-z0-9._-]+)?(@sha256:[a-f0-9]{64})?$" ;
  ] ;
  sh:property [
    sh:path :image_pull_policy ;
    sh:maxCount 1 ;
    sh:in ( "Always" "IfNotPresent" "Never" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "Waiting" "Running" "Terminated" "Unknown" ) ;
  ] .
```

---

### 2. Pod

**Definition**: A Kubernetes pod representing one or more containers that share storage and network resources.

**OWL Class Definition**:
```turtle
:Pod
  rdf:type owl:Class ;
  rdfs:subClassOf :ContainerLayer ;
  rdfs:label "Pod" ;
  rdfs:comment "A Kubernetes pod" ;
  skos:definition "A pod is the smallest deployable unit in Kubernetes, containing one or more containers" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | Kubernetes | Pod name |
| namespace | xsd:string | 1..1 | mandatory | Kubernetes | Namespace containing the pod |
| labels | xsd:string | 0..1 | optional | Kubernetes | Key-value labels (JSON format) |
| annotations | xsd:string | 0..1 | optional | Kubernetes | Annotations (JSON format) |
| node_name | xsd:string | 0..1 | optional | Kubernetes | Node where pod is scheduled |
| pod_ip | xsd:string | 0..1 | optional | Kubernetes | IP address allocated to pod |
| host_ip | xsd:string | 0..1 | optional | Kubernetes | IP address of host node |
| restart_policy | xsd:string | 0..1 | enum | Kubernetes | Container restart policy: Always, OnFailure, Never |
| lifecycle_status | xsd:string | 1..1 | enum | Kubernetes | Pod phase: Pending, Running, Succeeded, Failed, Unknown |
| start_time | xsd:dateTime | 0..1 | optional | Kubernetes | Pod start timestamp |
| qos_class | xsd:string | 0..1 | enum | Kubernetes | Quality of Service class: Guaranteed, Burstable, BestEffort |

**Enumeration Values**:
- **restart_policy**: `Always`, `OnFailure`, `Never`
- **lifecycle_status**: `Pending`, `Running`, `Succeeded`, `Failed`, `Unknown`
- **qos_class**: `Guaranteed`, `Burstable`, `BestEffort`

**SHACL Validation Shape**:
```turtle
:PodShape
  a sh:NodeShape ;
  sh:targetClass :Pod ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :namespace ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :restart_policy ;
    sh:maxCount 1 ;
    sh:in ( "Always" "OnFailure" "Never" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "Pending" "Running" "Succeeded" "Failed" "Unknown" ) ;
  ] ;
  sh:property [
    sh:path :pod_ip ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:pattern "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$" ;
  ] .
```

---

### 3. ContainerImage

**Definition**: A container image template that contains application code and dependencies.

**OWL Class Definition**:
```turtle
:ContainerImage
  rdf:type owl:Class ;
  rdfs:subClassOf :ContainerLayer ;
  rdfs:label "Container Image" ;
  rdfs:comment "A container image template" ;
  skos:definition "A container image is an immutable template containing application code, runtime, and dependencies" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | Kubernetes | Image name |
| registry | xsd:string | 0..1 | optional | Kubernetes | Container registry (e.g., "docker.io", "quay.io") |
| repository | xsd:string | 1..1 | mandatory | Kubernetes | Image repository (e.g., "library/nginx") |
| tag | xsd:string | 0..1 | optional | Kubernetes | Image tag (e.g., "1.21", "latest") |
| digest | xsd:string | 0..1 | optional | Kubernetes | Image digest (SHA256 hash) |
| size_bytes | xsd:integer | 0..1 | optional | Docker | Image size in bytes |
| created_at | xsd:dateTime | 0..1 | optional | Docker | Image creation timestamp |
| architecture | xsd:string | 0..1 | enum | Docker | CPU architecture: amd64, arm64, arm, ppc64le, s390x |
| os | xsd:string | 0..1 | enum | Docker | Operating system: linux, windows |

**Enumeration Values**:
- **architecture**: `amd64`, `arm64`, `arm`, `ppc64le`, `s390x`, `386`
- **os**: `linux`, `windows`

**SHACL Validation Shape**:
```turtle
:ContainerImageShape
  a sh:NodeShape ;
  sh:targetClass :ContainerImage ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :repository ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :digest ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:pattern "^sha256:[a-f0-9]{64}$" ;
  ] .
```

---

### 4. Cluster

**Definition**: An orchestration cluster (Kubernetes, OpenShift, Docker Swarm, etc.).

**OWL Class Definition**:
```turtle
:Cluster
  rdf:type owl:Class ;
  rdfs:subClassOf :ContainerLayer ;
  rdfs:label "Cluster" ;
  rdfs:comment "An orchestration cluster" ;
  skos:definition "A cluster is a set of nodes that run containerized applications managed by an orchestration platform" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | Kubernetes | Cluster name |
| orchestration_platform | xsd:string | 1..1 | enum | Kubernetes | Platform: kubernetes, openshift, docker_swarm, ecs, aci, nomad |
| version | xsd:string | 1..1 | mandatory | Kubernetes | Platform version (e.g., "1.28.3") |
| api_endpoint | xsd:anyURI | 1..1 | mandatory | Kubernetes | API server endpoint URL |
| region | xsd:string | 0..1 | optional | Cloud APIs | Cloud region or datacenter location |
| total_nodes | xsd:integer | 0..1 | optional | Kubernetes | Total number of nodes in cluster |
| total_capacity_cpu | xsd:string | 0..1 | optional | Kubernetes | Total CPU capacity (e.g., "64 cores") |
| total_capacity_memory | xsd:string | 0..1 | optional | Kubernetes | Total memory capacity (e.g., "256Gi") |
| lifecycle_status | xsd:string | 1..1 | enum | Kubernetes | Current state: active, degraded, failed, maintenance |

**Enumeration Values**:
- **orchestration_platform**: `kubernetes`, `openshift`, `docker_swarm`, `ecs`, `aci`, `nomad`, `rancher`
- **lifecycle_status**: `active`, `degraded`, `failed`, `maintenance`, `provisioning`

**SHACL Validation Shape**:
```turtle
:ClusterShape
  a sh:NodeShape ;
  sh:targetClass :Cluster ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :orchestration_platform ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "kubernetes" "openshift" "docker_swarm" "ecs" "aci" "nomad" "rancher" ) ;
  ] ;
  sh:property [
    sh:path :version ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :api_endpoint ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:anyURI ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "degraded" "failed" "maintenance" "provisioning" ) ;
  ] .
```

---

### 5. Namespace

**Definition**: A logical isolation boundary within a cluster for organizing resources.

**OWL Class Definition**:
```turtle
:Namespace
  rdf:type owl:Class ;
  rdfs:subClassOf :ContainerLayer ;
  rdfs:label "Namespace" ;
  rdfs:comment "A logical isolation boundary within a cluster" ;
  skos:definition "A namespace provides resource isolation, access control, and quota management within a cluster" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | Kubernetes | Namespace name |
| display_name | xsd:string | 0..1 | optional | OpenShift | Human-readable display name |
| description | xsd:string | 0..1 | optional | OpenShift | Namespace description |
| labels | xsd:string | 0..1 | optional | Kubernetes | Key-value labels (JSON format) |
| annotations | xsd:string | 0..1 | optional | Kubernetes | Annotations (JSON format) |
| resource_quota_cpu | xsd:string | 0..1 | optional | Kubernetes | CPU quota (e.g., "10 cores") |
| resource_quota_memory | xsd:string | 0..1 | optional | Kubernetes | Memory quota (e.g., "20Gi") |
| lifecycle_status | xsd:string | 1..1 | enum | Kubernetes | Current state: Active, Terminating |

**Enumeration Values**:
- **lifecycle_status**: `Active`, `Terminating`

**SHACL Validation Shape**:
```turtle
:NamespaceShape
  a sh:NodeShape ;
  sh:targetClass :Namespace ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:pattern "^[a-z0-9]([-a-z0-9]*[a-z0-9])?$" ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "Active" "Terminating" ) ;
  ] .
```

---

### 6. Deployment

**Definition**: A deployment configuration that manages pod lifecycle and scaling.

**OWL Class Definition**:
```turtle
:Deployment
  rdf:type owl:Class ;
  rdfs:subClassOf :ContainerLayer ;
  rdfs:label "Deployment" ;
  rdfs:comment "A deployment configuration" ;
  skos:definition "A deployment provides declarative updates for pods and manages their lifecycle" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | Kubernetes | Deployment name |
| namespace | xsd:string | 1..1 | mandatory | Kubernetes | Namespace containing the deployment |
| replica_count | xsd:integer | 0..1 | optional | Kubernetes | Desired number of pod replicas (default: 1) |
| available_replicas | xsd:integer | 0..1 | optional | Kubernetes | Number of available replicas |
| ready_replicas | xsd:integer | 0..1 | optional | Kubernetes | Number of ready replicas |
| strategy_type | xsd:string | 0..1 | enum | Kubernetes | Deployment strategy: RollingUpdate, Recreate |
| max_unavailable | xsd:string | 0..1 | optional | Kubernetes | Max unavailable pods during update (int or percentage) |
| max_surge | xsd:string | 0..1 | optional | Kubernetes | Max surge pods during update (int or percentage) |
| revision_history_limit | xsd:integer | 0..1 | optional | Kubernetes | Number of old ReplicaSets to retain |
| min_ready_seconds | xsd:integer | 0..1 | optional | Kubernetes | Minimum ready time before considering pod available |
| lifecycle_status | xsd:string | 1..1 | enum | Kubernetes | Current state: progressing, available, failed |

**Enumeration Values**:
- **strategy_type**: `RollingUpdate`, `Recreate`
- **lifecycle_status**: `progressing`, `available`, `failed`, `paused`

**SHACL Validation Shape**:
```turtle
:DeploymentShape
  a sh:NodeShape ;
  sh:targetClass :Deployment ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :namespace ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :replica_count ;
    sh:maxCount 1 ;
    sh:datatype xsd:integer ;
    sh:minInclusive 0 ;
  ] ;
  sh:property [
    sh:path :strategy_type ;
    sh:maxCount 1 ;
    sh:in ( "RollingUpdate" "Recreate" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "progressing" "available" "failed" "paused" ) ;
  ] .
```

---

### 7. Service

**Definition**: A Kubernetes/OpenShift service that exposes pods as a network service.

**OWL Class Definition**:
```turtle
:KubernetesService
  rdf:type owl:Class ;
  rdfs:subClassOf :ContainerLayer ;
  rdfs:label "Kubernetes Service" ;
  rdfs:comment "A Kubernetes/OpenShift service" ;
  skos:definition "A service provides stable networking and load balancing for a set of pods" .
```

**Note**: This entity is named `KubernetesService` to distinguish it from the `Service` entity in Layer 2 (Application Layer).

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | Kubernetes | Service name |
| namespace | xsd:string | 1..1 | mandatory | Kubernetes | Namespace containing the service |
| service_type | xsd:string | 1..1 | enum | Kubernetes | Service type: ClusterIP, NodePort, LoadBalancer, ExternalName |
| cluster_ip | xsd:string | 0..1 | optional | Kubernetes | Internal cluster IP address |
| external_ips | xsd:string | 0..* | optional | Kubernetes | External IP addresses (JSON array) |
| ports | xsd:string | 1..* | mandatory | Kubernetes | Service ports (JSON array format) |
| session_affinity | xsd:string | 0..1 | enum | Kubernetes | Session affinity: None, ClientIP |
| load_balancer_ip | xsd:string | 0..1 | optional | Kubernetes | Load balancer IP address |
| selector | xsd:string | 0..1 | optional | Kubernetes | Pod selector labels (JSON format) |

**Enumeration Values**:
- **service_type**: `ClusterIP`, `NodePort`, `LoadBalancer`, `ExternalName`
- **session_affinity**: `None`, `ClientIP`

**SHACL Validation Shape**:
```turtle
:KubernetesServiceShape
  a sh:NodeShape ;
  sh:targetClass :KubernetesService ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :namespace ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :service_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "ClusterIP" "NodePort" "LoadBalancer" "ExternalName" ) ;
  ] ;
  sh:property [
    sh:path :ports ;
    sh:minCount 1 ;
  ] .
```

---

### 8. Route

**Definition**: An OpenShift route that exposes a service at an external hostname.

**OWL Class Definition**:
```turtle
:Route
  rdf:type owl:Class ;
  rdfs:subClassOf :ContainerLayer ;
  rdfs:label "Route" ;
  rdfs:comment "An OpenShift route" ;
  skos:definition "A route exposes a service at an external hostname for external access" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | OpenShift | Route name |
| namespace | xsd:string | 1..1 | mandatory | OpenShift | Namespace containing the route |
| external_hostname | xsd:string | 0..1 | optional | OpenShift | External hostname (auto-generated if not specified) |
| route_path | xsd:string | 0..1 | optional | OpenShift | URL path prefix (e.g., "/api") |
| target_service | xsd:string | 1..1 | mandatory | OpenShift | Target service name |
| target_port | xsd:string | 1..1 | mandatory | OpenShift | Target service port |
| tls_termination | xsd:string | 0..1 | enum | OpenShift | TLS termination: edge, passthrough, reencrypt, none |
| tls_certificate | xsd:string | 0..1 | optional | OpenShift | TLS certificate reference |
| tls_key | xsd:string | 0..1 | optional | OpenShift | TLS private key reference |
| tls_ca_certificate | xsd:string | 0..1 | optional | OpenShift | CA certificate reference |
| insecure_policy | xsd:string | 0..1 | enum | OpenShift | HTTP behavior: None, Allow, Redirect |
| wildcard_policy | xsd:string | 0..1 | enum | OpenShift | Wildcard support: None, Subdomain |

**Enumeration Values**:
- **tls_termination**: `edge`, `passthrough`, `reencrypt`, `none`
- **insecure_policy**: `None`, `Allow`, `Redirect`
- **wildcard_policy**: `None`, `Subdomain`

**SHACL Validation Shape**:
```turtle
:RouteShape
  a sh:NodeShape ;
  sh:targetClass :Route ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :namespace ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :target_service ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :target_port ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :tls_termination ;
    sh:maxCount 1 ;
    sh:in ( "edge" "passthrough" "reencrypt" "none" ) ;
  ] .
```

---

### 9. IngressController

**Definition**: A controller that manages external HTTP/HTTPS access to services.

**OWL Class Definition**:
```turtle
:IngressController
  rdf:type owl:Class ;
  rdfs:subClassOf :ContainerLayer ;
  rdfs:label "Ingress Controller" ;
  rdfs:comment "A controller for managing external access" ;
  skos:definition "An ingress controller manages external HTTP/HTTPS access to services in a cluster" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | Kubernetes | Ingress controller name |
| namespace | xsd:string | 1..1 | mandatory | Kubernetes | Namespace containing the ingress |
| ingress_class | xsd:string | 0..1 | optional | Kubernetes | Ingress class name (e.g., "nginx", "traefik") |
| default_backend | xsd:string | 0..1 | optional | Kubernetes | Default backend service |
| load_balancer_address | xsd:string | 0..1 | optional | Kubernetes | Load balancer address or hostname |
| tls_enabled | xsd:boolean | 0..1 | optional | Kubernetes | Whether TLS is configured |
| rules | xsd:string | 0..* | optional | Kubernetes | Ingress routing rules (JSON array format) |

**SHACL Validation Shape**:
```turtle
:IngressControllerShape
  a sh:NodeShape ;
  sh:targetClass :IngressController ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :namespace ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] .
```

---

## Container Layer Relationships

### Intra-Layer Relationships (within Container Layer)

#### 1. contains

**Definition**: A pod contains one or more containers.

**OWL Property Definition**:
```turtle
:contains
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Pod ;
  rdfs:range :Container ;
  rdfs:label "contains" ;
  rdfs:comment "A pod contains containers" .
```

**Cardinality**: 1 Pod to many Containers (1..*)

**Inverse Property**: `part_of`

**Semantic Rules**:
- A pod MUST contain at least one container
- All containers in a pod share the same network namespace
- All containers in a pod share the same storage volumes

---

#### 2. part_of

**Definition**: A pod is part of a deployment/statefulset/daemonset.

**OWL Property Definition**:
```turtle
:part_of
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Pod ;
  rdfs:range :Deployment ;
  rdfs:label "part of" ;
  rdfs:comment "A pod is part of a deployment" .
```

**Cardinality**: Many Pods to 1 Deployment (*..1)

**Inverse Property**: `manages`

**Semantic Rules**:
- Pods are typically managed by a controller (Deployment, StatefulSet, DaemonSet)
- Standalone pods (not managed by a controller) are allowed but not recommended

---

#### 3. exposes

**Definition**: A service exposes pods for network access.

**OWL Property Definition**:
```turtle
:exposes
  rdf:type owl:ObjectProperty ;
  rdfs:domain :KubernetesService ;
  rdfs:range :Pod ;
  rdfs:label "exposes" ;
  rdfs:comment "A service exposes pods" .
```

**Cardinality**: 1 Service to many Pods (1..*)

**Inverse Property**: `exposed_by`

**Semantic Rules**:
- Services use label selectors to identify pods
- Services provide stable networking for dynamic pod sets
- Services load balance traffic across pods

---

#### 4. routes_to

**Definition**: A route or ingress routes traffic to a service.

**OWL Property Definition**:
```turtle
:routes_to
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Route :IngressController ) ] ;
  rdfs:range :KubernetesService ;
  rdfs:label "routes to" ;
  rdfs:comment "A route routes traffic to a service" .
```

**Cardinality**: Many Routes to 1 Service (*..1)

**Inverse Property**: `receives_traffic_from`

**Semantic Rules**:
- Routes and ingresses provide external access to services
- Multiple routes can point to the same service
- Routes handle TLS termination and path-based routing

---

#### 5. runs_in

**Definition**: A pod runs in a namespace.

**OWL Property Definition**:
```turtle
:runs_in
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Pod ;
  rdfs:range :Namespace ;
  rdfs:label "runs in" ;
  rdfs:comment "A pod runs in a namespace" .
```

**Cardinality**: Many Pods to 1 Namespace (*..1)

**Inverse Property**: `contains_pod`

**Semantic Rules**:
- Every pod MUST belong to exactly one namespace
- Namespaces provide resource isolation and access control

---

#### 6. uses_image

**Definition**: A container uses a container image.

**OWL Property Definition**:
```turtle
:uses_image
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Container ;
  rdfs:range :ContainerImage ;
  rdfs:label "uses image" ;
  rdfs:comment "A container uses a container image" .
```

**Cardinality**: Many Containers to 1 ContainerImage (*..1)

**Inverse Property**: `used_by`

**Semantic Rules**:
- Every container MUST reference exactly one image
- Multiple containers can use the same image
- Image updates trigger container recreation

---

#### 7. managed_by

**Definition**: Resources are managed by a cluster.

**OWL Property Definition**:
```turtle
:managed_by
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Pod :Deployment :KubernetesService :Namespace ) ] ;
  rdfs:range :Cluster ;
  rdfs:label "managed by" ;
  rdfs:comment "Resources are managed by a cluster" .
```

**Cardinality**: Many Resources to 1 Cluster (*..1)

**Inverse Property**: `manages`

---

### Cross-Layer Relationships

#### 8. packages (Layer 2 → Layer 3)

**Definition**: A container packages an application.

**OWL Property Definition**:
```turtle
:packages
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Container ;
  rdfs:range :Application ;
  rdfs:label "packages" ;
  rdfs:comment "A container packages an application" .
```

**Cardinality**: Many Containers to 1 Application (*..1)

**Inverse Property**: `packaged_in`

**Semantic Rules**:
- Containers encapsulate application code and dependencies
- One application can be packaged in multiple container instances
- This relationship links Layer 3 to Layer 2

---

#### 9. deployed_as (Layer 2 → Layer 3)

**Definition**: An application is deployed as pods/containers.

**OWL Property Definition**:
```turtle
:deployed_as
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Application ;
  rdfs:range [ owl:unionOf ( :Pod :Container ) ] ;
  rdfs:label "deployed as" ;
  rdfs:comment "An application is deployed as pods or containers" .
```

**Cardinality**: 1 Application to many Pods/Containers (1..*)

**Inverse Property**: `deploys`

**Semantic Rules**:
- Modern applications are deployed as containerized workloads
- Legacy applications skip this layer entirely
- This relationship enables decomposition from Application to Container layer

---

#### 10. runs_on (Layer 3 → Layer 4)

**Definition**: A pod runs on a physical or virtual machine.

**OWL Property Definition**:
```turtle
:runs_on
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Pod ;
  rdfs:range [ owl:unionOf ( :VirtualMachine :PhysicalServer :CloudInstance ) ] ;
  rdfs:label "runs on" ;
  rdfs:comment "A pod runs on infrastructure" .
```

**Cardinality**: Many Pods to 1 Infrastructure (*..1)

**Inverse Property**: `hosts`

**Semantic Rules**:
- Pods are scheduled on cluster nodes (VMs or physical servers)
- Multiple pods can run on the same node
- This relationship links Layer 3 to Layer 4

---

#### 11. uses (Layer 3 → Layer 4)

**Definition**: A container uses persistent storage.

**OWL Property Definition**:
```turtle
:uses
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Container ;
  rdfs:range [ owl:unionOf ( :StorageVolume :PersistentVolume ) ] ;
  rdfs:label "uses" ;
  rdfs:comment "A container uses persistent storage" .
```

**Cardinality**: Many Containers to many Storage (*..*)

**Inverse Property**: `used_by`

**Semantic Rules**:
- Containers can mount persistent volumes for data storage
- PersistentVolumeClaims bind pods to storage
- This relationship links Layer 3 to Layer 4 storage

---

## Validation Rules and Constraints

### Layer Assignment Rules

1. All Container Layer entities MUST belong to Layer 3
2. Container Layer entities MUST NOT have attributes from other layers
3. Cross-layer relationships MUST connect to Layer 2 (Application) or Layer 4 (Physical Infrastructure)

### Attribute Constraints

1. **Mandatory Attributes**: name, namespace (where applicable), lifecycle_status
2. **Enumeration Validation**: All enum attributes MUST use defined values
3. **Resource Limits**: CPU and memory values MUST follow Kubernetes resource syntax
4. **IP Address Validation**: IP addresses MUST match IPv4 or IPv6 patterns
5. **Image Reference Validation**: Container images MUST follow registry/repository:tag format

### Relationship Constraints

1. **Pod-Container**: A pod MUST contain at least one container
2. **Service-Pod**: A service MUST expose at least one pod
3. **Namespace Isolation**: Pods and services MUST belong to the same namespace for exposure
4. **Deployment Management**: Pods managed by deployments MUST have matching labels
5. **Route-Service**: Routes MUST target existing services in the same namespace

### Lifecycle Constraints

1. **Pod Lifecycle**: Pods transition through Pending → Running → Succeeded/Failed
2. **Container Lifecycle**: Containers transition through Waiting → Running → Terminated
3. **Deployment Lifecycle**: Deployments transition through progressing → available
4. **Namespace Lifecycle**: Namespaces transition from Active → Terminating (one-way)

---

## Usage Patterns and Examples

### Pattern 1: Microservice Deployment

**Scenario**: Deploy a microservice application in Kubernetes

**Instance Data (Turtle)**:
```turtle
@prefix : <http://example.org/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Container Image
:order-service-image
  a :ContainerImage ;
  :name "order-service" ;
  :registry "docker.io" ;
  :repository "mycompany/order-service" ;
  :tag "v1.2.3" ;
  :digest "sha256:abc123..." ;
  :architecture "amd64" ;
  :os "linux" .

# Container
:order-service-container
  a :Container ;
  :name "order-service" ;
  :image_name "docker.io/mycompany/order-service:v1.2.3" ;
  :image_pull_policy "IfNotPresent" ;
  :resources_requests_cpu "100m" ;
  :resources_requests_memory "128Mi" ;
  :resources_limits_cpu "500m" ;
  :resources_limits_memory "512Mi" ;
  :lifecycle_status "Running" ;
  :uses_image :order-service-image .

# Pod
:order-service-pod-abc123
  a :Pod ;
  :name "order-service-pod-abc123" ;
  :namespace "production" ;
  :pod_ip "10.244.1.15" ;
  :host_ip "192.168.1.10" ;
  :restart_policy "Always" ;
  :lifecycle_status "Running" ;
  :start_time "2025-11-10T10:30:00Z"^^xsd:dateTime ;
  :contains :order-service-container ;
  :runs_in :production-namespace .

# Deployment
:order-service-deployment
  a :Deployment ;
  :name "order-service" ;
  :namespace "production" ;
  :replica_count 3 ;
  :available_replicas 3 ;
  :ready_replicas 3 ;
  :strategy_type "RollingUpdate" ;
  :max_unavailable "1" ;
  :max_surge "1" ;
  :lifecycle_status "available" ;
  :manages :order-service-pod-abc123 .

# Service
:order-service-svc
  a :KubernetesService ;
  :name "order-service" ;
  :namespace "production" ;
  :service_type "ClusterIP" ;
  :cluster_ip "10.96.5.20" ;
  :ports "[{\"port\":8080,\"targetPort\":8080,\"protocol\":\"TCP\"}]" ;
  :session_affinity "None" ;
  :exposes :order-service-pod-abc123 .

# Route (OpenShift)
:order-service-route
  a :Route ;
  :name "order-service" ;
  :namespace "production" ;
  :external_hostname "orders.example.com" ;
  :route_path "/api" ;
  :target_service "order-service" ;
  :target_port "8080" ;
  :tls_termination "edge" ;
  :insecure_policy "Redirect" ;
  :routes_to :order-service-svc .

# Namespace
:production-namespace
  a :Namespace ;
  :name "production" ;
  :display_name "Production Environment" ;
  :description "Production workloads" ;
  :resource_quota_cpu "50 cores" ;
  :resource_quota_memory "100Gi" ;
  :lifecycle_status "Active" .

# Cluster
:prod-cluster
  a :Cluster ;
  :name "prod-k8s-cluster" ;
  :orchestration_platform "kubernetes" ;
  :version "1.28.3" ;
  :api_endpoint "https://k8s-api.example.com:6443"^^xsd:anyURI ;
  :region "us-east-1" ;
  :total_nodes 10 ;
  :total_capacity_cpu "80 cores" ;
  :total_capacity_memory "320Gi" ;
  :lifecycle_status "active" ;
  :manages :production-namespace .

# Cross-layer relationship to Application (Layer 2)
:order-service-app
  a :Application ;
  :name "Order Service" ;
  :application_type "microservice" ;
  :deployment_model "containerized" ;
  :deployed_as :order-service-pod-abc123 .

:order-service-container
  :packages :order-service-app .
```

---

### Pattern 2: Stateful Application with Persistent Storage

**Scenario**: PostgreSQL database deployed in Kubernetes with persistent storage

**Instance Data (Turtle)**:
```turtle
# Container
:postgres-container
  a :Container ;
  :name "postgres" ;
  :image_name "postgres:15.3" ;
  :resources_requests_cpu "500m" ;
  :resources_requests_memory "1Gi" ;
  :resources_limits_cpu "2" ;
  :resources_limits_memory "4Gi" ;
  :volume_mounts "[{\"name\":\"postgres-data\",\"mountPath\":\"/var/lib/postgresql/data\"}]" ;
  :lifecycle_status "Running" .

# Pod
:postgres-pod-0
  a :Pod ;
  :name "postgres-0" ;
  :namespace "databases" ;
  :pod_ip "10.244.2.30" ;
  :restart_policy "Always" ;
  :lifecycle_status "Running" ;
  :contains :postgres-container .

# StatefulSet (modeled as Deployment)
:postgres-statefulset
  a :Deployment ;
  :name "postgres" ;
  :namespace "databases" ;
  :replica_count 1 ;
  :strategy_type "RollingUpdate" ;
  :lifecycle_status "available" ;
  :manages :postgres-pod-0 .

# Service (Headless)
:postgres-svc
  a :KubernetesService ;
  :name "postgres" ;
  :namespace "databases" ;
  :service_type "ClusterIP" ;
  :cluster_ip "None" ;
  :ports "[{\"port\":5432,\"targetPort\":5432}]" ;
  :exposes :postgres-pod-0 .

# Cross-layer relationship to Storage (Layer 4)
:postgres-pv
  a :PersistentVolume ;
  :name "postgres-pv-001" ;
  :capacity "50Gi" .

:postgres-container
  :uses :postgres-pv .
```

---

## Query Patterns

### Query 1: Find All Pods in a Namespace

**SPARQL**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?pod ?status ?ip
WHERE {
  ?pod a :Pod ;
       :namespace "production" ;
       :lifecycle_status ?status ;
       :pod_ip ?ip .
}
ORDER BY ?pod
```

**Cypher (Neo4j)**:
```cypher
MATCH (pod:Pod {namespace: 'production'})
RETURN pod.name AS pod, 
       pod.lifecycle_status AS status, 
       pod.pod_ip AS ip
ORDER BY pod.name
```

---

### Query 2: Trace Application to Infrastructure

**SPARQL**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?app ?container ?pod ?node
WHERE {
  ?app a :Application ;
       :name "Order Service" .
  ?container :packages ?app .
  ?pod :contains ?container .
  ?pod :runs_on ?node .
}
```

**Cypher (Neo4j)**:
```cypher
MATCH (app:Application {name: 'Order Service'})
      <-[:PACKAGES]-(container:Container)
      <-[:CONTAINS]-(pod:Pod)
      -[:RUNS_ON]->(node)
RETURN app.name AS application,
       container.name AS container,
       pod.name AS pod,
       node.name AS node
```

---

### Query 3: Find All Services Exposed by a Deployment

**SPARQL**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?service ?type ?cluster_ip
WHERE {
  ?deployment a :Deployment ;
              :name "order-service" .
  ?deployment :manages ?pod .
  ?service :exposes ?pod ;
           :service_type ?type ;
           :cluster_ip ?cluster_ip .
}
```

**Cypher (Neo4j)**:
```cypher
MATCH (deployment:Deployment {name: 'order-service'})
      -[:MANAGES]->(pod:Pod)
      <-[:EXPOSES]-(service:KubernetesService)
RETURN DISTINCT service.name AS service,
                service.service_type AS type,
                service.cluster_ip AS cluster_ip
```

---

### Query 4: Find External Routes for an Application

**SPARQL**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?route ?hostname ?path ?tls
WHERE {
  ?app a :Application ;
       :name "Order Service" .
  ?container :packages ?app .
  ?pod :contains ?container .
  ?service :exposes ?pod .
  ?route :routes_to ?service ;
         :external_hostname ?hostname ;
         :route_path ?path ;
         :tls_termination ?tls .
}
```

**Cypher (Neo4j)**:
```cypher
MATCH (app:Application {name: 'Order Service'})
      <-[:PACKAGES]-(container:Container)
      <-[:CONTAINS]-(pod:Pod)
      <-[:EXPOSES]-(service:KubernetesService)
      <-[:ROUTES_TO]-(route:Route)
RETURN route.external_hostname AS hostname,
       route.route_path AS path,
       route.tls_termination AS tls
```

---

### Query 5: Find All Containers Using a Specific Image

**SPARQL**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?container ?pod ?namespace
WHERE {
  ?image a :ContainerImage ;
         :repository "mycompany/order-service" ;
         :tag "v1.2.3" .
  ?container :uses_image ?image .
  ?pod :contains ?container ;
       :namespace ?namespace .
}
```

**Cypher (Neo4j)**:
```cypher
MATCH (image:ContainerImage {repository: 'mycompany/order-service', tag: 'v1.2.3'})
      <-[:USES_IMAGE]-(container:Container)
      <-[:CONTAINS]-(pod:Pod)
RETURN container.name AS container,
       pod.name AS pod,
       pod.namespace AS namespace
```

---

## Requirements Traceability

### Requirement 1.3: Layer Definition

**Satisfied by**:
- Layer 3 defined with clear scope and boundaries
- Entity types assigned exclusively to Layer 3
- Cross-layer relationships defined to Layer 2 and Layer 4

### Requirement 1.4: Cross-Layer Decomposition

**Satisfied by**:
- `deployed_as` relationship (Application → Pod)
- `packages` relationship (Container → Application)
- `runs_on` relationship (Pod → Infrastructure)

### Requirement 8.1, 8.2, 8.3, 8.5: Framework-Sourced Attributes

**Satisfied by**:
- All attributes sourced from Kubernetes API or OpenShift API
- Framework sources documented in attribute tables
- Data types and constraints specified

### Requirement 13.1: Container Entity Types

**Satisfied by**:
- Container, Pod, ContainerImage, Cluster, Namespace, Deployment, Service, Route, IngressController defined

### Requirement 13.2: Orchestration Platforms

**Satisfied by**:
- Kubernetes and OpenShift entity types defined
- Platform-specific attributes (e.g., Route for OpenShift)
- Cluster entity with orchestration_platform attribute

### Requirement 13.3: Container-Infrastructure Relationships

**Satisfied by**:
- `runs_on` relationship (Pod → Node)
- `uses` relationship (Container → Storage)

### Requirement 13.4: Orchestration Patterns

**Satisfied by**:
- `part_of` relationship (Pod → Deployment)
- `exposes` relationship (Service → Pod)
- `routes_to` relationship (Route → Service)

---

## Framework Mapping Summary

| Ontology Entity | Kubernetes Resource | OpenShift Resource | Framework Source |
|-----------------|---------------------|-------------------|------------------|
| Container | Container (in Pod spec) | Container | Kubernetes API |
| Pod | Pod | Pod | Kubernetes API |
| ContainerImage | Image | ImageStream | Kubernetes/OpenShift API |
| Cluster | Cluster | Cluster | Kubernetes API |
| Namespace | Namespace | Project | Kubernetes/OpenShift API |
| Deployment | Deployment/StatefulSet/DaemonSet | DeploymentConfig | Kubernetes/OpenShift API |
| KubernetesService | Service | Service | Kubernetes API |
| Route | Ingress | Route | OpenShift API |
| IngressController | Ingress | IngressController | Kubernetes API |

---

## Next Steps

1. ✅ Layer 3 entity types specified
2. ✅ Layer 3 relationships defined
3. ⏳ Integrate with Layer 2 (Application) cross-layer relationships
4. ⏳ Integrate with Layer 4 (Physical Infrastructure) cross-layer relationships
5. ⏳ Create formal OWL ontology definitions
6. ⏳ Validate with sample Kubernetes/OpenShift data

---

**Specification Complete**: 2025-11-10
**Version**: 1.0
**Status**: Complete - Ready for OWL implementation

