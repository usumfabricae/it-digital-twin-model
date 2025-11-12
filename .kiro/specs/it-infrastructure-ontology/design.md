# Design Document: IT Infrastructure and Application Dependency Ontology

## Overview

This design document specifies the structure and content of an ontology for representing IT infrastructure and application dependencies across six distinct layers. The ontology enables root cause analysis, impact analysis, and change management by providing a formal model of how business processes, applications, containers, physical infrastructure, network, and security components relate to each other.

The ontology is designed to be:
- **Layered**: Six non-overlapping layers with clear boundaries
- **Standards-based**: Attributes and concepts sourced from TOGAF, CIM, ITIL, and ArchiMate
- **Deployment-agnostic**: Supports both on-premises and cloud infrastructure
- **Architecture-aware**: Accommodates SOA, microservices, and monolithic patterns
- **Formally specified**: Expressible in OWL/RDF for semantic reasoning
- **CMDB-compatible**: Mappable to common CMDB implementations

## Architecture

### Layer Structure

The ontology is organized into six distinct layers, each representing a different level of abstraction in the IT infrastructure stack:

```
┌─────────────────────────────────────────┐
│   Layer 1: Business Processes           │  (What business outcomes)
├─────────────────────────────────────────┤
│   Layer 2: Application Layer            │  (What services/applications)
├─────────────────────────────────────────┤
│   Layer 3: Container & Orchestration    │  (How applications are packaged)
├─────────────────────────────────────────┤
│   Layer 4: Physical Infrastructure      │  (What compute/storage resources)
├─────────────────────────────────────────┤
│   Layer 5: Network Topology & Comm Path │  (How components communicate)
├─────────────────────────────────────────┤
│   Layer 6: Security Infrastructure      │  (How components are secured)
└─────────────────────────────────────────┘
```

### Cross-Layer Relationships

Components can be decomposed across layers through specific relationship types. Note that not all applications traverse all layers - legacy applications may skip the Container layer entirely.

**Containerized Application Path**:
- Business Process → Application (fulfills, supports)
- Application → Container (packaged_in, deployed_as)
- Container → Physical Infrastructure (runs_on, hosted_on)

**Legacy Application Path** (skips Layer 3):
- Business Process → Application (fulfills, supports)
- Application → Physical Infrastructure (runs_on, hosted_on)
- Application Component → Application Server (deployed_on)
- Application Server → Virtual Machine (runs_on)

**Common Cross-Layer Relationships**:
- Application → Network (communicates_via, uses_path)
- All layers → Security (protected_by, secured_by)

### Ontology Formalism

The ontology will be expressed using:
- **OWL 2 (Web Ontology Language)**: For formal class definitions, properties, and axioms
- **RDF Schema**: For basic vocabulary and relationships
- **SHACL (Shapes Constraint Language)**: For validation rules and constraints

## Components and Interfaces

### Layer 1: Business Processes

**Purpose**: Represents business capabilities, processes, and products that drive IT requirements.

**Entity Types**:
- `BusinessProcess`: A sequence of activities that produces a business outcome
- `BusinessCapability`: An ability that the business possesses
- `BusinessService`: A service that supports business operations
- `Product`: A business product or offering

**Attributes** (sourced from TOGAF Business Architecture):
- `name` (string, mandatory): Business-friendly name
- `description` (string, optional): Purpose and scope
- `owner` (string, mandatory): Business owner or stakeholder
- `criticality` (enum: critical, high, medium, low, mandatory): Business importance
- `lifecycle_status` (enum: planned, active, deprecated, retired, mandatory): Current state

**Framework Mapping**:
- TOGAF: Business Architecture metamodel (Business Process, Business Service, Business Capability)
- ArchiMate: Business Layer elements

### Layer 2: Application Layer

**Purpose**: Represents software applications, services, and data objects that fulfill business requirements.

**Entity Types**:
- `Application`: A software system that provides business functionality
- `ApplicationComponent`: A modular part of an application (e.g., servlet, EJB, web service)
- `ApplicationServer`: A runtime environment for applications (e.g., WebSphere, WebLogic, JBoss, Tomcat)
- `Service`: A service in SOA or microservices architecture
- `API`: An application programming interface
- `Database`: A logical database system (e.g., Oracle DB, PostgreSQL, MongoDB)
- `DatabaseInstance`: A specific database instance or schema
- `DataObject`: A logical data entity or schema (tables, collections, documents)
- `MessageQueue`: A message-oriented middleware component (e.g., MQ, RabbitMQ, Kafka)
- `CacheService`: A caching layer (e.g., Redis, Memcached)
- `FileStorageService`: A logical file storage service (e.g., NFS share, CIFS share, mounted filesystem)
- `ObjectStorageService`: A logical object storage service (e.g., S3 bucket, Azure Blob container, GCS bucket)

