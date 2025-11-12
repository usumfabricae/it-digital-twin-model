# Layer 3: Container and Orchestration - Relationships Guide

## Overview

This document provides detailed semantics, usage patterns, and validation rules for all relationships in Layer 3 (Container and Orchestration). It complements the main Layer 3 specification by focusing specifically on relationship definitions and their proper usage.

**Purpose**: Define precise semantics for intra-layer and cross-layer relationships in the Container and Orchestration layer.

**Scope**: All relationship types connecting Container Layer entities to each other and to entities in other layers.

---

## Relationship Categories

### Intra-Layer Relationships
Relationships connecting entities within Layer 3:
1. `contains` - Pod contains Containers
2. `part_of` - Pod part of Deployment
3. `exposes` - Service exposes Pods
4. `routes_to` - Route/Ingress routes to Service
5. `runs_in` - Pod runs in Namespace
6. `uses_image` - Container uses ContainerImage
7. `managed_by` - Resources managed by Cluster

### Cross-Layer Relationships
Relationships connecting Layer 3 to other layers:
8. `packages` - Container packages Application (Layer 3 → Layer 2)
9. `deployed_as` - Application deployed as Pod (Layer 2 → Layer 3)
10. `runs_on` - Pod runs on Infrastructure (Layer 3 → Layer 4)
11. `uses` - Container uses Storage (Layer 3 → Layer 4)

---

## Intra-Layer Relationship Specifications

### 1. contains (Pod → Container)

**Definition**: A pod contains one or more containers that share network and storage resources.

**OWL Property Definition**:
```turtle
:contains
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Pod ;
  rdfs:range :Container ;
  rdfs:label "contains" ;
  rdfs:comment "A pod contains containers" ;
  owl:inverseOf :part_of_pod .
```

**Cardinality**: 1 Pod to many Containers (1..*)

**Mandatory**: Yes - A pod MUST contain at least one container

**Relationship Properties**:
- No additional properties required

**Semantic Rules**:
1. A pod MUST contain at least one container
2. All containers in a pod share the same network namespace (same IP address)
3. All containers in a pod share the same storage volumes
4. Containers in a pod are co-located and co-scheduled on the same node
5. Containers in a pod start and stop together

**Usage Example**:
```turtle
:order-service-pod
  a :Pod ;
  :name "order-service-pod-abc123" ;
  :contains :order-service-container ;
  :contains :sidecar-proxy-container .

:order-service-container
  a :Container ;
  :name "order-service" ;
  :image_name "mycompany/order-service:v1.0" .

:sidecar-proxy-container
  a :Container ;
  :name "envoy-proxy" ;
  :image_name "envoyproxy/envoy:v1.28" .
```

**Validation Rules**:
```turtle
:PodContainerValidation
  a sh:NodeShape ;
  sh:targetClass :Pod ;
  sh:property [
    sh:path :contains ;
    sh:minCount 1 ;
    sh:class :Container ;
  ] .
```

**Common Patterns**:
- **Single Container Pod**: Most common pattern, one application container per pod
- **Sidecar Pattern**: Main container + sidecar (logging, proxy, monitoring)
- **Init Container Pattern**: Init containers run before main containers

---

### 2. part_of (Pod → Deployment)

**Definition**: A pod is part of a deployment, statefulset, or daemonset controller.

**OWL Property Definition**:
```turtle
:part_of
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Pod ;
  rdfs:range :Deployment ;
  rdfs:label "part of" ;
  rdfs:comment "A pod is part of a deployment" ;
  owl:inverseOf :manages .
```

**Cardinality**: Many Pods to 1 Deployment (*..1)

**Mandatory**: No - Standalone pods are allowed but not recommended

**Relationship Properties**:
- `replica_index` (integer, optional): Index of pod in replica set (for StatefulSets)

**Semantic Rules**:
1. Pods managed by deployments have matching labels
2. Deployment controllers ensure desired replica count
3. Pods are recreated if they fail (based on restart policy)
4. Deployment updates trigger pod recreation
5. Standalone pods (not managed by a controller) are not automatically recreated

**Usage Example**:
```turtle
:order-service-deployment
  a :Deployment ;
  :name "order-service" ;
  :replica_count 3 ;
  :manages :order-service-pod-1 ;
  :manages :order-service-pod-2 ;
  :manages :order-service-pod-3 .

:order-service-pod-1
  a :Pod ;
  :name "order-service-pod-abc123" ;
  :part_of :order-service-deployment .
```