**Attributes** (sourced from TOGAF Application Architecture and CIM):
- `name` (string, mandatory): Application or service name
- `version` (string, optional): Version identifier
- `application_type` (enum: monolithic, SOA_service, microservice, batch, legacy, mandatory): Architecture pattern
- `deployment_model` (enum: containerized, vm_based, bare_metal, serverless, mandatory): How the application is deployed
- `runtime_environment` (string, optional): Application server or runtime (e.g., WebSphere, Tomcat, Node.js)
- `technology_stack` (string, optional): Primary technologies used (e.g., Java EE, .NET, Python)
- `data_classification` (enum: public, internal, confidential, restricted, optional): Data sensitivity
- `lifecycle_status` (enum: development, testing, production, deprecated, retired, mandatory): Deployment status

**Framework Mapping**:
- TOGAF: Application Architecture metamodel (Application Component, Data Entity)
- CIM: CIM_ApplicationSystem, CIM_DatabaseSystem
- ITIL: Application Management

### Layer 3: Container and Orchestration

**Purpose**: Represents containerization and orchestration technologies that package and manage applications.

**Entity Types**:
- `Container`: A containerized application instance
- `Pod`: A Kubernetes pod or equivalent orchestration unit
- `ContainerImage`: A container image template
- `Cluster`: An orchestration cluster (Kubernetes, Docker Swarm, OpenShift, etc.)
- `Namespace`: A logical isolation boundary within a cluster
- `Deployment`: A deployment configuration for containers
- `Service`: A Kubernetes/OpenShift service that exposes pods
- `Route`: An OpenShift route or Kubernetes ingress that exposes services externally
- `IngressController`: A controller that manages external access to services

**Attributes** (sourced from Kubernetes API, OpenShift API, and CIM):
- `name` (string, mandatory): Container or resource name
- `image_name` (string, optional): Container image reference
- `orchestration_platform` (enum: kubernetes, openshift, docker_swarm, ecs, aci, none, mandatory): Platform type
- `replica_count` (integer, optional): Number of replicas
- `resource_limits` (string, optional): CPU/memory limits
- `exposed_port` (integer, optional): Port exposed by service or route
- `external_hostname` (string, optional): External DNS name for route/ingress
- `route_path` (string, optional): URL path for route
- `tls_termination` (enum: edge, passthrough, reencrypt, none, optional): TLS termination type for routes
- `lifecycle_status` (enum: pending, running, succeeded, failed, unknown, mandatory): Runtime status

**Framework Mapping**:
- Kubernetes API: Pod, Deployment, Service, Namespace, Ingress
- OpenShift API: Route, DeploymentConfig
- CIM: CIM_Container, CIM_VirtualSystemSettingData

### Layer 4: Physical Infrastructure

**Purpose**: Represents physical and virtual compute, storage, and infrastructure resources.

**Entity Types**:
- `PhysicalServer`: A physical server machine
- `VirtualMachine`: A virtualized server instance
- `StorageArray`: A physical storage system (SAN, NAS)
- `StorageVolume`: A logical storage volume or LUN
- `FileSystem`: A mounted file system (NFS, CIFS, local filesystem)
- `StoragePool`: A logical grouping of storage resources
- `Hypervisor`: A virtualization platform
- `CloudInstance`: A cloud provider compute instance (EC2, Azure VM, GCE)
- `CloudStorageService`: A managed cloud storage service (RDS, EBS, Azure Disk, GCS)
- `ObjectStorageBucket`: A physical object storage bucket (S3, Azure Blob, GCS bucket)

**Attributes** (sourced from CIM and cloud provider APIs):
- `name` (string, mandatory): Resource name or identifier
- `resource_type` (enum: physical, virtual, cloud_iaas, cloud_paas, cloud_saas, mandatory): Deployment model
- `location` (string, mandatory): Datacenter, region, or availability zone
- `capacity` (string, optional): CPU, memory, storage capacity
- `operating_system` (string, optional): OS type and version
- `lifecycle_status` (enum: provisioning, running, stopped, terminated, mandatory): Operational state

**Framework Mapping**:
- CIM: CIM_ComputerSystem, CIM_StorageExtent, CIM_VirtualComputerSystem
- TOGAF: Technology Architecture (Platform Services)
- Cloud Provider APIs: AWS EC2, Azure Compute, GCP Compute Engine

### Layer 5: Network Topology and Communication Path

**Purpose**: Represents network infrastructure and communication paths between components.

**Entity Types**:
- `NetworkDevice`: A network device (router, switch, etc.)
- `LoadBalancer`: A load balancing device or service
- `NetworkInterface`: A network interface card or virtual NIC
- `NetworkSegment`: A network subnet or VLAN
- `CommunicationPath`: A logical communication path between components
- `NetworkRoute`: A routing rule or path

**Attributes** (sourced from CIM Network Model):
- `name` (string, mandatory): Device or path name
- `device_type` (enum: router, switch, load_balancer, firewall, gateway, mandatory): Device category
- `ip_address` (string, optional): IP address or range
- `protocol` (string, optional): Communication protocol (TCP, HTTP, gRPC, etc.)
- `port` (integer, optional): Network port number
- `bandwidth` (string, optional): Network capacity
- `lifecycle_status` (enum: active, inactive, degraded, failed, mandatory): Operational state

**Framework Mapping**:
- CIM: CIM_NetworkPort, CIM_IPProtocolEndpoint, CIM_NetworkPipe
- TOGAF: Technology Architecture (Communication Infrastructure)

### Layer 6: Security Infrastructure

**Purpose**: Represents security controls, policies, and infrastructure that protect IT resources.

**Entity Types**:
- `Firewall`: A network firewall device or service
- `WAF`: A web application firewall
- `Certificate`: A digital certificate
- `CertificateAuthority`: A certificate authority
- `SecurityPolicy`: A security policy or rule set
- `IdentityProvider`: An authentication/authorization service
- `SecurityZone`: A security boundary or trust zone

**Attributes** (sourced from security frameworks and CIM):
- `name` (string, mandatory): Security component name
- `security_type` (enum: firewall, waf, ids, ips, certificate, policy, iam, mandatory): Security control type
- `policy_rules` (string, optional): Policy or rule configuration
- `expiration_date` (date, optional): Expiration date for certificates
- `trust_level` (enum: trusted, untrusted, dmz, mandatory): Trust classification
- `lifecycle_status` (enum: active, expired, revoked, disabled, mandatory): Security status

**Framework Mapping**:
- CIM: CIM_SecurityService, CIM_Credential
- NIST Cybersecurity Framework: Protect function
- TOGAF: Security Architecture

## Data Models

### Core Ontology Classes

```turtle
# Base class for all ontology entities
:InfrastructureEntity
  rdf:type owl:Class ;
  rdfs:comment "Base class for all infrastructure components" .

# Layer classes
:BusinessProcessLayer rdfs:subClassOf :InfrastructureEntity .
:ApplicationLayer rdfs:subClassOf :InfrastructureEntity .
:ContainerLayer rdfs:subClassOf :InfrastructureEntity .
:PhysicalInfrastructureLayer rdfs:subClassOf :InfrastructureEntity .
:NetworkLayer rdfs:subClassOf :InfrastructureEntity .
:SecurityLayer rdfs:subClassOf :InfrastructureEntity .

# Example entity types
:Application rdfs:subClassOf :ApplicationLayer .
:Database rdfs:subClassOf :ApplicationLayer .
:PhysicalServer rdfs:subClassOf :PhysicalInfrastructureLayer .
:Container rdfs:subClassOf :ContainerLayer .
```

### Relationship Types

**Cross-Layer Relationships**:
- `fulfills`: Business Process → Application (a business process is fulfilled by applications)
- `supports`: Application → Business Process (an application supports business processes)
- `uses`: Application → Database, Application → API (an application uses data or services)
- `packaged_in`: Application → Container (an application is packaged in a container)
- `deployed_as`: Application → Container (an application is deployed as containers)
- `runs_on`: Container → Physical Infrastructure (a container runs on infrastructure)
- `hosted_on`: Database → Physical Infrastructure (a database is hosted on infrastructure)
- `communicates_via`: Application → Network Path (an application communicates via network)
- `protected_by`: Any Entity → Security Component (an entity is protected by security controls)
- `secured_by`: Any Entity → Security Policy (an entity is secured by policies)