**Validation Rules**:
```turtle
:PodDeploymentValidation
  a sh:NodeShape ;
  sh:targetClass :Pod ;
  sh:property [
    sh:path :part_of ;
    sh:maxCount 1 ;
    sh:class :Deployment ;
  ] .
```

**Common Patterns**:
- **Deployment**: Stateless applications with rolling updates
- **StatefulSet**: Stateful applications with stable network identities
- **DaemonSet**: One pod per node (logging, monitoring agents)
- **Standalone Pod**: Direct pod creation (not recommended for production)

---

### 3. exposes (Service → Pod)

**Definition**: A service exposes pods for network access with load balancing.

**OWL Property Definition**:
```turtle
:exposes
  rdf:type owl:ObjectProperty ;
  rdfs:domain :KubernetesService ;
  rdfs:range :Pod ;
  rdfs:label "exposes" ;
  rdfs:comment "A service exposes pods" ;
  owl:inverseOf :exposed_by .
```

**Cardinality**: 1 Service to many Pods (1..*)

**Mandatory**: Yes - A service MUST expose at least one pod

**Relationship Properties**:
- `weight` (integer, optional): Traffic weight for load balancing
- `health_check_status` (enum: healthy, unhealthy, optional): Pod health status

**Semantic Rules**:
1. Services use label selectors to identify pods
2. Services provide stable networking (cluster IP) for dynamic pod sets
3. Services load balance traffic across healthy pods
4. Pods and services MUST be in the same namespace
5. Service endpoints are automatically updated as pods are created/destroyed

**Usage Example**:
```turtle
:order-service-svc
  a :KubernetesService ;
  :name "order-service" ;
  :namespace "production" ;
  :service_type "ClusterIP" ;
  :cluster_ip "10.96.5.20" ;
  :exposes :order-service-pod-1 ;
  :exposes :order-service-pod-2 ;
  :exposes :order-service-pod-3 .

:order-service-pod-1
  a :Pod ;
  :name "order-service-pod-abc123" ;
  :namespace "production" ;
  :exposed_by :order-service-svc .
```

**Validation Rules**:
```turtle
:ServicePodValidation
  a sh:NodeShape ;
  sh:targetClass :KubernetesService ;
  sh:property [
    sh:path :exposes ;
    sh:minCount 1 ;
    sh:class :Pod ;
  ] ;
  # Validate same namespace
  sh:sparql [
    sh:message "Service and pods must be in the same namespace" ;
    sh:select """
      PREFIX : <http://example.org/ontology#>
      SELECT $this
      WHERE {
        $this a :KubernetesService ;
              :namespace ?svc_ns ;
              :exposes ?pod .
        ?pod :namespace ?pod_ns .
        FILTER(?svc_ns != ?pod_ns)
      }
    """ ;
  ] .
```

**Common Patterns**:
- **ClusterIP**: Internal service accessible within cluster
- **NodePort**: Service exposed on each node's IP at a static port
- **LoadBalancer**: Cloud load balancer for external access
- **Headless Service**: Direct pod access without load balancing (StatefulSets)

---

### 4. routes_to (Route/Ingress → Service)

**Definition**: A route or ingress routes external traffic to a service.

**OWL Property Definition**:
```turtle
:routes_to
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Route :IngressController ) ] ;
  rdfs:range :KubernetesService ;
  rdfs:label "routes to" ;
  rdfs:comment "A route routes traffic to a service" ;
  owl:inverseOf :receives_traffic_from .
```

**Cardinality**: Many Routes to 1 Service (*..1)

**Mandatory**: Yes - A route MUST target a service

**Relationship Properties**:
- `path_prefix` (string, optional): URL path prefix for routing
- `traffic_weight` (integer, optional): Traffic percentage for A/B testing
- `tls_enabled` (boolean, optional): Whether TLS is configured

**Semantic Rules**:
1. Routes provide external access to internal services
2. Routes handle TLS termination and path-based routing
3. Multiple routes can point to the same service (different paths/hostnames)
4. Routes and services MUST be in the same namespace
5. Route hostnames MUST be unique within the cluster

**Usage Example**:
```turtle
:order-service-route
  a :Route ;
  :name "order-service" ;
  :namespace "production" ;
  :external_hostname "orders.example.com" ;
  :route_path "/api" ;
  :tls_termination "edge" ;
  :routes_to :order-service-svc .

:order-service-svc
  a :KubernetesService ;
  :name "order-service" ;
  :namespace "production" ;
  :receives_traffic_from :order-service-route .
```