**Intra-Layer Relationships**:
- `depends_on`: Application → Application (service dependencies)
- `calls`: Service → Service (API calls)
- `connected_to`: Network Device → Network Device (physical connections)
- `routes_through`: Communication Path → Network Device (routing)
- `part_of`: Component → Parent Component (composition)

**Relationship Properties**:
- `criticality` (enum: critical, high, medium, low): Importance of the relationship
- `dependency_type` (enum: synchronous, asynchronous, batch): Nature of dependency
- `direction` (enum: unidirectional, bidirectional): Relationship direction

### Cardinality Constraints

- Business Process → Application: 1 to many (one process can use multiple applications)
- Application → Container: 1 to many (one application can have multiple container instances)
- Container → Physical Infrastructure: many to 1 (multiple containers on one host)
- Application → Database: many to many (applications can share databases)
- Application → Network Path: 1 to many (one application can use multiple paths)
- Entity → Security Component: many to many (multiple entities protected by multiple controls)

## Framework Mappings

### TOGAF Metamodel Mapping

| Ontology Layer | TOGAF Layer | TOGAF Elements |
|----------------|-------------|----------------|
| Business Processes | Business Architecture | Business Process, Business Service, Business Capability |
| Application Layer | Application Architecture | Application Component, Data Entity, Application Service |
| Container & Orchestration | Technology Architecture | Platform Services (partial) |
| Physical Infrastructure | Technology Architecture | Platform Services, Physical Technology Components |
| Network Topology | Technology Architecture | Communication Infrastructure |
| Security Infrastructure | Security Architecture | Security Services, Security Policies |

### CIM Class Mapping

| Ontology Entity Type | CIM Class | CIM Namespace |
|----------------------|-----------|---------------|
| Application | CIM_ApplicationSystem | CIM_Application |
| Database | CIM_DatabaseSystem | CIM_Database |
| PhysicalServer | CIM_ComputerSystem | CIM_Core |
| VirtualMachine | CIM_VirtualComputerSystem | CIM_Virtualization |
| StorageVolume | CIM_StorageExtent | CIM_Storage |
| NetworkDevice | CIM_NetworkDevice | CIM_Network |
| NetworkInterface | CIM_NetworkPort | CIM_Network |
| Firewall | CIM_SecurityService | CIM_Security |
| Container | CIM_Container | CIM_Virtualization |

### ITIL Process Mapping

| Ontology Layer | ITIL Process Area |
|----------------|-------------------|
| Business Processes | Service Strategy, Service Design |
| Application Layer | Application Management, Service Design |
| Container & Orchestration | Technical Management |
| Physical Infrastructure | Technical Management, Capacity Management |
| Network Topology | Technical Management, Network Management |
| Security Infrastructure | Information Security Management |

## Validation Rules and Constraints

### Layer Assignment Rules

1. Each entity type MUST belong to exactly one layer
2. Entities CANNOT have attributes from multiple layers
3. Cross-layer relationships MUST connect entities from different layers
4. Intra-layer relationships MUST connect entities within the same layer

### Attribute Constraints

1. Mandatory attributes MUST be present for all entity instances
2. Enumeration attributes MUST use only defined values
3. Lifecycle status MUST follow valid state transitions
4. Framework-sourced attributes MUST maintain semantic consistency with source framework

### Relationship Constraints

1. Relationship types MUST respect cardinality constraints
2. Circular dependencies SHOULD be flagged for review
3. Cross-layer relationships MUST follow allowed patterns (e.g., Application → Database → Server)
4. Orphaned entities (no relationships) SHOULD be flagged for review

### SHACL Validation Example

```turtle
:ApplicationShape
  a sh:NodeShape ;
  sh:targetClass :Application ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:in ( "development" "testing" "production" "deprecated" "retired" ) ;
  ] ;
  sh:property [
    sh:path :runs_on ;
    sh:class :PhysicalInfrastructureLayer ;
  ] .
```

## Query Patterns

### Root Cause Analysis Query

**Scenario**: An application is experiencing issues. Find all infrastructure components it depends on.

**SPARQL Query**:
```sparql
SELECT ?component ?layer ?status
WHERE {
  :MyApplication (:uses|:runs_on|:hosted_on|:communicates_via)+ ?component .
  ?component rdf:type ?layer .
  ?component :lifecycle_status ?status .
  FILTER(?status IN ("degraded", "failed"))
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (app:Application {name: 'MyApplication'})-[r:USES|RUNS_ON|HOSTED_ON|COMMUNICATES_VIA*]->(component)
WHERE component.lifecycle_status IN ['degraded', 'failed']
RETURN component.name AS component, 
       labels(component) AS layer, 
       component.lifecycle_status AS status
```

### Impact Analysis Query

**Scenario**: A server needs maintenance. Find all applications and business processes affected.

**SPARQL Query**:
```sparql
SELECT ?affected ?type
WHERE {
  ?affected (:runs_on|:hosted_on|:uses)+ :Server123 .
  ?affected rdf:type ?type .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (affected)-[r:RUNS_ON|HOSTED_ON|USES*]->(server:PhysicalServer {name: 'Server123'})
RETURN affected.name AS affected, 
       labels(affected) AS type
```

### Decomposition Chain Query

**Scenario**: Trace a business process down to physical infrastructure.

**SPARQL Query**:
```sparql
SELECT ?layer1 ?layer2 ?layer3 ?layer4
WHERE {
  :BusinessProcess1 :fulfills ?layer1 .
  ?layer1 :uses ?layer2 .
  ?layer2 :hosted_on ?layer3 .
  ?layer3 :runs_on ?layer4 .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH path = (bp:BusinessProcess {name: 'BusinessProcess1'})-[:FULFILLS]->(app:Application)
             -[:USES]->(db:Database)
             -[:HOSTED_ON]->(vm:VirtualMachine)
             -[:RUNS_ON]->(server:PhysicalServer)
RETURN bp.name AS business_process,
       app.name AS application,
       db.name AS database,
       vm.name AS virtual_machine,
       server.name AS physical_server
```

### Storage Dependency Query

**Scenario**: Find all applications using a specific storage array.

**SPARQL Query**:
```sparql
SELECT ?application ?storage_service ?volume
WHERE {
  ?application :uses ?storage_service .
  ?storage_service :stored_on ?volume .
  ?volume :allocated_from :StorageArray_SAN01 .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (app:Application)-[:USES]->(storage)-[:STORED_ON]->(volume:StorageVolume)
      -[:ALLOCATED_FROM]->(array:StorageArray {name: 'StorageArray_SAN01'})
RETURN app.name AS application,
       storage.name AS storage_service,
       volume.name AS volume
```

### Network Path Analysis Query

**Scenario**: Find all network devices in the communication path between two applications.

**SPARQL Query**:
```sparql
SELECT ?network_device
WHERE {
  :Application1 :communicates_via ?path .
  ?path :routes_through ?network_device .
  ?network_device :connected_to* ?target_device .
  :Application2 :communicates_via ?target_path .
  ?target_path :routes_through ?target_device .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (app1:Application {name: 'Application1'})-[:COMMUNICATES_VIA]->(path1:CommunicationPath)
      -[:ROUTES_THROUGH]->(device:NetworkDevice)
      -[:CONNECTED_TO*]-(device2:NetworkDevice)
      <-[:ROUTES_THROUGH]-(path2:CommunicationPath)
      <-[:COMMUNICATES_VIA]-(app2:Application {name: 'Application2'})
RETURN DISTINCT device.name AS network_device
```

### Security Dependency Query

**Scenario**: Find all security components protecting an application and its dependencies.

**SPARQL Query**:
```sparql
SELECT ?component ?security_control ?security_type
WHERE {
  {
    :MyApplication :protected_by ?security_control .
  } UNION {
    :MyApplication (:uses|:runs_on|:hosted_on)+ ?component .
    ?component :protected_by ?security_control .
  }
  ?security_control :security_type ?security_type .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (app:Application {name: 'MyApplication'})
OPTIONAL MATCH (app)-[:PROTECTED_BY]->(sec1:SecurityLayer)
OPTIONAL MATCH (app)-[:USES|RUNS_ON|HOSTED_ON*]->(component)-[:PROTECTED_BY]->(sec2:SecurityLayer)
WITH app, sec1, component, sec2
UNWIND [sec1, sec2] AS security_control
WHERE security_control IS NOT NULL
RETURN DISTINCT component.name AS component,
                security_control.name AS security_control,
                security_control.security_type AS security_type
```

### Cross-Layer Dependency Count Query

**Scenario**: Count dependencies at each layer for an application.