**Validation Rules**:
```turtle
:RouteServiceValidation
  a sh:NodeShape ;
  sh:targetClass :Route ;
  sh:property [
    sh:path :routes_to ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:class :KubernetesService ;
  ] ;
  # Validate same namespace
  sh:sparql [
    sh:message "Route and service must be in the same namespace" ;
    sh:select """
      PREFIX : <http://example.org/ontology#>
      SELECT $this
      WHERE {
        $this a :Route ;
              :namespace ?route_ns ;
              :routes_to ?service .
        ?service :namespace ?svc_ns .
        FILTER(?route_ns != ?svc_ns)
      }
    """ ;
  ] .
```

**Common Patterns**:
- **Edge Termination**: TLS terminated at route, HTTP to backend
- **Passthrough Termination**: TLS passed through to backend service
- **Re-encrypt Termination**: TLS terminated and re-encrypted to backend
- **Path-based Routing**: Multiple routes with different paths to same service

---

### 5. runs_in (Pod → Namespace)

**Definition**: A pod runs in a namespace for resource isolation.

**OWL Property Definition**:
```turtle
:runs_in
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Pod ;
  rdfs:range :Namespace ;
  rdfs:label "runs in" ;
  rdfs:comment "A pod runs in a namespace" ;
  owl:inverseOf :contains_pod .
```

**Cardinality**: Many Pods to 1 Namespace (*..1)

**Mandatory**: Yes - Every pod MUST belong to exactly one namespace

**Relationship Properties**:
- No additional properties required

**Semantic Rules**:
1. Every pod MUST belong to exactly one namespace
2. Namespaces provide resource isolation and access control
3. Resource quotas apply at the namespace level
4. Network policies can isolate namespaces
5. RBAC permissions are scoped to namespaces

**Usage Example**:
```turtle
:production-namespace
  a :Namespace ;
  :name "production" ;
  :resource_quota_cpu "50 cores" ;
  :resource_quota_memory "100Gi" ;
  :contains_pod :order-service-pod .

:order-service-pod
  a :Pod ;
  :name "order-service-pod-abc123" ;
  :namespace "production" ;
  :runs_in :production-namespace .
```

**Validation Rules**:
```turtle
:PodNamespaceValidation
  a sh:NodeShape ;
  sh:targetClass :Pod ;
  sh:property [
    sh:path :runs_in ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:class :Namespace ;
  ] ;
  # Validate namespace attribute matches relationship
  sh:sparql [
    sh:message "Pod namespace attribute must match runs_in relationship" ;
    sh:select """
      PREFIX : <http://example.org/ontology#>
      SELECT $this
      WHERE {
        $this a :Pod ;
              :namespace ?ns_attr ;
              :runs_in ?ns_obj .
        ?ns_obj :name ?ns_name .
        FILTER(?ns_attr != ?ns_name)
      }
    """ ;
  ] .
```

**Common Patterns**:
- **Environment Isolation**: Separate namespaces for dev, staging, production
- **Team Isolation**: Separate namespaces per team or project
- **Application Isolation**: Separate namespaces per application
- **Multi-tenancy**: Separate namespaces per tenant

---

### 6. uses_image (Container → ContainerImage)

**Definition**: A container uses a container image as its template.

**OWL Property Definition**:
```turtle
:uses_image
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Container ;
  rdfs:range :ContainerImage ;
  rdfs:label "uses image" ;
  rdfs:comment "A container uses a container image" ;
  owl:inverseOf :used_by .
```

**Cardinality**: Many Containers to 1 ContainerImage (*..1)

**Mandatory**: Yes - Every container MUST reference exactly one image

**Relationship Properties**:
- `pull_timestamp` (dateTime, optional): When image was last pulled
- `image_pull_status` (enum: success, failed, pending, optional): Pull status

**Semantic Rules**:
1. Every container MUST reference exactly one image
2. Multiple containers can use the same image
3. Image updates trigger container recreation
4. Image pull policy determines when images are pulled
5. Image digests provide immutable references

**Usage Example**:
```turtle
:order-service-image
  a :ContainerImage ;
  :name "order-service" ;
  :repository "mycompany/order-service" ;
  :tag "v1.2.3" ;
  :digest "sha256:abc123..." ;
  :used_by :order-service-container-1 ;
  :used_by :order-service-container-2 .

:order-service-container-1
  a :Container ;
  :name "order-service" ;
  :image_name "mycompany/order-service:v1.2.3" ;
  :uses_image :order-service-image .
```