**SPARQL Query**:
```sparql
SELECT ?layer (COUNT(?component) AS ?count)
WHERE {
  :MyApplication (:uses|:runs_on|:hosted_on|:communicates_via)+ ?component .
  ?component rdf:type ?layer .
}
GROUP BY ?layer
ORDER BY ?count DESC
```

**Cypher Query** (Neo4j):
```cypher
MATCH (app:Application {name: 'MyApplication'})-[r:USES|RUNS_ON|HOSTED_ON|COMMUNICATES_VIA*]->(component)
WITH labels(component)[0] AS layer, COUNT(DISTINCT component) AS count
RETURN layer, count
ORDER BY count DESC
```

## Storage Component Model

Storage components are modeled across two layers depending on their abstraction level:

### Layer 2: Logical Storage (Application Layer)

**Purpose**: Represents storage from the application's perspective - what the application uses.

**Entity Types**:
- `Database`: Logical database system (Oracle, PostgreSQL, MongoDB)
- `DatabaseInstance`: Specific database instance or schema
- `DataObject`: Logical data structures (tables, collections)
- `FileStorageService`: Logical file storage (NFS share, CIFS share, mounted path)
- `ObjectStorageService`: Logical object storage (S3 bucket, Azure Blob container)
- `CacheService`: Caching layer (Redis, Memcached)

**Storage Type Distinctions**:
- **Database**: Structured data with query capabilities (SQL, NoSQL)
- **File Storage**: Hierarchical file systems with directories and files (NFS, CIFS, local mounts)
- **Object Storage**: Flat namespace with key-value access (S3, Blob, GCS)
- **Cache**: In-memory temporary data storage

**Example**: 
- Application "Order Service" `uses` Database "OrderDB"
- Application "Media Processor" `uses` FileStorageService "/mnt/media"
- Application "Backup Service" `uses` ObjectStorageService "backup-bucket"

### Layer 4: Physical Storage (Physical Infrastructure Layer)

**Purpose**: Represents the physical storage infrastructure - where data is actually stored.

**Entity Types**:
- `StorageArray`: Physical storage hardware (SAN, NAS)
- `StorageVolume`: Logical volume or LUN
- `FileSystem`: Mounted filesystem (NFS, CIFS, ext4, NTFS)
- `StoragePool`: Logical grouping of storage
- `CloudStorageService`: Managed cloud storage (RDS instance, EBS volume)
- `ObjectStorageBucket`: Physical object storage bucket

**Example**:
- Database "OrderDB" `hosted_on` StorageVolume "vol-12345"
- StorageVolume "vol-12345" `allocated_from` StorageArray "NetApp-SAN-01"

### Storage Decomposition Patterns

#### Pattern 1: On-Premises Database

**Decomposition**: Application → Database → Storage Volume → Storage Array

**Example**: Legacy Oracle database
- Application: "ERP System"
- Database: "ERP_PROD_DB" (Oracle 19c)
- Database Instance: "ERPDB01"
- Storage Volume: "LUN-456" (500GB)
- Storage Array: "EMC-VNX-01" (SAN)

**Relationships**:
- ERP System `uses` ERP_PROD_DB
- ERP_PROD_DB `contains` ERPDB01
- ERPDB01 `stored_on` LUN-456
- LUN-456 `allocated_from` EMC-VNX-01

#### Pattern 2: Cloud Managed Database

**Decomposition**: Application → Database → Cloud Storage Service

**Example**: AWS RDS PostgreSQL
- Application: "Customer Portal"
- Database: "CustomerDB" (PostgreSQL)
- Cloud Storage Service: "RDS Instance db-abc123"

**Relationships**:
- Customer Portal `uses` CustomerDB
- CustomerDB `hosted_on` RDS Instance db-abc123

#### Pattern 3: Object Storage

**Decomposition**: Application → Object Storage Service → Object Storage Bucket

**Example**: S3 for document storage
- Application: "Document Management System"
- Object Storage Service: "documents-bucket" (logical S3 bucket)
- Object Storage Bucket: "s3://documents-bucket" (physical bucket in us-east-1)

**Relationships**:
- Document Management System `uses` documents-bucket
- documents-bucket `stored_in` s3://documents-bucket

#### Pattern 4: Shared File System

**Decomposition**: Application → File System → Storage Volume → Storage Array

**Example**: NFS shared storage
- Application: "Media Processing Service"
- File System: "/mnt/media-storage" (NFS mount)
- Storage Volume: "nfs-vol-789"
- Storage Array: "NetApp-NAS-02"

**Relationships**:
- Media Processing Service `uses` /mnt/media-storage
- /mnt/media-storage `mounted_from` nfs-vol-789
- nfs-vol-789 `allocated_from` NetApp-NAS-02

#### Pattern 5: Containerized Database with Persistent Volume

**Decomposition**: Application → Database → Container → Persistent Volume → Storage

**Example**: PostgreSQL in Kubernetes with persistent storage
- Application: "Analytics Service"
- Database: "AnalyticsDB" (PostgreSQL)
- Container: "postgres-container"
- Persistent Volume Claim: "postgres-pvc"
- Storage Volume: "ebs-vol-xyz"
- Cloud Storage Service: "AWS EBS"

**Relationships**:
- Analytics Service `uses` AnalyticsDB
- AnalyticsDB `deployed_as` postgres-container
- postgres-container `uses` postgres-pvc
- postgres-pvc `bound_to` ebs-vol-xyz
- ebs-vol-xyz `provisioned_from` AWS EBS

### Storage Relationship Types

**Application to Storage (Layer 2)**:
- `uses`: Application uses Database/ObjectStorage/FileSystem
- `reads_from`: Application reads from storage
- `writes_to`: Application writes to storage

**Storage to Infrastructure (Layer 2 → Layer 4)**:
- `hosted_on`: Database hosted on physical/cloud storage
- `stored_on`: Data stored on storage volume
- `stored_in`: Data stored in object storage bucket
- `mounted_from`: Filesystem mounted from storage volume

**Infrastructure Storage (Layer 4)**:
- `allocated_from`: Volume allocated from storage array
- `provisioned_from`: Cloud storage provisioned from cloud service
- `replicated_to`: Storage replicated to another volume/array

## Application Deployment Patterns

### Pattern 1: Containerized Applications (Modern)

**Decomposition Path**: Business Process → Application → Container → VM/Physical Server

**Example**: Microservice deployed in Kubernetes
- Business Process: "Order Processing"
- Application: "Order Service" (microservice)
- Container: "order-service:v1.2" (Docker container)
- Pod: "order-service-pod-abc123" (Kubernetes pod)
- Virtual Machine: "k8s-worker-node-01" (VM running Kubernetes)
- Physical Server: "server-rack-05-slot-12" (physical host)

**Relationships**:
- Order Processing `fulfills` Order Service
- Order Service `deployed_as` order-service:v1.2
- order-service:v1.2 `packaged_in` order-service-pod-abc123
- order-service-pod-abc123 `runs_on` k8s-worker-node-01
- k8s-worker-node-01 `runs_on` server-rack-05-slot-12

### Pattern 2: Legacy Applications on Application Servers

**Decomposition Path**: Business Process → Application → Application Server → VM → Physical Server

**Example**: Java EE application on WebSphere
- Business Process: "Customer Management"
- Application: "CRM Application"
- Application Component: "CustomerServlet" (servlet)
- Application Server: "WebSphere 9.0 Instance" (application server)
- Virtual Machine: "crm-app-vm-01" (VM)
- Physical Server: "server-rack-03-slot-08" (physical host)

**Relationships**:
- Customer Management `fulfills` CRM Application
- CRM Application `contains` CustomerServlet
- CustomerServlet `deployed_on` WebSphere 9.0 Instance
- WebSphere 9.0 Instance `runs_on` crm-app-vm-01
- crm-app-vm-01 `hosted_on` server-rack-03-slot-08

**Note**: Layer 3 (Container & Orchestration) is bypassed for legacy applications.

### Pattern 3: Serverless/Cloud-Native

**Decomposition Path**: Business Process → Application → Cloud Service

**Example**: AWS Lambda function
- Business Process: "Image Processing"
- Application: "Image Resizer Function"
- Cloud Service: "AWS Lambda" (managed service)

**Relationships**:
- Image Processing `fulfills` Image Resizer Function
- Image Resizer Function `runs_on` AWS Lambda

**Note**: Both Layer 3 and Layer 4 are abstracted away by the cloud provider.

### Pattern 4: Hybrid SOA Integration

**Decomposition Path**: Multiple applications across different deployment models

**Example**: Order processing integrating legacy and modern services
- Business Process: "Order Fulfillment"
- Application 1: "Order API" (microservice in Kubernetes)
- Application 2: "Inventory System" (legacy on WebSphere)
- Application 3: "Payment Gateway" (cloud SaaS)
- Message Queue: "Order Queue" (RabbitMQ)