**Validation Rules**:
```turtle
:ContainerImageValidation
  a sh:NodeShape ;
  sh:targetClass :Container ;
  sh:property [
    sh:path :uses_image ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:class :ContainerImage ;
  ] .
```

**Common Patterns**:
- **Tag-based Reference**: Use image tags for versioning (e.g., "v1.2.3")
- **Digest-based Reference**: Use SHA256 digests for immutability
- **Latest Tag**: Use "latest" tag for development (not recommended for production)
- **Private Registry**: Pull images from private container registries

---

### 7. managed_by (Resources → Cluster)

**Definition**: Container resources are managed by a cluster.

**OWL Property Definition**:
```turtle
:managed_by
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Pod :Deployment :KubernetesService :Namespace ) ] ;
  rdfs:range :Cluster ;
  rdfs:label "managed by" ;
  rdfs:comment "Resources are managed by a cluster" ;
  owl:inverseOf :manages .
```

**Cardinality**: Many Resources to 1 Cluster (*..1)

**Mandatory**: Yes - All container resources MUST belong to a cluster

**Relationship Properties**:
- No additional properties required

**Semantic Rules**:
1. All container resources belong to exactly one cluster
2. Clusters provide the orchestration platform
3. Cluster API server manages resource lifecycle
4. Resources cannot be moved between clusters (must be recreated)

**Usage Example**:
```turtle
:prod-cluster
  a :Cluster ;
  :name "prod-k8s-cluster" ;
  :orchestration_platform "kubernetes" ;
  :version "1.28.3" ;
  :manages :production-namespace ;
  :manages :order-service-deployment .

:production-namespace
  a :Namespace ;
  :name "production" ;
  :managed_by :prod-cluster .

:order-service-deployment
  a :Deployment ;
  :name "order-service" ;
  :managed_by :prod-cluster .
```

---

## Cross-Layer Relationship Specifications

### 8. packages (Container → Application)

**Definition**: A container packages an application with its dependencies.

**OWL Property Definition**:
```turtle
:packages
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Container ;
  rdfs:range :Application ;
  rdfs:label "packages" ;
  rdfs:comment "A container packages an application" ;
  owl:inverseOf :packaged_in .
```

**Cardinality**: Many Containers to 1 Application (*..1)

**Mandatory**: Yes - Containers SHOULD package an application

**Cross-Layer**: Layer 3 → Layer 2

**Relationship Properties**:
- `packaging_date` (dateTime, optional): When container was built
- `build_version` (string, optional): Build or commit identifier

**Semantic Rules**:
1. Containers encapsulate application code and dependencies
2. One application can be packaged in multiple container instances
3. Container images are immutable snapshots of applications
4. This relationship enables tracing from infrastructure to application logic

**Usage Example**:
```turtle
# Layer 2 (Application)
:order-service-app
  a :Application ;
  :name "Order Service" ;
  :application_type "microservice" ;
  :deployment_model "containerized" ;
  :packaged_in :order-service-container .

# Layer 3 (Container)
:order-service-container
  a :Container ;
  :name "order-service" ;
  :image_name "mycompany/order-service:v1.2.3" ;
  :packages :order-service-app .
```

**Validation Rules**:
```turtle
:ContainerApplicationValidation
  a sh:NodeShape ;
  sh:targetClass :Container ;
  sh:property [
    sh:path :packages ;
    sh:maxCount 1 ;
    sh:class :Application ;
  ] ;
  # Validate application deployment model
  sh:sparql [
    sh:message "Packaged application must have containerized deployment model" ;
    sh:select """
      PREFIX : <http://example.org/ontology#>
      SELECT $this
      WHERE {
        $this a :Container ;
              :packages ?app .
        ?app :deployment_model ?model .
        FILTER(?model != "containerized")
      }
    """ ;
  ] .
```

---

### 9. deployed_as (Application → Pod)

**Definition**: An application is deployed as pods or containers.

**OWL Property Definition**:
```turtle
:deployed_as
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Application ;
  rdfs:range [ owl:unionOf ( :Pod :Container ) ] ;
  rdfs:label "deployed as" ;
  rdfs:comment "An application is deployed as pods or containers" ;
  owl:inverseOf :deploys .
```

**Cardinality**: 1 Application to many Pods/Containers (1..*)

**Mandatory**: Conditional - Only for containerized applications

**Cross-Layer**: Layer 2 → Layer 3

**Relationship Properties**:
- `deployment_date` (dateTime, optional): When deployment occurred
- `deployment_strategy` (enum: rolling, blue_green, canary, optional): Deployment strategy

**Semantic Rules**:
1. Modern applications are deployed as containerized workloads
2. Legacy applications skip this layer entirely (deployed directly on VMs/servers)
3. One application can have multiple pod instances (replicas)
4. This relationship enables decomposition from Application to Container layer

**Usage Example**:
```turtle
# Layer 2 (Application)
:order-service-app
  a :Application ;
  :name "Order Service" ;
  :application_type "microservice" ;
  :deployment_model "containerized" ;
  :deployed_as :order-service-pod-1 ;
  :deployed_as :order-service-pod-2 ;
  :deployed_as :order-service-pod-3 .

# Layer 3 (Container)
:order-service-pod-1
  a :Pod ;
  :name "order-service-pod-abc123" ;
  :deploys :order-service-app .
```

**Validation Rules**:
```turtle
:ApplicationPodValidation
  a sh:NodeShape ;
  sh:targetClass :Application ;
  # Only containerized applications should have deployed_as relationship
  sh:sparql [
    sh:message "Only containerized applications can be deployed as pods" ;
    sh:select """
      PREFIX : <http://example.org/ontology#>
      SELECT $this
      WHERE {
        $this a :Application ;
              :deployed_as ?pod ;
              :deployment_model ?model .
        ?pod a :Pod .
        FILTER(?model != "containerized")
      }
    """ ;
  ] .
```

---

### 10. runs_on (Pod → Infrastructure)

**Definition**: A pod runs on physical or virtual infrastructure.

**OWL Property Definition**:
```turtle
:runs_on
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Pod ;
  rdfs:range [ owl:unionOf ( :VirtualMachine :PhysicalServer :CloudInstance ) ] ;
  rdfs:label "runs on" ;
  rdfs:comment "A pod runs on infrastructure" ;
  owl:inverseOf :hosts .
```

**Cardinality**: Many Pods to 1 Infrastructure (*..1)

**Mandatory**: Yes - Pods MUST be scheduled on infrastructure

**Cross-Layer**: Layer 3 → Layer 4

**Relationship Properties**:
- `scheduled_at` (dateTime, optional): When pod was scheduled
- `resource_allocation` (string, optional): Allocated resources (CPU, memory)

**Semantic Rules**:
1. Pods are scheduled on cluster nodes (VMs or physical servers)
2. Multiple pods can run on the same node
3. Kubernetes scheduler determines pod placement
4. This relationship links Layer 3 to Layer 4

**Usage Example**:
```turtle
# Layer 3 (Container)
:order-service-pod
  a :Pod ;
  :name "order-service-pod-abc123" ;
  :node_name "k8s-worker-node-01" ;
  :runs_on :k8s-worker-node-01 .

# Layer 4 (Physical Infrastructure)
:k8s-worker-node-01
  a :VirtualMachine ;
  :name "k8s-worker-node-01" ;
  :resource_type "virtual" ;
  :hosts :order-service-pod .
```

**Validation Rules**:
```turtle
:PodInfrastructureValidation
  a sh:NodeShape ;
  sh:targetClass :Pod ;
  sh:property [
    sh:path :runs_on ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:or (
      [ sh:class :VirtualMachine ]
      [ sh:class :PhysicalServer ]
      [ sh:class :CloudInstance ]
    ) ;
  ] ;
  # Validate node_name attribute matches relationship
  sh:sparql [
    sh:message "Pod node_name must match runs_on relationship" ;
    sh:select """
      PREFIX : <http://example.org/ontology#>
      SELECT $this
      WHERE {
        $this a :Pod ;
              :node_name ?node_attr ;
              :runs_on ?node_obj .
        ?node_obj :name ?node_name .
        FILTER(?node_attr != ?node_name)
      }
    """ ;
  ] .
```

---

### 11. uses (Container → Storage)

**Definition**: A container uses persistent storage volumes.

**OWL Property Definition**:
```turtle
:uses
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Container ;
  rdfs:range [ owl:unionOf ( :StorageVolume :PersistentVolume ) ] ;
  rdfs:label "uses" ;
  rdfs:comment "A container uses persistent storage" ;
  owl:inverseOf :used_by .
```