**Relationships**:
- Order Fulfillment `fulfills` Order API, Inventory System, Payment Gateway
- Order API `calls` Inventory System (via Message Queue)
- Order API `calls` Payment Gateway (via API)
- Order API `uses` Order Queue
- Inventory System `uses` Order Queue

## Deployment Models

### On-Premises Infrastructure

**Characteristics**:
- Physical servers in organization-owned datacenters
- Traditional network topology with physical devices
- Legacy applications and databases
- Manual or semi-automated provisioning

**Ontology Considerations**:
- Emphasis on Physical Infrastructure layer entities
- Detailed network topology modeling
- Physical location attributes (datacenter, rack, etc.)
- Hardware lifecycle management

### Cloud Infrastructure

**Characteristics**:
- Virtual resources from cloud providers (AWS, Azure, GCP)
- Software-defined networking
- Managed services (PaaS, SaaS)
- API-driven provisioning

**Ontology Considerations**:
- Cloud-specific entity types (CloudInstance, CloudService)
- Region and availability zone attributes
- Cloud provider-specific attributes
- Managed service dependencies

### Hybrid Infrastructure

**Characteristics**:
- Mix of on-premises and cloud resources
- Hybrid networking (VPN, Direct Connect, ExpressRoute)
- Data synchronization between environments
- Workload portability requirements

**Ontology Considerations**:
- Deployment model attribute to distinguish on-prem vs. cloud
- Cross-environment relationships
- Network path modeling for hybrid connectivity
- Consistent abstraction across deployment models

## Extension Points

### Adding New Entity Types

1. Identify the appropriate layer for the new entity type
2. Define entity type as subclass of layer class
3. Specify attributes sourced from relevant frameworks
4. Define relationships to existing entity types
5. Create SHACL validation shapes
6. Document framework mappings

### Adding New Frameworks

1. Analyze framework metamodel and concepts
2. Map framework concepts to ontology layers
3. Identify attribute candidates from framework
4. Document mappings in framework mapping tables
5. Update entity type definitions with new attributes
6. Cite framework in attribute documentation

### Custom Attributes

Organizations may need custom attributes beyond framework-sourced ones:
1. Custom attributes SHOULD be namespaced separately (e.g., `custom:attribute_name`)
2. Custom attributes SHOULD NOT conflict with framework attributes
3. Custom attributes SHOULD be documented with rationale
4. Custom attributes MAY be proposed for inclusion in future ontology versions

## Tooling and Implementation

### Ontology Development Tools

- **Protégé**: OWL ontology editor for creating and editing the ontology
- **TopBraid Composer**: Commercial ontology development environment
- **WebVOWL**: Visualization tool for OWL ontologies

### Validation and Reasoning Tools

- **Apache Jena**: Java framework for RDF and OWL processing
- **RDFLib**: Python library for RDF manipulation
- **SHACL Validator**: Tools for validating RDF data against SHACL shapes
- **HermiT / Pellet**: OWL reasoners for consistency checking and inference

### Graph Database Options

- **Neo4j**: Property graph database with Cypher query language
- **Amazon Neptune**: Managed graph database supporting RDF and property graphs
- **Stardog**: Enterprise knowledge graph platform with reasoning
- **GraphDB**: RDF graph database with SPARQL support

### Visualization Tools

- **Cytoscape**: Network visualization platform
- **Gephi**: Graph visualization and exploration tool
- **D3.js**: JavaScript library for custom graph visualizations
- **yEd**: Diagramming tool for graph layouts

## Next Steps for Design Validation

To validate this design, the following activities are recommended:

1. **Framework Analysis**: Deep dive into TOGAF, CIM, ITIL, and ArchiMate to extract complete attribute sets
2. **Entity Type Enumeration**: Create comprehensive lists of entity types for each layer
3. **Relationship Catalog**: Document all relationship types with cardinality and constraints
4. **Sample Instance Data**: Create a complex architecture of multiple applications interacting through seevices exposed via API, Load Balancers esposed via microservices and also java application services, spanning multiple datacenters or regions in otrder to test the ontology structure
5. **Query Testing**: Develop and test SPARQL queries for common use cases
. **Stakeholder Review**: Review with IT architects, operations teams
8. **Prototype Development**: Build a small-scale prototype with sample data