**Cardinality**: Many Containers to many Storage (*..*)

**Mandatory**: No - Containers may be stateless

**Cross-Layer**: Layer 3 → Layer 4

**Relationship Properties**:
- `mount_path` (string, mandatory): Container mount path
- `read_only` (boolean, optional): Whether mount is read-only
- `sub_path` (string, optional): Subdirectory within volume

**Semantic Rules**:
1. Containers can mount persistent volumes for data storage
2. PersistentVolumeClaims bind pods to storage
3. Multiple containers can share the same volume
4. This relationship links Layer 3 to Layer 4 storage

**Usage Example**:
```turtle
# Layer 3 (Container)
:postgres-container
  a :Container ;
  :name "postgres" ;
  :image_name "postgres:15.3" ;
  :uses :postgres-pv .

# Layer 4 (Physical Infrastructure)
:postgres-pv
  a :PersistentVolume ;
  :name "postgres-pv-001" ;
  :capacity "50Gi" ;
  :used_by :postgres-container .
```

**Validation Rules**:
```turtle
:ContainerStorageValidation
  a sh:NodeShape ;
  sh:targetClass :Container ;
  sh:property [
    sh:path :uses ;
    sh:or (
      [ sh:class :StorageVolume ]
      [ sh:class :PersistentVolume ]
    ) ;
  ] .
```

---

## Relationship Validation Summary

### Mandatory Relationships

| Entity Type | Mandatory Relationships |
|-------------|------------------------|
| Container | uses_image (1), packages (0..1) |
| Pod | contains (1..*), runs_in (1), runs_on (1) |
| Deployment | manages (1..*) |
| KubernetesService | exposes (1..*) |
| Route | routes_to (1) |
| Namespace | managed_by (1) |

### Cardinality Constraints

| Relationship | Domain | Range | Cardinality |
|--------------|--------|-------|-------------|
| contains | Pod | Container | 1..* |
| part_of | Pod | Deployment | *..1 |
| exposes | KubernetesService | Pod | 1..* |
| routes_to | Route | KubernetesService | *..1 |
| runs_in | Pod | Namespace | *..1 |
| uses_image | Container | ContainerImage | *..1 |
| managed_by | Resource | Cluster | *..1 |
| packages | Container | Application | *..1 |
| deployed_as | Application | Pod | 1..* |
| runs_on | Pod | Infrastructure | *..1 |
| uses | Container | Storage | *..* |

---

## Query Patterns for Relationships

### Pattern 1: Full Decomposition Chain

**Query**: Trace from Application to Infrastructure through Container layer

**SPARQL**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?app ?container ?pod ?node
WHERE {
  ?app a :Application ;
       :name "Order Service" .
  ?app :deployed_as ?pod .
  ?pod :contains ?container .
  ?container :packages ?app .
  ?pod :runs_on ?node .
}
```

---

### Pattern 2: Service Dependency Graph

**Query**: Find all services and their backing pods

**SPARQL**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?service ?pod ?container ?image
WHERE {
  ?service a :KubernetesService ;
           :exposes ?pod .
  ?pod :contains ?container .
  ?container :uses_image ?image .
}
```

---

### Pattern 3: Storage Dependencies

**Query**: Find all containers using persistent storage

**SPARQL**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?container ?pod ?storage ?capacity
WHERE {
  ?container a :Container ;
             :uses ?storage .
  ?pod :contains ?container .
  ?storage :capacity ?capacity .
}
```

---

## Requirements Traceability

### Requirement 2.1: Dependency Relationships

**Satisfied by**:
- All intra-layer relationships defined with clear semantics
- Cross-layer relationships enable dependency tracing

### Requirement 2.2: Directional Relationships

**Satisfied by**:
- All relationships have defined domain and range
- Inverse properties specified for bidirectional navigation

### Requirement 2.4: Cardinality Constraints

**Satisfied by**:
- Cardinality specified for all relationships
- SHACL validation shapes enforce constraints

### Requirement 13.3: Container-Infrastructure Relationships

**Satisfied by**:
- `runs_on` relationship (Pod → Infrastructure)
- `uses` relationship (Container → Storage)

### Requirement 13.4: Orchestration Patterns

**Satisfied by**:
- `part_of` relationship (Pod → Deployment)
- `exposes` relationship (Service → Pod)
- `routes_to` relationship (Route → Service)

---

**Document Complete**: 2025-11-10
**Version**: 1.0
**Status**: Complete

