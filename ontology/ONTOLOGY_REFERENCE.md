# IT Infrastructure and Application Dependency Ontology - Reference Documentation

## Document Information

- **Version**: 1.0.0
- **Date**: 2024-01-15
- **Status**: Complete
- **Ontology URI**: `http://example.org/it-infrastructure-ontology#`
- **Prefix**: `:`

## Table of Contents

1. [Introduction](#introduction)
2. [Ontology Architecture](#ontology-architecture)
3. [Entity Types by Layer](#entity-types-by-layer)
4. [Relationship Types](#relationship-types)
5. [Data Properties (Attributes)](#data-properties-attributes)
6. [Framework Mappings](#framework-mappings)
7. [Validation Rules](#validation-rules)
8. [Usage Examples](#usage-examples)
9. [Extension Guidelines](#extension-guidelines)

---

## Introduction

The IT Infrastructure and Application Dependency Ontology is a formal OWL 2 ontology that provides a comprehensive model for representing IT infrastructure and application dependencies across six distinct architectural layers. The ontology enables root cause analysis, impact assessment, and full-stack decomposition from business processes to physical infrastructure.

### Purpose

- Model enterprise IT infrastructure using semantic web standards (OWL, RDF, SHACL)
- Support dependency tracking across business, application, container, infrastructure, network, and security layers
- Enable SPARQL and Cypher queries for root cause and impact analysis
- Provide CMDB integration capabilities with formal validation rules

### Key Features

- **Six-layer architecture** with clear separation of concerns
- **50+ entity types** covering modern and legacy deployments
- **Framework alignment** with TOGAF, CIM, ITIL, ArchiMate, Kubernetes, and cloud provider APIs
- **SHACL validation shapes** for data quality enforcement
- **Comprehensive deployment patterns** (containerized, legacy, hybrid, cloud)
- **Query patterns** for operational analysis and troubleshooting

### Target Audience

- IT Architects and Enterprise Architects
- Operations Engineers and SREs
- Data Modelers and Knowledge Engineers
- CMDB Administrators
- Application Developers integrating with semantic technologies

---

## Ontology Architecture

### Layer Structure

The ontology is organized into six disjoint layers, ensuring each entity belongs to exactly one layer:

```
┌─────────────────────────────────────────┐
│   Layer 1: Business Processes           │  Business capabilities, processes, services
├─────────────────────────────────────────┤
│   Layer 2: Application Layer            │  Applications, services, databases, APIs
├─────────────────────────────────────────┤
│   Layer 3: Container & Orchestration    │  Containers, pods, clusters, orchestration
├─────────────────────────────────────────┤
│   Layer 4: Physical Infrastructure      │  Servers, storage, VMs, cloud resources
├─────────────────────────────────────────┤
│   Layer 5: Network Topology             │  Network devices, paths, communication
├─────────────────────────────────────────┤
│   Layer 6: Security Infrastructure      │  Firewalls, certificates, policies, controls
└─────────────────────────────────────────┘
```

### Base Class Hierarchy

```turtle
:InfrastructureEntity
  rdf:type owl:Class ;
  rdfs:label "Infrastructure Entity" ;
  rdfs:comment "Base class for all infrastructure components" .

# Layer Classes (all disjoint)
:BusinessProcessLayer rdfs:subClassOf :InfrastructureEntity .
:ApplicationLayer rdfs:subClassOf :InfrastructureEntity .
:ContainerLayer rdfs:subClassOf :InfrastructureEntity .
:PhysicalInfrastructureLayer rdfs:subClassOf :InfrastructureEntity .
:NetworkLayer rdfs:subClassOf :InfrastructureEntity .
:SecurityLayer rdfs:subClassOf :InfrastructureEntity .
```

### Cross-Layer Relationships

Components can be decomposed across layers through specific relationship types:

- **Business → Application**: `realized_by`, `requires`
- **Application → Container**: `deployed_as`, `packaged_in`
- **Application → Infrastructure**: `runs_on`, `hosted_on`
- **Container → Infrastructure**: `runs_on`
- **Application → Network**: `communicates_via`
- **Any Layer → Security**: `protected_by`, `secured_by`

---

## Entity Types by Layer

### Layer 1: Business Process Layer

#### BusinessProcess

**Definition**: A sequence of activities that produces a business outcome.

**Framework Source**: TOGAF Business Architecture, ArchiMate Business Layer

**Key Attributes**:
- `name` (string, mandatory) - Business-friendly name
- `owner` (string, mandatory) - Business owner or stakeholder
- `criticality` (enum, mandatory) - Business importance: critical, high, medium, low
- `lifecycle_status` (enum, mandatory) - Current state: planned, active, deprecated, retired
- `process_type` (enum, mandatory) - Type: core, supporting, management
- `frequency` (enum, optional) - Execution frequency: real-time, hourly, daily, weekly, monthly, quarterly, annual, on-demand

**OWL Class**:
```turtle
:BusinessProcess
  rdf:type owl:Class ;
  rdfs:subClassOf :BusinessProcessLayer ;
  rdfs:label "Business Process" ;
  skos:definition "A sequence of activities that produces a business outcome" .
```

#### BusinessCapability

**Definition**: An ability that the business possesses to achieve specific outcomes.

**Framework Source**: TOGAF Business Architecture, ArchiMate Business Layer

**Key Attributes**:
- `name` (string, mandatory) - Capability name
- `capability_level` (enum, mandatory) - Maturity level: initial, developing, defined, managed, optimizing
- `criticality` (enum, mandatory) - Business importance
- `lifecycle_status` (enum, mandatory) - Current state

#### BusinessService

**Definition**: A service that supports business operations and delivers value to stakeholders.

**Framework Source**: TOGAF Business Architecture, ITIL Service Strategy

**Key Attributes**:
- `name` (string, mandatory) - Service name
- `service_level` (string, optional) - Service level agreement or target
- `criticality` (enum, mandatory) - Business importance
- `lifecycle_status` (enum, mandatory) - Current state

#### Product

**Definition**: A business product or offering delivered to customers.

**Framework Source**: TOGAF Business Architecture

**Key Attributes**:
- `name` (string, mandatory) - Product name
- `product_type` (enum, mandatory) - Type: physical, digital, service, hybrid
- `criticality` (enum, mandatory) - Business importance
- `lifecycle_status` (enum, mandatory) - Current state

---

### Layer 2: Application Layer

#### Application

**Definition**: A software system that provides business functionality.

**Framework Source**: TOGAF Application Architecture, CIM_ApplicationSystem

**Key Attributes**:
- `name` (string, mandatory) - Application name
- `version` (string, optional) - Version identifier
- `application_type` (enum, mandatory) - Architecture pattern: monolithic, SOA_service, microservice, batch, legacy
- `deployment_model` (enum, mandatory) - Deployment type: containerized, vm_based, bare_metal, serverless
- `runtime_environment` (string, optional) - Runtime (e.g., "WebSphere", "Tomcat", "Node.js")
- `technology_stack` (string, optional) - Technologies (e.g., "Java EE", ".NET", "Python")
- `data_classification` (enum, optional) - Data sensitivity: public, internal, confidential, restricted
- `lifecycle_status` (enum, mandatory) - State: development, testing, production, deprecated, retired

#### ApplicationComponent

**Definition**: A modular part of an application (e.g., servlet, EJB, web service).

**Framework Source**: TOGAF Application Architecture

**Key Attributes**:
- `name` (string, mandatory) - Component name
- `component_type` (enum, mandatory) - Type: servlet, ejb, web_service, rest_api, batch_job, scheduled_task
- `version` (string, optional) - Component version
- `lifecycle_status` (enum, mandatory) - Current state

#### ApplicationServer

**Definition**: A runtime environment for applications (e.g., WebSphere, WebLogic, JBoss, Tomcat).

**Framework Source**: CIM_ApplicationSystem, TOGAF Technology Architecture

**Key Attributes**:
- `name` (string, mandatory) - Server instance name
- `server_type` (enum, mandatory) - Type: websphere, weblogic, jboss, tomcat, iis, apache, nginx
- `version` (string, optional) - Server version
- `port` (integer, optional) - Primary listening port
- `lifecycle_status` (enum, mandatory) - State: running, stopped, degraded, failed

#### Service

**Definition**: A service in SOA or microservices architecture.

**Framework Source**: TOGAF Application Architecture, ArchiMate Application Layer

**Key Attributes**:
- `name` (string, mandatory) - Service name
- `service_type` (enum, mandatory) - Type: rest, soap, grpc, graphql, messaging
- `endpoint_url` (anyURI, optional) - Service endpoint URL
- `version` (string, optional) - Service version
- `lifecycle_status` (enum, mandatory) - Current state

#### API

**Definition**: An application programming interface.

**Framework Source**: TOGAF Application Architecture

**Key Attributes**:
- `name` (string, mandatory) - API name
- `api_type` (enum, mandatory) - Type: rest, soap, graphql, grpc, websocket
- `endpoint_url` (anyURI, optional) - API endpoint URL
- `version` (string, optional) - API version
- `authentication_type` (enum, optional) - Auth type: none, basic, oauth2, api_key, jwt
- `lifecycle_status` (enum, mandatory) - Current state

#### Database

**Definition**: A logical database system (e.g., Oracle DB, PostgreSQL, MongoDB).

**Framework Source**: CIM_DatabaseSystem, TOGAF Application Architecture

**Key Attributes**:
- `name` (string, mandatory) - Database name
- `database_type` (enum, mandatory) - Type: relational, nosql_document, nosql_keyvalue, nosql_graph, nosql_columnar, timeseries
- `database_engine` (string, optional) - Engine (e.g., "Oracle", "PostgreSQL", "MongoDB")
- `version` (string, optional) - Database version
- `port` (integer, optional) - Database port
- `data_classification` (enum, optional) - Data sensitivity
- `lifecycle_status` (enum, mandatory) - Current state

#### DatabaseInstance

**Definition**: A specific database instance or schema.

**Framework Source**: CIM_DatabaseSystem

**Key Attributes**:
- `name` (string, mandatory) - Instance or schema name
- `instance_id` (string, optional) - Unique instance identifier
- `size_gb` (decimal, optional) - Database size in GB
- `lifecycle_status` (enum, mandatory) - Current state

#### DataObject

**Definition**: A logical data entity or schema (tables, collections, documents).

**Framework Source**: TOGAF Application Architecture

**Key Attributes**:
- `name` (string, mandatory) - Data object name
- `object_type` (enum, mandatory) - Type: table, view, collection, document, schema
- `data_classification` (enum, optional) - Data sensitivity
- `lifecycle_status` (enum, mandatory) - Current state

#### MessageQueue

**Definition**: A message-oriented middleware component (e.g., MQ, RabbitMQ, Kafka).

**Framework Source**: TOGAF Application Architecture

**Key Attributes**:
- `name` (string, mandatory) - Queue name
- `queue_type` (enum, mandatory) - Type: point_to_point, publish_subscribe, streaming
- `queue_engine` (string, optional) - Engine (e.g., "RabbitMQ", "Kafka", "IBM MQ")
- `lifecycle_status` (enum, mandatory) - Current state

#### CacheService

**Definition**: A caching layer (e.g., Redis, Memcached).

**Framework Source**: TOGAF Application Architecture

**Key Attributes**:
- `name` (string, mandatory) - Cache service name
- `cache_type` (enum, mandatory) - Type: in_memory, distributed, cdn
- `cache_engine` (string, optional) - Engine (e.g., "Redis", "Memcached")
- `lifecycle_status` (enum, mandatory) - Current state

#### FileStorageService

**Definition**: A logical file storage service (e.g., NFS share, CIFS share, mounted filesystem).

**Framework Source**: CIM Storage Model

**Key Attributes**:
- `name` (string, mandatory) - Storage service name
- `storage_type` (enum, mandatory) - Type: nfs, cifs, local, cloud_file
- `mount_path` (string, optional) - Mount point or path
- `capacity_gb` (decimal, optional) - Storage capacity in GB
- `lifecycle_status` (enum, mandatory) - Current state

#### ObjectStorageService

**Definition**: A logical object storage service (e.g., S3 bucket, Azure Blob container, GCS bucket).

**Framework Source**: Cloud Provider APIs (AWS S3, Azure Blob, GCS)

**Key Attributes**:
- `name` (string, mandatory) - Storage service name
- `storage_type` (enum, mandatory) - Type: s3, azure_blob, gcs, object_storage
- `bucket_name` (string, optional) - Bucket or container name
- `region` (string, optional) - Cloud region
- `lifecycle_status` (enum, mandatory) - Current state

---

### Layer 3: Container and Orchestration Layer

#### Container

**Definition**: A containerized application instance.

**Framework Source**: Kubernetes API, Docker, CIM_Container

**Key Attributes**:
- `name` (string, mandatory) - Container name
- `container_id` (string, optional) - Unique container identifier
- `image_name` (string, optional) - Container image reference
- `image_tag` (string, optional) - Image tag or version
- `port` (integer, optional) - Exposed port
- `resource_limits_cpu` (string, optional) - CPU limits
- `resource_limits_memory` (string, optional) - Memory limits
- `lifecycle_status` (enum, mandatory) - State: pending, running, succeeded, failed, unknown

#### Pod

**Definition**: A Kubernetes pod or equivalent orchestration unit.

**Framework Source**: Kubernetes API

**Key Attributes**:
- `name` (string, mandatory) - Pod name
- `pod_id` (string, optional) - Unique pod identifier
- `replica_count` (integer, optional) - Number of replicas
- `restart_policy` (enum, optional) - Restart policy: always, on_failure, never
- `lifecycle_status` (enum, mandatory) - State: pending, running, succeeded, failed, unknown

#### ContainerImage

**Definition**: A container image template.

**Framework Source**: Docker, Kubernetes API

**Key Attributes**:
- `name` (string, mandatory) - Image name
- `image_tag` (string, optional) - Image tag or version
- `registry_url` (anyURI, optional) - Container registry URL
- `size_mb` (decimal, optional) - Image size in MB
- `lifecycle_status` (enum, mandatory) - Current state

#### Cluster

**Definition**: An orchestration cluster (Kubernetes, Docker Swarm, OpenShift, etc.).

**Framework Source**: Kubernetes API, OpenShift API

**Key Attributes**:
- `name` (string, mandatory) - Cluster name
- `cluster_id` (string, optional) - Unique cluster identifier
- `orchestration_platform` (enum, mandatory) - Platform: kubernetes, openshift, docker_swarm, ecs, aci, none
- `version` (string, optional) - Platform version
- `node_count` (integer, optional) - Number of nodes
- `lifecycle_status` (enum, mandatory) - State: active, degraded, failed, maintenance

#### Namespace

**Definition**: A logical isolation boundary within a cluster.

**Framework Source**: Kubernetes API, OpenShift API

**Key Attributes**:
- `name` (string, mandatory) - Namespace name
- `namespace_id` (string, optional) - Unique namespace identifier
- `resource_quota_cpu` (string, optional) - CPU quota
- `resource_quota_memory` (string, optional) - Memory quota
- `lifecycle_status` (enum, mandatory) - Current state

#### Deployment

**Definition**: A deployment configuration for containers.

**Framework Source**: Kubernetes API

**Key Attributes**:
- `name` (string, mandatory) - Deployment name
- `deployment_id` (string, optional) - Unique deployment identifier
- `replica_count` (integer, optional) - Desired replica count
- `strategy` (enum, optional) - Deployment strategy: rolling_update, recreate, blue_green, canary
- `lifecycle_status` (enum, mandatory) - Current state

#### KubernetesService

**Definition**: A Kubernetes/OpenShift service that exposes pods.

**Framework Source**: Kubernetes API, OpenShift API

**Key Attributes**:
- `name` (string, mandatory) - Service name
- `service_id` (string, optional) - Unique service identifier
- `service_type` (enum, mandatory) - Type: cluster_ip, node_port, load_balancer, external_name
- `port` (integer, optional) - Service port
- `target_port` (integer, optional) - Target pod port
- `lifecycle_status` (enum, mandatory) - Current state

#### Route

**Definition**: An OpenShift route or Kubernetes ingress that exposes services externally.

**Framework Source**: OpenShift API, Kubernetes Ingress API

**Key Attributes**:
- `name` (string, mandatory) - Route name
- `route_id` (string, optional) - Unique route identifier
- `external_hostname` (string, optional) - External DNS name
- `route_path` (string, optional) - URL path
- `tls_termination` (enum, optional) - TLS termination: edge, passthrough, reencrypt, none
- `lifecycle_status` (enum, mandatory) - Current state

#### IngressController

**Definition**: A controller that manages external access to services.

**Framework Source**: Kubernetes Ingress API

**Key Attributes**:
- `name` (string, mandatory) - Ingress controller name
- `controller_type` (enum, mandatory) - Type: nginx, haproxy, traefik, istio, custom
- `lifecycle_status` (enum, mandatory) - Current state

---

### Layer 4: Physical Infrastructure Layer

#### PhysicalServer

**Definition**: A physical server machine.

**Framework Source**: CIM_ComputerSystem, TOGAF Technology Architecture

**Key Attributes**:
- `name` (string, mandatory) - Server name or hostname
- `server_id` (string, optional) - Unique server identifier
- `resource_type` (enum, mandatory) - Type: physical
- `manufacturer` (string, optional) - Server manufacturer
- `model` (string, optional) - Server model
- `serial_number` (string, optional) - Hardware serial number
- `cpu_count` (integer, optional) - Number of CPUs
- `cpu_cores` (integer, optional) - Total CPU cores
- `memory_gb` (decimal, optional) - Total memory in GB
- `location` (string, mandatory) - Datacenter, rack location
- `operating_system` (string, optional) - OS type and version
- `lifecycle_status` (enum, mandatory) - State: provisioning, running, stopped, terminated, maintenance

#### VirtualMachine

**Definition**: A virtualized server instance.

**Framework Source**: CIM_VirtualComputerSystem, VMware API

**Key Attributes**:
- `name` (string, mandatory) - VM name
- `vm_id` (string, optional) - Unique VM identifier
- `resource_type` (enum, mandatory) - Type: virtual
- `vcpu_count` (integer, optional) - Number of virtual CPUs
- `memory_gb` (decimal, optional) - Memory in GB
- `disk_gb` (decimal, optional) - Disk size in GB
- `operating_system` (string, optional) - OS type and version
- `location` (string, mandatory) - Datacenter or region
- `lifecycle_status` (enum, mandatory) - State: provisioning, running, stopped, terminated

#### Hypervisor

**Definition**: A virtualization platform.

**Framework Source**: CIM_VirtualSystemManagementService, VMware API

**Key Attributes**:
- `name` (string, mandatory) - Hypervisor name
- `hypervisor_type` (enum, mandatory) - Type: vmware_esxi, hyper_v, kvm, xen, virtualbox
- `version` (string, optional) - Hypervisor version
- `lifecycle_status` (enum, mandatory) - Current state

#### CloudInstance

**Definition**: A cloud provider compute instance (EC2, Azure VM, GCE).

**Framework Source**: AWS EC2 API, Azure Compute API, GCP Compute Engine API

**Key Attributes**:
- `name` (string, mandatory) - Instance name
- `instance_id` (string, optional) - Cloud instance identifier
- `resource_type` (enum, mandatory) - Type: cloud_iaas
- `cloud_provider` (enum, mandatory) - Provider: aws, azure, gcp, alibaba, oracle, ibm
- `instance_type` (string, optional) - Instance type (e.g., "t3.medium", "Standard_D2s_v3")
- `region` (string, optional) - Cloud region
- `availability_zone` (string, optional) - Availability zone
- `vcpu_count` (integer, optional) - Number of vCPUs
- `memory_gb` (decimal, optional) - Memory in GB
- `operating_system` (string, optional) - OS type and version
- `lifecycle_status` (enum, mandatory) - State: provisioning, running, stopped, terminated

#### CloudService

**Definition**: A managed cloud service (RDS, Lambda, etc.).

**Framework Source**: Cloud Provider APIs

**Key Attributes**:
- `name` (string, mandatory) - Service name
- `service_id` (string, optional) - Cloud service identifier
- `resource_type` (enum, mandatory) - Type: cloud_paas, cloud_saas
- `cloud_provider` (enum, mandatory) - Provider: aws, azure, gcp, alibaba, oracle, ibm
- `service_type` (string, optional) - Service type (e.g., "RDS", "Lambda", "Azure SQL")
- `region` (string, optional) - Cloud region
- `lifecycle_status` (enum, mandatory) - Current state

#### StorageArray

**Definition**: A physical storage system (SAN, NAS).

**Framework Source**: CIM_StorageExtent, CIM Storage Model

**Key Attributes**:
- `name` (string, mandatory) - Storage array name
- `array_id` (string, optional) - Unique array identifier
- `storage_type` (enum, mandatory) - Type: san, nas, das
- `manufacturer` (string, optional) - Storage manufacturer
- `model` (string, optional) - Storage model
- `capacity_tb` (decimal, optional) - Total capacity in TB
- `location` (string, mandatory) - Datacenter location
- `lifecycle_status` (enum, mandatory) - Current state

#### StorageVolume

**Definition**: A logical storage volume or LUN.

**Framework Source**: CIM_StorageExtent

**Key Attributes**:
- `name` (string, mandatory) - Volume name
- `volume_id` (string, optional) - Unique volume identifier
- `capacity_gb` (decimal, optional) - Volume capacity in GB
- `volume_type` (enum, optional) - Type: block, file, object
- `raid_level` (string, optional) - RAID level
- `lifecycle_status` (enum, mandatory) - Current state

#### FileSystem

**Definition**: A mounted file system (NFS, CIFS, ext4, NTFS).

**Framework Source**: CIM_FileSystem

**Key Attributes**:
- `name` (string, mandatory) - Filesystem name
- `filesystem_type` (enum, mandatory) - Type: nfs, cifs, ext4, ntfs, xfs, zfs
- `mount_point` (string, optional) - Mount path
- `capacity_gb` (decimal, optional) - Filesystem capacity in GB
- `lifecycle_status` (enum, mandatory) - Current state

#### StoragePool

**Definition**: A logical grouping of storage resources.

**Framework Source**: CIM_StoragePool

**Key Attributes**:
- `name` (string, mandatory) - Storage pool name
- `pool_id` (string, optional) - Unique pool identifier
- `capacity_tb` (decimal, optional) - Pool capacity in TB
- `lifecycle_status` (enum, mandatory) - Current state

#### CloudStorageService

**Definition**: A managed cloud storage service (RDS instance, EBS volume, Azure Disk).

**Framework Source**: Cloud Provider APIs

**Key Attributes**:
- `name` (string, mandatory) - Storage service name
- `service_id` (string, optional) - Cloud service identifier
- `cloud_provider` (enum, mandatory) - Provider: aws, azure, gcp, alibaba, oracle, ibm
- `storage_type` (string, optional) - Storage type (e.g., "EBS", "Azure Disk", "Persistent Disk")
- `capacity_gb` (decimal, optional) - Storage capacity in GB
- `region` (string, optional) - Cloud region
- `lifecycle_status` (enum, mandatory) - Current state

#### ObjectStorageBucket

**Definition**: A physical object storage bucket (S3, Azure Blob, GCS bucket).

**Framework Source**: Cloud Provider APIs

**Key Attributes**:
- `name` (string, mandatory) - Bucket name
- `bucket_id` (string, optional) - Unique bucket identifier
- `cloud_provider` (enum, mandatory) - Provider: aws, azure, gcp, alibaba, oracle, ibm
- `region` (string, optional) - Cloud region
- `storage_class` (string, optional) - Storage class (e.g., "Standard", "Glacier")
- `lifecycle_status` (enum, mandatory) - Current state

---

### Layer 5: Network Topology and Communication Path Layer

#### NetworkDevice

**Definition**: A network device such as a router, switch, firewall, or gateway.

**Framework Source**: CIM Network Model, TOGAF Technology Architecture

**Key Attributes**:
- `name` (string, mandatory) - Device name or hostname
- `device_id` (string, optional) - Unique device identifier
- `device_type` (enum, mandatory) - Type: router, switch, load_balancer, firewall, gateway, proxy, vpn_gateway
- `manufacturer` (string, optional) - Device manufacturer
- `model` (string, optional) - Device model
- `management_ip` (string, optional) - Management IP address
- `location` (string, mandatory) - Physical or logical location
- `is_virtual` (boolean, optional) - Whether device is virtual
- `throughput_gbps` (decimal, optional) - Maximum throughput in Gbps
- `lifecycle_status` (enum, mandatory) - State: active, inactive, degraded, failed, maintenance

#### LoadBalancer

**Definition**: A load balancing device or service that distributes traffic across multiple targets.

**Framework Source**: CIM Network Model, Cloud Provider APIs

**Key Attributes**:
- `name` (string, mandatory) - Load balancer name
- `lb_id` (string, optional) - Unique load balancer identifier
- `lb_type` (enum, mandatory) - Type: hardware, software, cloud_managed
- `algorithm` (enum, optional) - Algorithm: round_robin, least_connections, ip_hash, weighted
- `port` (integer, optional) - Listening port
- `protocol` (enum, optional) - Protocol: http, https, tcp, udp
- `lifecycle_status` (enum, mandatory) - Current state

#### NetworkInterface

**Definition**: A network interface card or virtual NIC.

**Framework Source**: CIM_NetworkPort

**Key Attributes**:
- `name` (string, mandatory) - Interface name
- `interface_id` (string, optional) - Unique interface identifier
- `mac_address` (string, optional) - MAC address
- `ip_address` (string, optional) - IP address
- `subnet_mask` (string, optional) - Subnet mask
- `speed_mbps` (integer, optional) - Interface speed in Mbps
- `is_virtual` (boolean, optional) - Whether interface is virtual
- `lifecycle_status` (enum, mandatory) - State: active, inactive, degraded, failed

#### NetworkSegment

**Definition**: A network subnet or VLAN.

**Framework Source**: CIM Network Model

**Key Attributes**:
- `name` (string, mandatory) - Segment name
- `segment_id` (string, optional) - Unique segment identifier
- `segment_type` (enum, mandatory) - Type: subnet, vlan, vpc, vnet
- `cidr_block` (string, optional) - CIDR notation (e.g., "10.0.1.0/24")
- `vlan_id` (integer, optional) - VLAN identifier
- `gateway_ip` (string, optional) - Default gateway IP
- `lifecycle_status` (enum, mandatory) - Current state

#### CommunicationPath

**Definition**: A logical communication path between components.

**Framework Source**: CIM_NetworkPipe

**Key Attributes**:
- `name` (string, mandatory) - Path name
- `path_id` (string, optional) - Unique path identifier
- `protocol` (enum, mandatory) - Protocol: tcp, udp, http, https, grpc, amqp, mqtt
- `source_port` (integer, optional) - Source port
- `destination_port` (integer, optional) - Destination port
- `bandwidth_mbps` (integer, optional) - Bandwidth in Mbps
- `latency_ms` (decimal, optional) - Latency in milliseconds
- `lifecycle_status` (enum, mandatory) - State: active, inactive, degraded, failed

#### NetworkRoute

**Definition**: A routing rule or path.

**Framework Source**: CIM Network Model

**Key Attributes**:
- `name` (string, mandatory) - Route name
- `route_id` (string, optional) - Unique route identifier
- `destination_cidr` (string, optional) - Destination CIDR block
- `next_hop` (string, optional) - Next hop IP or gateway
- `metric` (integer, optional) - Route metric or priority
- `lifecycle_status` (enum, mandatory) - Current state

---

### Layer 6: Security Infrastructure Layer

#### Firewall

**Definition**: A network firewall device or service.

**Framework Source**: CIM_SecurityService, NIST Cybersecurity Framework

**Key Attributes**:
- `name` (string, mandatory) - Firewall name
- `firewall_id` (string, optional) - Unique firewall identifier
- `security_type` (enum, mandatory) - Type: firewall
- `firewall_type` (enum, mandatory) - Firewall type: network, host_based, cloud_managed, waf
- `rule_count` (integer, optional) - Number of firewall rules
- `location` (string, optional) - Physical or logical location
- `lifecycle_status` (enum, mandatory) - State: active, expired, revoked, disabled

#### WAF

**Definition**: A web application firewall.

**Framework Source**: NIST Cybersecurity Framework

**Key Attributes**:
- `name` (string, mandatory) - WAF name
- `waf_id` (string, optional) - Unique WAF identifier
- `security_type` (enum, mandatory) - Type: waf
- `waf_type` (enum, mandatory) - WAF type: cloud_managed, on_premises, hybrid
- `rule_set` (string, optional) - Rule set or policy name
- `lifecycle_status` (enum, mandatory) - Current state

#### Certificate

**Definition**: A digital certificate.

**Framework Source**: X.509 Standard, PKI Standards

**Key Attributes**:
- `name` (string, mandatory) - Certificate name or common name
- `certificate_id` (string, optional) - Unique certificate identifier
- `security_type` (enum, mandatory) - Type: certificate
- `certificate_type` (enum, mandatory) - Certificate type: ssl_tls, code_signing, client_auth, server_auth
- `subject` (string, optional) - Certificate subject
- `issuer` (string, optional) - Certificate issuer
- `serial_number` (string, optional) - Certificate serial number
- `valid_from` (date, optional) - Validity start date
- `valid_to` (date, optional) - Validity end date
- `key_size` (integer, optional) - Key size in bits
- `lifecycle_status` (enum, mandatory) - State: active, expired, revoked, disabled

#### CertificateAuthority

**Definition**: A certificate authority that issues certificates.

**Framework Source**: X.509 Standard, PKI Standards

**Key Attributes**:
- `name` (string, mandatory) - CA name
- `ca_id` (string, optional) - Unique CA identifier
- `security_type` (enum, mandatory) - Type: certificate
- `ca_type` (enum, mandatory) - CA type: root, intermediate, subordinate
- `lifecycle_status` (enum, mandatory) - Current state

#### SecurityPolicy

**Definition**: A security policy or rule set.

**Framework Source**: NIST Cybersecurity Framework

**Key Attributes**:
- `name` (string, mandatory) - Policy name
- `policy_id` (string, optional) - Unique policy identifier
- `security_type` (enum, mandatory) - Type: policy
- `policy_type` (enum, mandatory) - Policy type: access_control, encryption, authentication, authorization, audit
- `policy_rules` (string, optional) - Policy rules or configuration
- `lifecycle_status` (enum, mandatory) - Current state

#### IdentityProvider

**Definition**: An authentication/authorization service.

**Framework Source**: NIST Cybersecurity Framework

**Key Attributes**:
- `name` (string, mandatory) - Identity provider name
- `idp_id` (string, optional) - Unique IdP identifier
- `security_type` (enum, mandatory) - Type: iam
- `idp_type` (enum, mandatory) - IdP type: ldap, active_directory, saml, oauth2, oidc
- `endpoint_url` (anyURI, optional) - IdP endpoint URL
- `lifecycle_status` (enum, mandatory) - Current state

#### SecurityZone

**Definition**: A security boundary or trust zone.

**Framework Source**: NIST Cybersecurity Framework

**Key Attributes**:
- `name` (string, mandatory) - Security zone name
- `zone_id` (string, optional) - Unique zone identifier
- `security_type` (enum, mandatory) - Type: policy
- `trust_level` (enum, mandatory) - Trust level: trusted, untrusted, dmz, restricted
- `zone_type` (enum, optional) - Zone type: internal, external, dmz, management
- `lifecycle_status` (enum, mandatory) - Current state

---

## Relationship Types

### Intra-Layer Relationships

These relationships connect entities within the same layer.

#### part_of / contains

**Domain**: Any entity type  
**Range**: Any entity type (same layer)  
**Inverse**: `contains` / `part_of`  
**Cardinality**: Many-to-One  
**Description**: Hierarchical composition relationship

**Example**:
```turtle
:CustomerServlet :part_of :CRMApplication .
:CRMApplication :contains :CustomerServlet .
```

#### enables / enabled_by

**Domain**: BusinessCapability  
**Range**: BusinessProcess  
**Inverse**: `enabled_by` / `enables`  
**Cardinality**: Many-to-Many  
**Description**: Capability enablement relationship

**Example**:
```turtle
:OrderManagementCapability :enables :OrderFulfillmentProcess .
```

#### supports / supported_by

**Domain**: BusinessService, Application  
**Range**: BusinessProcess, Application  
**Inverse**: `supported_by` / `supports`  
**Cardinality**: Many-to-Many  
**Description**: Service support relationship

**Example**:
```turtle
:PaymentService :supports :OrderFulfillmentProcess .
```

#### connected_to

**Domain**: NetworkDevice, NetworkInterface  
**Range**: NetworkDevice, NetworkInterface  
**Inverse**: `connected_to` (symmetric)  
**Cardinality**: Many-to-Many  
**Description**: Physical or logical network connection

**Example**:
```turtle
:Router01 :connected_to :Switch01 .
```

#### issued_by / issues

**Domain**: Certificate  
**Range**: CertificateAuthority  
**Inverse**: `issues` / `issued_by`  
**Cardinality**: Many-to-One  
**Description**: Certificate issuance relationship

**Example**:
```turtle
:WebServerCert :issued_by :InternalCA .
```

---

### Cross-Layer Relationships

These relationships connect entities across different layers.

#### realized_by / realizes

**Domain**: BusinessProcess, BusinessService  
**Range**: Application, Service  
**Inverse**: `realizes` / `realized_by`  
**Cardinality**: Many-to-Many  
**Description**: Business process realization by applications

**Example**:
```turtle
:OrderFulfillmentProcess :realized_by :OrderManagementSystem .
```

#### requires

**Domain**: BusinessProcess, BusinessCapability  
**Range**: Application, Service  
**Inverse**: None  
**Cardinality**: Many-to-Many  
**Description**: Business requirement for applications

**Example**:
```turtle
:CustomerManagement :requires :CRMApplication .
```

#### deployed_as / deploys

**Domain**: Application, ApplicationComponent  
**Range**: Container, Pod  
**Inverse**: `deploys` / `deployed_as`  
**Cardinality**: One-to-Many  
**Description**: Application deployment as containers

**Example**:
```turtle
:OrderService :deployed_as :OrderServiceContainer .
```

#### packaged_in / packages

**Domain**: Application, ApplicationComponent  
**Range**: Container, ContainerImage  
**Inverse**: `packages` / `packaged_in`  
**Cardinality**: Many-to-One  
**Description**: Application packaging in containers

**Example**:
```turtle
:OrderService :packaged_in :OrderServiceImage .
```

#### runs_on / hosts

**Domain**: Application, Container, Pod, VirtualMachine  
**Range**: VirtualMachine, PhysicalServer, Hypervisor, CloudInstance  
**Inverse**: `hosts` / `runs_on`  
**Cardinality**: Many-to-One  
**Description**: Execution on infrastructure

**Example**:
```turtle
:OrderServicePod :runs_on :K8sWorkerNode01 .
:K8sWorkerNode01 :hosts :OrderServicePod .
```

#### hosted_on

**Domain**: Database, ApplicationServer  
**Range**: VirtualMachine, PhysicalServer, CloudInstance, CloudService  
**Inverse**: `hosts`  
**Cardinality**: Many-to-One  
**Description**: Database or application server hosting

**Example**:
```turtle
:OrderDB :hosted_on :DatabaseServer01 .
```

#### uses

**Domain**: Application, Service, Container, Pod  
**Range**: Database, API, MessageQueue, CacheService, FileStorageService, ObjectStorageService, PersistentVolumeClaim  
**Inverse**: `used_by`  
**Cardinality**: Many-to-Many  
**Description**: Resource usage relationship

**Example**:
```turtle
:OrderService :uses :OrderDB .
:OrderService :uses :PaymentAPI .
```

#### calls

**Domain**: Service, API, Application  
**Range**: Service, API  
**Inverse**: `called_by`  
**Cardinality**: Many-to-Many  
**Description**: Service-to-service communication

**Example**:
```turtle
:OrderService :calls :PaymentService .
```

#### communicates_via

**Domain**: Application, Service, Container  
**Range**: CommunicationPath, NetworkSegment  
**Inverse**: None  
**Cardinality**: Many-to-Many  
**Description**: Communication path usage

**Example**:
```turtle
:OrderService :communicates_via :HTTPSPath .
```

#### routes_through

**Domain**: CommunicationPath  
**Range**: NetworkDevice, LoadBalancer  
**Inverse**: None  
**Cardinality**: Many-to-Many  
**Description**: Network routing

**Example**:
```turtle
:HTTPSPath :routes_through :LoadBalancer01 .
```

#### protected_by / protects

**Domain**: Any entity type  
**Range**: Firewall, WAF, SecurityPolicy, SecurityZone  
**Inverse**: `protects` / `protected_by`  
**Cardinality**: Many-to-Many  
**Description**: Security protection relationship

**Example**:
```turtle
:OrderService :protected_by :WebAppFirewall .
```

#### secured_by / secures

**Domain**: Any entity type  
**Range**: Certificate, SecurityPolicy, IdentityProvider  
**Inverse**: `secures` / `secured_by`  
**Cardinality**: Many-to-Many  
**Description**: Security policy application

**Example**:
```turtle
:OrderServiceAPI :secured_by :APIGatewayCert .
```

#### stored_on / stores

**Domain**: Database, DatabaseInstance, FileStorageService  
**Range**: StorageVolume, FileSystem, CloudStorageService  
**Inverse**: `stores` / `stored_on`  
**Cardinality**: Many-to-One  
**Description**: Data storage location

**Example**:
```turtle
:OrderDB :stored_on :SAN_Volume_123 .
```

#### stored_in

**Domain**: ObjectStorageService  
**Range**: ObjectStorageBucket  
**Inverse**: None  
**Cardinality**: Many-to-One  
**Description**: Object storage location

**Example**:
```turtle
:DocumentStorage :stored_in :S3_Bucket_Documents .
```

#### allocated_from

**Domain**: StorageVolume  
**Range**: StorageArray, StoragePool  
**Inverse**: `allocates`  
**Cardinality**: Many-to-One  
**Description**: Storage allocation

**Example**:
```turtle
:Volume_123 :allocated_from :NetApp_SAN_01 .
```

#### mounted_from

**Domain**: FileSystem  
**Range**: StorageVolume  
**Inverse**: None  
**Cardinality**: Many-to-One  
**Description**: Filesystem mount

**Example**:
```turtle
:NFSMount_Media :mounted_from :NFS_Volume_456 .
```

#### attached_to

**Domain**: NetworkInterface, StorageVolume  
**Range**: PhysicalServer, VirtualMachine, CloudInstance  
**Inverse**: None  
**Cardinality**: Many-to-One  
**Description**: Hardware attachment

**Example**:
```turtle
:eth0 :attached_to :WebServer01 .
```

#### exposes

**Domain**: KubernetesService, Route  
**Range**: Pod, Deployment  
**Inverse**: `exposed_by`  
**Cardinality**: Many-to-Many  
**Description**: Service exposure

**Example**:
```turtle
:OrderServiceK8s :exposes :OrderServicePod .
```

#### routes_to

**Domain**: Route, IngressController  
**Range**: KubernetesService  
**Inverse**: None  
**Cardinality**: Many-to-One  
**Description**: Traffic routing

**Example**:
```turtle
:OrderServiceRoute :routes_to :OrderServiceK8s .
```

#### runs_in

**Domain**: Pod, Deployment  
**Range**: Namespace, Cluster  
**Inverse**: None  
**Cardinality**: Many-to-One  
**Description**: Namespace or cluster membership

**Example**:
```turtle
:OrderServicePod :runs_in :ProductionNamespace .
```

#### uses_image

**Domain**: Container, Pod  
**Range**: ContainerImage  
**Inverse**: None  
**Cardinality**: Many-to-One  
**Description**: Container image usage

**Example**:
```turtle
:OrderServiceContainer :uses_image :OrderServiceImage_v1_2 .
```

---

## Data Properties (Attributes)

### Common Attributes

These attributes are applicable across multiple entity types.

| Property | Data Type | Cardinality | Description | Framework Source |
|----------|-----------|-------------|-------------|------------------|
| `name` | xsd:string | 1..1 | Entity name or identifier | All frameworks |
| `description` | xsd:string | 0..1 | Detailed description | All frameworks |
| `owner` | xsd:string | 0..1 | Owner or responsible party | TOGAF, ITIL |
| `criticality` | xsd:string | 0..1 | Importance level: critical, high, medium, low | TOGAF, ITIL |
| `lifecycle_status` | xsd:string | 1..1 | Current operational state | All frameworks |
| `version` | xsd:string | 0..1 | Version identifier | All frameworks |
| `location` | xsd:string | 0..1 | Physical or logical location | CIM, TOGAF |
| `created_date` | xsd:date | 0..1 | Creation date | All frameworks |
| `modified_date` | xsd:date | 0..1 | Last modification date | All frameworks |

---

### Layer 1: Business Process Layer Attributes

| Property | Data Type | Cardinality | Description | Framework Source |
|----------|-----------|-------------|-------------|------------------|
| `process_type` | xsd:string | 1..1 | Process type: core, supporting, management | TOGAF |
| `frequency` | xsd:string | 0..1 | Execution frequency: real-time, hourly, daily, weekly, monthly, quarterly, annual, on-demand | TOGAF |
| `maturity_level` | xsd:string | 0..1 | Process maturity: initial, developing, defined, managed, optimizing | TOGAF |
| `capability_level` | xsd:string | 1..1 | Capability maturity level | TOGAF |
| `service_level` | xsd:string | 0..1 | Service level agreement or target | ITIL |
| `product_type` | xsd:string | 1..1 | Product type: physical, digital, service, hybrid | TOGAF |

---

### Layer 2: Application Layer Attributes

| Property | Data Type | Cardinality | Description | Framework Source |
|----------|-----------|-------------|-------------|------------------|
| `application_type` | xsd:string | 1..1 | Architecture pattern: monolithic, SOA_service, microservice, batch, legacy | TOGAF |
| `deployment_model` | xsd:string | 1..1 | Deployment type: containerized, vm_based, bare_metal, serverless | TOGAF, Cloud APIs |
| `runtime_environment` | xsd:string | 0..1 | Runtime (e.g., "WebSphere", "Tomcat", "Node.js") | CIM |
| `technology_stack` | xsd:string | 0..1 | Technologies (e.g., "Java EE", ".NET", "Python") | TOGAF |
| `data_classification` | xsd:string | 0..1 | Data sensitivity: public, internal, confidential, restricted | NIST |
| `component_type` | xsd:string | 1..1 | Component type: servlet, ejb, web_service, rest_api, batch_job, scheduled_task | TOGAF |
| `server_type` | xsd:string | 1..1 | Server type: websphere, weblogic, jboss, tomcat, iis, apache, nginx | CIM |
| `port` | xsd:integer | 0..1 | Network port number | CIM |
| `service_type` | xsd:string | 1..1 | Service type: rest, soap, grpc, graphql, messaging | TOGAF |
| `endpoint_url` | xsd:anyURI | 0..1 | Service or API endpoint URL | TOGAF |
| `api_type` | xsd:string | 1..1 | API type: rest, soap, graphql, grpc, websocket | TOGAF |
| `authentication_type` | xsd:string | 0..1 | Auth type: none, basic, oauth2, api_key, jwt | NIST |
| `database_type` | xsd:string | 1..1 | Database type: relational, nosql_document, nosql_keyvalue, nosql_graph, nosql_columnar, timeseries | CIM |
| `database_engine` | xsd:string | 0..1 | Database engine (e.g., "Oracle", "PostgreSQL", "MongoDB") | CIM |
| `instance_id` | xsd:string | 0..1 | Unique instance identifier | CIM |
| `size_gb` | xsd:decimal | 0..1 | Database size in GB | CIM |
| `object_type` | xsd:string | 1..1 | Data object type: table, view, collection, document, schema | TOGAF |
| `queue_type` | xsd:string | 1..1 | Queue type: point_to_point, publish_subscribe, streaming | TOGAF |
| `queue_engine` | xsd:string | 0..1 | Queue engine (e.g., "RabbitMQ", "Kafka", "IBM MQ") | TOGAF |
| `cache_type` | xsd:string | 1..1 | Cache type: in_memory, distributed, cdn | TOGAF |
| `cache_engine` | xsd:string | 0..1 | Cache engine (e.g., "Redis", "Memcached") | TOGAF |
| `storage_type` | xsd:string | 1..1 | Storage type: nfs, cifs, local, cloud_file, s3, azure_blob, gcs, object_storage | CIM, Cloud APIs |
| `mount_path` | xsd:string | 0..1 | Mount point or path | CIM |
| `capacity_gb` | xsd:decimal | 0..1 | Storage capacity in GB | CIM |
| `bucket_name` | xsd:string | 0..1 | Bucket or container name | Cloud APIs |
| `region` | xsd:string | 0..1 | Cloud region | Cloud APIs |

---

### Layer 3: Container and Orchestration Layer Attributes

| Property | Data Type | Cardinality | Description | Framework Source |
|----------|-----------|-------------|-------------|------------------|
| `container_id` | xsd:string | 0..1 | Unique container identifier | Kubernetes API |
| `image_name` | xsd:string | 0..1 | Container image reference | Kubernetes API |
| `image_tag` | xsd:string | 0..1 | Image tag or version | Kubernetes API |
| `resource_limits_cpu` | xsd:string | 0..1 | CPU limits | Kubernetes API |
| `resource_limits_memory` | xsd:string | 0..1 | Memory limits | Kubernetes API |
| `pod_id` | xsd:string | 0..1 | Unique pod identifier | Kubernetes API |
| `replica_count` | xsd:integer | 0..1 | Number of replicas | Kubernetes API |
| `restart_policy` | xsd:string | 0..1 | Restart policy: always, on_failure, never | Kubernetes API |
| `registry_url` | xsd:anyURI | 0..1 | Container registry URL | Kubernetes API |
| `size_mb` | xsd:decimal | 0..1 | Image size in MB | Kubernetes API |
| `cluster_id` | xsd:string | 0..1 | Unique cluster identifier | Kubernetes API |
| `orchestration_platform` | xsd:string | 1..1 | Platform: kubernetes, openshift, docker_swarm, ecs, aci, none | Kubernetes API, Cloud APIs |
| `node_count` | xsd:integer | 0..1 | Number of nodes | Kubernetes API |
| `namespace_id` | xsd:string | 0..1 | Unique namespace identifier | Kubernetes API |
| `resource_quota_cpu` | xsd:string | 0..1 | CPU quota | Kubernetes API |
| `resource_quota_memory` | xsd:string | 0..1 | Memory quota | Kubernetes API |
| `deployment_id` | xsd:string | 0..1 | Unique deployment identifier | Kubernetes API |
| `strategy` | xsd:string | 0..1 | Deployment strategy: rolling_update, recreate, blue_green, canary | Kubernetes API |
| `service_id` | xsd:string | 0..1 | Unique service identifier | Kubernetes API |
| `service_type` | xsd:string | 1..1 | Service type: cluster_ip, node_port, load_balancer, external_name | Kubernetes API |
| `target_port` | xsd:integer | 0..1 | Target pod port | Kubernetes API |
| `route_id` | xsd:string | 0..1 | Unique route identifier | OpenShift API |
| `external_hostname` | xsd:string | 0..1 | External DNS name | OpenShift API |
| `route_path` | xsd:string | 0..1 | URL path | OpenShift API |
| `tls_termination` | xsd:string | 0..1 | TLS termination: edge, passthrough, reencrypt, none | OpenShift API |
| `controller_type` | xsd:string | 1..1 | Controller type: nginx, haproxy, traefik, istio, custom | Kubernetes API |

---

### Layer 4: Physical Infrastructure Layer Attributes

| Property | Data Type | Cardinality | Description | Framework Source |
|----------|-----------|-------------|-------------|------------------|
| `server_id` | xsd:string | 0..1 | Unique server identifier | CIM |
| `resource_type` | xsd:string | 1..1 | Resource type: physical, virtual, cloud_iaas, cloud_paas, cloud_saas | CIM, Cloud APIs |
| `manufacturer` | xsd:string | 0..1 | Hardware manufacturer | CIM |
| `model` | xsd:string | 0..1 | Hardware model | CIM |
| `serial_number` | xsd:string | 0..1 | Hardware serial number | CIM |
| `cpu_count` | xsd:integer | 0..1 | Number of CPUs | CIM |
| `cpu_cores` | xsd:integer | 0..1 | Total CPU cores | CIM |
| `memory_gb` | xsd:decimal | 0..1 | Memory in GB | CIM |
| `operating_system` | xsd:string | 0..1 | OS type and version | CIM |
| `vm_id` | xsd:string | 0..1 | Unique VM identifier | CIM |
| `vcpu_count` | xsd:integer | 0..1 | Number of virtual CPUs | CIM |
| `disk_gb` | xsd:decimal | 0..1 | Disk size in GB | CIM |
| `hypervisor_type` | xsd:string | 1..1 | Hypervisor type: vmware_esxi, hyper_v, kvm, xen, virtualbox | CIM, VMware API |
| `instance_id` | xsd:string | 0..1 | Cloud instance identifier | Cloud APIs |
| `cloud_provider` | xsd:string | 1..1 | Cloud provider: aws, azure, gcp, alibaba, oracle, ibm | Cloud APIs |
| `instance_type` | xsd:string | 0..1 | Instance type (e.g., "t3.medium", "Standard_D2s_v3") | Cloud APIs |
| `availability_zone` | xsd:string | 0..1 | Availability zone | Cloud APIs |
| `service_id` | xsd:string | 0..1 | Cloud service identifier | Cloud APIs |
| `service_type` | xsd:string | 0..1 | Service type (e.g., "RDS", "Lambda", "Azure SQL") | Cloud APIs |
| `array_id` | xsd:string | 0..1 | Unique array identifier | CIM |
| `capacity_tb` | xsd:decimal | 0..1 | Storage capacity in TB | CIM |
| `volume_id` | xsd:string | 0..1 | Unique volume identifier | CIM |
| `volume_type` | xsd:string | 0..1 | Volume type: block, file, object | CIM |
| `raid_level` | xsd:string | 0..1 | RAID level | CIM |
| `filesystem_type` | xsd:string | 1..1 | Filesystem type: nfs, cifs, ext4, ntfs, xfs, zfs | CIM |
| `mount_point` | xsd:string | 0..1 | Mount path | CIM |
| `pool_id` | xsd:string | 0..1 | Unique pool identifier | CIM |
| `bucket_id` | xsd:string | 0..1 | Unique bucket identifier | Cloud APIs |
| `storage_class` | xsd:string | 0..1 | Storage class (e.g., "Standard", "Glacier") | Cloud APIs |

---

### Layer 5: Network Topology Layer Attributes

| Property | Data Type | Cardinality | Description | Framework Source |
|----------|-----------|-------------|-------------|------------------|
| `device_id` | xsd:string | 0..1 | Unique device identifier | CIM |
| `device_type` | xsd:string | 1..1 | Device type: router, switch, load_balancer, firewall, gateway, proxy, vpn_gateway | CIM |
| `firmware_version` | xsd:string | 0..1 | Firmware or OS version | CIM |
| `management_ip` | xsd:string | 0..1 | Management IP address | CIM |
| `is_virtual` | xsd:boolean | 0..1 | Whether device is virtual | CIM |
| `port_count` | xsd:integer | 0..1 | Number of network ports | CIM |
| `throughput_gbps` | xsd:decimal | 0..1 | Maximum throughput in Gbps | CIM |
| `lb_id` | xsd:string | 0..1 | Unique load balancer identifier | CIM, Cloud APIs |
| `lb_type` | xsd:string | 1..1 | Load balancer type: hardware, software, cloud_managed | CIM, Cloud APIs |
| `algorithm` | xsd:string | 0..1 | Algorithm: round_robin, least_connections, ip_hash, weighted | CIM |
| `protocol` | xsd:string | 0..1 | Protocol: http, https, tcp, udp, grpc, amqp, mqtt | CIM |
| `interface_id` | xsd:string | 0..1 | Unique interface identifier | CIM |
| `mac_address` | xsd:string | 0..1 | MAC address | CIM |
| `ip_address` | xsd:string | 0..1 | IP address | CIM |
| `subnet_mask` | xsd:string | 0..1 | Subnet mask | CIM |
| `speed_mbps` | xsd:integer | 0..1 | Interface speed in Mbps | CIM |
| `segment_id` | xsd:string | 0..1 | Unique segment identifier | CIM |
| `segment_type` | xsd:string | 1..1 | Segment type: subnet, vlan, vpc, vnet | CIM, Cloud APIs |
| `cidr_block` | xsd:string | 0..1 | CIDR notation (e.g., "10.0.1.0/24") | CIM |
| `vlan_id` | xsd:integer | 0..1 | VLAN identifier | CIM |
| `gateway_ip` | xsd:string | 0..1 | Default gateway IP | CIM |
| `path_id` | xsd:string | 0..1 | Unique path identifier | CIM |
| `source_port` | xsd:integer | 0..1 | Source port | CIM |
| `destination_port` | xsd:integer | 0..1 | Destination port | CIM |
| `bandwidth_mbps` | xsd:integer | 0..1 | Bandwidth in Mbps | CIM |
| `latency_ms` | xsd:decimal | 0..1 | Latency in milliseconds | CIM |
| `route_id` | xsd:string | 0..1 | Unique route identifier | CIM |
| `destination_cidr` | xsd:string | 0..1 | Destination CIDR block | CIM |
| `next_hop` | xsd:string | 0..1 | Next hop IP or gateway | CIM |
| `metric` | xsd:integer | 0..1 | Route metric or priority | CIM |

---

### Layer 6: Security Infrastructure Layer Attributes

| Property | Data Type | Cardinality | Description | Framework Source |
|----------|-----------|-------------|-------------|------------------|
| `firewall_id` | xsd:string | 0..1 | Unique firewall identifier | CIM, NIST |
| `security_type` | xsd:string | 1..1 | Security type: firewall, waf, certificate, policy, iam | NIST |
| `firewall_type` | xsd:string | 1..1 | Firewall type: network, host_based, cloud_managed, waf | NIST |
| `rule_count` | xsd:integer | 0..1 | Number of firewall rules | NIST |
| `waf_id` | xsd:string | 0..1 | Unique WAF identifier | NIST |
| `waf_type` | xsd:string | 1..1 | WAF type: cloud_managed, on_premises, hybrid | NIST |
| `rule_set` | xsd:string | 0..1 | Rule set or policy name | NIST |
| `certificate_id` | xsd:string | 0..1 | Unique certificate identifier | X.509 |
| `certificate_type` | xsd:string | 1..1 | Certificate type: ssl_tls, code_signing, client_auth, server_auth | X.509 |
| `subject` | xsd:string | 0..1 | Certificate subject | X.509 |
| `issuer` | xsd:string | 0..1 | Certificate issuer | X.509 |
| `valid_from` | xsd:date | 0..1 | Validity start date | X.509 |
| `valid_to` | xsd:date | 0..1 | Validity end date | X.509 |
| `key_size` | xsd:integer | 0..1 | Key size in bits | X.509 |
| `ca_id` | xsd:string | 0..1 | Unique CA identifier | X.509 |
| `ca_type` | xsd:string | 1..1 | CA type: root, intermediate, subordinate | X.509 |
| `policy_id` | xsd:string | 0..1 | Unique policy identifier | NIST |
| `policy_type` | xsd:string | 1..1 | Policy type: access_control, encryption, authentication, authorization, audit | NIST |
| `policy_rules` | xsd:string | 0..1 | Policy rules or configuration | NIST |
| `idp_id` | xsd:string | 0..1 | Unique IdP identifier | NIST |
| `idp_type` | xsd:string | 1..1 | IdP type: ldap, active_directory, saml, oauth2, oidc | NIST |
| `zone_id` | xsd:string | 0..1 | Unique zone identifier | NIST |
| `trust_level` | xsd:string | 1..1 | Trust level: trusted, untrusted, dmz, restricted | NIST |
| `zone_type` | xsd:string | 0..1 | Zone type: internal, external, dmz, management | NIST |

---

## Framework Mappings

### TOGAF Framework Mapping

| Ontology Layer | TOGAF Layer | TOGAF Elements | Mapped Entity Types |
|----------------|-------------|----------------|---------------------|
| Layer 1: Business Processes | Business Architecture | Business Process, Business Service, Business Capability, Product | BusinessProcess, BusinessCapability, BusinessService, Product |
| Layer 2: Application Layer | Application Architecture | Application Component, Data Entity, Application Service, Application Interface | Application, ApplicationComponent, Service, API, Database, DataObject |
| Layer 3: Container & Orchestration | Technology Architecture | Platform Services (partial) | Container, Pod, Cluster |
| Layer 4: Physical Infrastructure | Technology Architecture | Platform Services, Physical Technology Components | PhysicalServer, VirtualMachine, StorageArray, CloudInstance |
| Layer 5: Network Topology | Technology Architecture | Communication Infrastructure | NetworkDevice, LoadBalancer, NetworkSegment |
| Layer 6: Security Infrastructure | Security Architecture | Security Services, Security Policies | Firewall, Certificate, SecurityPolicy |

### CIM (Common Information Model) Mapping

| Ontology Entity Type | CIM Class | CIM Namespace |
|----------------------|-----------|---------------|
| Application | CIM_ApplicationSystem | CIM_Application |
| Database | CIM_DatabaseSystem | CIM_Database |
| PhysicalServer | CIM_ComputerSystem | CIM_Core |
| VirtualMachine | CIM_VirtualComputerSystem | CIM_Virtualization |
| Hypervisor | CIM_VirtualSystemManagementService | CIM_Virtualization |
| StorageArray | CIM_StorageExtent | CIM_Storage |
| StorageVolume | CIM_StorageExtent | CIM_Storage |
| FileSystem | CIM_FileSystem | CIM_Storage |
| StoragePool | CIM_StoragePool | CIM_Storage |
| NetworkDevice | CIM_NetworkDevice | CIM_Network |
| NetworkInterface | CIM_NetworkPort | CIM_Network |
| LoadBalancer | CIM_NetworkService | CIM_Network |
| NetworkSegment | CIM_NetworkSegment | CIM_Network |
| CommunicationPath | CIM_NetworkPipe | CIM_Network |
| Firewall | CIM_SecurityService | CIM_Security |
| Container | CIM_Container | CIM_Virtualization |

### ITIL Process Mapping

| Ontology Layer | ITIL Process Area | ITIL Concepts |
|----------------|-------------------|---------------|
| Layer 1: Business Processes | Service Strategy, Service Design | Business Service, Service Level Management |
| Layer 2: Application Layer | Application Management, Service Design | Application, Configuration Item |
| Layer 3: Container & Orchestration | Technical Management | Technical Service |
| Layer 4: Physical Infrastructure | Technical Management, Capacity Management | Server, Storage, Configuration Item |
| Layer 5: Network Topology | Technical Management, Network Management | Network Device, Network Service |
| Layer 6: Security Infrastructure | Information Security Management | Security Control, Security Policy |

### ArchiMate Mapping

| Ontology Layer | ArchiMate Layer | ArchiMate Elements |
|----------------|-----------------|-------------------|
| Layer 1: Business Processes | Business Layer | Business Process, Business Service, Business Capability, Product |
| Layer 2: Application Layer | Application Layer | Application Component, Application Service, Data Object |
| Layer 3: Container & Orchestration | Technology Layer | System Software (partial) |
| Layer 4: Physical Infrastructure | Technology Layer | Node, Device, System Software |
| Layer 5: Network Topology | Technology Layer | Communication Network, Path |
| Layer 6: Security Infrastructure | Technology Layer (cross-cutting) | Security Service |

### Kubernetes API Mapping

| Ontology Entity Type | Kubernetes Resource | API Group |
|----------------------|---------------------|-----------|
| Container | Container | core/v1 |
| Pod | Pod | core/v1 |
| ContainerImage | Image | core/v1 |
| Cluster | Cluster | N/A (cluster-level) |
| Namespace | Namespace | core/v1 |
| Deployment | Deployment | apps/v1 |
| KubernetesService | Service | core/v1 |
| Route | Ingress | networking.k8s.io/v1 |
| IngressController | IngressController | networking.k8s.io/v1 |

### OpenShift API Mapping

| Ontology Entity Type | OpenShift Resource | API Group |
|----------------------|--------------------|-----------|
| Route | Route | route.openshift.io/v1 |
| Deployment | DeploymentConfig | apps.openshift.io/v1 |
| Cluster | Cluster | config.openshift.io/v1 |

### Cloud Provider API Mapping

#### AWS

| Ontology Entity Type | AWS Service/Resource | AWS API |
|----------------------|----------------------|---------|
| CloudInstance | EC2 Instance | EC2 API |
| CloudService | RDS, Lambda, ECS, etc. | Various APIs |
| CloudStorageService | EBS Volume, RDS Storage | EBS API, RDS API |
| ObjectStorageBucket | S3 Bucket | S3 API |
| NetworkSegment | VPC Subnet | VPC API |
| LoadBalancer | ELB, ALB, NLB | ELB API |

#### Azure

| Ontology Entity Type | Azure Service/Resource | Azure API |
|----------------------|------------------------|-----------|
| CloudInstance | Virtual Machine | Compute API |
| CloudService | Azure SQL, Functions, AKS, etc. | Various APIs |
| CloudStorageService | Managed Disk, Azure SQL Storage | Disk API, SQL API |
| ObjectStorageBucket | Blob Container | Blob Storage API |
| NetworkSegment | Virtual Network Subnet | Network API |
| LoadBalancer | Load Balancer, Application Gateway | Network API |

#### GCP

| Ontology Entity Type | GCP Service/Resource | GCP API |
|----------------------|----------------------|---------|
| CloudInstance | Compute Engine Instance | Compute Engine API |
| CloudService | Cloud SQL, Cloud Functions, GKE, etc. | Various APIs |
| CloudStorageService | Persistent Disk, Cloud SQL Storage | Compute API, SQL API |
| ObjectStorageBucket | Cloud Storage Bucket | Cloud Storage API |
| NetworkSegment | VPC Subnet | VPC API |
| LoadBalancer | Cloud Load Balancing | Load Balancing API |

### Security Framework Mapping

| Ontology Entity Type | NIST CSF Function | X.509/PKI Standard |
|----------------------|-------------------|-------------------|
| Firewall | Protect | N/A |
| WAF | Protect, Detect | N/A |
| Certificate | Protect | X.509 Certificate |
| CertificateAuthority | Protect | X.509 CA |
| SecurityPolicy | Protect | N/A |
| IdentityProvider | Protect | N/A |
| SecurityZone | Protect | N/A |

---

## Validation Rules

### SHACL Validation Shapes

The ontology includes comprehensive SHACL validation shapes to ensure data quality and consistency.

#### Mandatory Attribute Validation

All entity instances must have required attributes:

```turtle
:ApplicationShape
  a sh:NodeShape ;
  sh:targetClass :Application ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
    sh:message "Application must have exactly one name" ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "Application must have exactly one lifecycle_status" ;
  ] .
```

#### Enumeration Validation

Enumerated attributes must use defined values:

```turtle
:ApplicationShape
  sh:property [
    sh:path :application_type ;
    sh:minCount 1 ;
    sh:in ( "monolithic" "SOA_service" "microservice" "batch" "legacy" ) ;
    sh:message "application_type must be one of: monolithic, SOA_service, microservice, batch, legacy" ;
  ] ;
  sh:property [
    sh:path :deployment_model ;
    sh:minCount 1 ;
    sh:in ( "containerized" "vm_based" "bare_metal" "serverless" ) ;
    sh:message "deployment_model must be one of: containerized, vm_based, bare_metal, serverless" ;
  ] .
```

#### Cardinality Constraints

Relationships must respect cardinality constraints:

```turtle
:PodShape
  a sh:NodeShape ;
  sh:targetClass :Pod ;
  sh:property [
    sh:path :runs_on ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:class :VirtualMachine ;
    sh:message "Pod must run on exactly one VirtualMachine" ;
  ] .
```

#### Cross-Layer Relationship Validation

Cross-layer relationships must connect appropriate entity types:

```turtle
:ApplicationShape
  sh:property [
    sh:path :runs_on ;
    sh:or (
      [ sh:class :VirtualMachine ]
      [ sh:class :PhysicalServer ]
      [ sh:class :CloudInstance ]
    ) ;
    sh:message "Application must run on VirtualMachine, PhysicalServer, or CloudInstance" ;
  ] .
```

#### Numeric Range Validation

Numeric attributes must be within valid ranges:

```turtle
:VirtualMachineShape
  sh:property [
    sh:path :vcpu_count ;
    sh:datatype xsd:integer ;
    sh:minInclusive 1 ;
    sh:maxInclusive 128 ;
    sh:message "vcpu_count must be between 1 and 128" ;
  ] ;
  sh:property [
    sh:path :memory_gb ;
    sh:datatype xsd:decimal ;
    sh:minExclusive 0.0 ;
    sh:message "memory_gb must be greater than 0" ;
  ] .
```

#### Custom Business Logic Validation

SPARQL-based validation for complex rules:

```turtle
:ActiveCertificateNotExpiredShape
  a sh:NodeShape ;
  sh:targetClass :Certificate ;
  sh:sparql [
    sh:message "Active certificate must not be expired" ;
    sh:prefixes :, xsd: ;
    sh:select """
      SELECT $this
      WHERE {
        $this :lifecycle_status "active" .
        $this :valid_to ?validTo .
        FILTER (?validTo < NOW())
      }
    """ ;
  ] .
```

### Validation Error Messages

All validation shapes include descriptive error messages to help identify and fix issues:

- **Missing mandatory attributes**: "Entity must have exactly one [attribute]"
- **Invalid enumeration values**: "[attribute] must be one of: [valid values]"
- **Cardinality violations**: "Entity must have [min] to [max] [relationship]"
- **Type mismatches**: "[relationship] must connect to [valid entity types]"
- **Range violations**: "[attribute] must be between [min] and [max]"
- **Business logic violations**: Custom messages for complex rules

### Validation Tools

The ontology can be validated using:

- **Apache Jena SHACL**: Command-line validation tool
- **pySHACL**: Python library for SHACL validation
- **TopBraid SHACL Validator**: Commercial validation tool
- **RDF4J SHACL**: Java library for SHACL validation

**Example validation command**:
```bash
pyshacl -s shacl-shapes.ttl -d instance-data.ttl -f human
```

---

## Usage Examples

### Creating Entity Instances

#### Example 1: Business Process to Application

```turtle
@prefix : <http://example.org/it-infrastructure-ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Business Process
:OrderFulfillment a :BusinessProcess ;
  :name "Order Fulfillment" ;
  :owner "Operations Manager" ;
  :criticality "critical" ;
  :lifecycle_status "active" ;
  :process_type "core" ;
  :frequency "real-time" .

# Application
:OrderManagementSystem a :Application ;
  :name "Order Management System" ;
  :application_type "monolithic" ;
  :deployment_model "vm_based" ;
  :technology_stack "Java EE" ;
  :lifecycle_status "production" .

# Relationship
:OrderFulfillment :realized_by :OrderManagementSystem .
```

#### Example 2: Containerized Microservice

```turtle
# Application
:OrderService a :Application ;
  :name "Order Service" ;
  :application_type "microservice" ;
  :deployment_model "containerized" ;
  :technology_stack "Node.js" ;
  :lifecycle_status "production" .

# Container Image
:OrderServiceImage a :ContainerImage ;
  :name "order-service" ;
  :image_tag "v1.2.3" ;
  :registry_url "registry.example.com/order-service:v1.2.3"^^xsd:anyURI ;
  :lifecycle_status "active" .

# Pod
:OrderServicePod a :Pod ;
  :name "order-service-pod-abc123" ;
  :replica_count 3 ;
  :lifecycle_status "running" .

# Virtual Machine (Kubernetes worker node)
:K8sWorkerNode01 a :VirtualMachine ;
  :name "k8s-worker-node-01" ;
  :resource_type "virtual" ;
  :vcpu_count 8 ;
  :memory_gb 32.0 ;
  :lifecycle_status "running" .

# Relationships
:OrderService :deployed_as :OrderServicePod .
:OrderServicePod :uses_image :OrderServiceImage .
:OrderServicePod :runs_on :K8sWorkerNode01 .
```

#### Example 3: Database with Storage

```turtle
# Database
:OrderDB a :Database ;
  :name "OrderDB" ;
  :database_type "relational" ;
  :database_engine "PostgreSQL" ;
  :version "14.5" ;
  :port 5432 ;
  :data_classification "confidential" ;
  :lifecycle_status "production" .

# Storage Volume
:SAN_Volume_123 a :StorageVolume ;
  :name "SAN-Volume-123" ;
  :volume_id "vol-123456" ;
  :capacity_gb 500.0 ;
  :volume_type "block" ;
  :lifecycle_status "active" .

# Storage Array
:NetApp_SAN_01 a :StorageArray ;
  :name "NetApp-SAN-01" ;
  :storage_type "san" ;
  :manufacturer "NetApp" ;
  :capacity_tb 50.0 ;
  :location "Datacenter-East-Rack-05" ;
  :lifecycle_status "active" .

# Relationships
:OrderService :uses :OrderDB .
:OrderDB :stored_on :SAN_Volume_123 .
:SAN_Volume_123 :allocated_from :NetApp_SAN_01 .
```

#### Example 4: Network and Security

```turtle
# Load Balancer
:WebLoadBalancer a :LoadBalancer ;
  :name "Web-LB-01" ;
  :lb_type "hardware" ;
  :algorithm "round_robin" ;
  :port 443 ;
  :protocol "https" ;
  :lifecycle_status "active" .

# Firewall
:WebAppFirewall a :Firewall ;
  :name "WebApp-Firewall" ;
  :security_type "firewall" ;
  :firewall_type "waf" ;
  :rule_count 150 ;
  :lifecycle_status "active" .

# Certificate
:WebServerCert a :Certificate ;
  :name "*.example.com" ;
  :security_type "certificate" ;
  :certificate_type "ssl_tls" ;
  :subject "CN=*.example.com" ;
  :issuer "CN=Example CA" ;
  :valid_from "2024-01-01"^^xsd:date ;
  :valid_to "2025-01-01"^^xsd:date ;
  :key_size 2048 ;
  :lifecycle_status "active" .

# Relationships
:OrderService :communicates_via :WebLoadBalancer .
:OrderService :protected_by :WebAppFirewall .
:OrderService :secured_by :WebServerCert .
```

### Query Examples

#### Query 1: Root Cause Analysis

Find all infrastructure components an application depends on:

**SPARQL**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?component ?layer ?status
WHERE {
  :OrderManagementSystem (:uses|:runs_on|:hosted_on|:communicates_via)+ ?component .
  ?component a ?layer .
  ?component :lifecycle_status ?status .
  FILTER(?status IN ("degraded", "failed"))
}
```

**Cypher** (Neo4j):
```cypher
MATCH (app:Application {name: 'Order Management System'})
      -[r:USES|RUNS_ON|HOSTED_ON|COMMUNICATES_VIA*]->(component)
WHERE component.lifecycle_status IN ['degraded', 'failed']
RETURN component.name AS component,
       labels(component) AS layer,
       component.lifecycle_status AS status
```

#### Query 2: Impact Analysis

Find all applications affected by a server maintenance:

**SPARQL**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?affected ?type
WHERE {
  ?affected (:runs_on|:hosted_on|:uses)+ :Server123 .
  ?affected a ?type .
}
```

**Cypher** (Neo4j):
```cypher
MATCH (affected)-[r:RUNS_ON|HOSTED_ON|USES*]->(server:PhysicalServer {name: 'Server123'})
RETURN affected.name AS affected,
       labels(affected) AS type
```

#### Query 3: Full Stack Decomposition

Trace from business process to physical infrastructure:

**SPARQL**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?process ?app ?container ?vm ?server
WHERE {
  ?process a :BusinessProcess ;
           :realized_by ?app .
  ?app :deployed_as ?container .
  ?container :runs_on ?vm .
  ?vm :runs_on ?server .
}
```

**Cypher** (Neo4j):
```cypher
MATCH path = (bp:BusinessProcess)-[:REALIZED_BY]->(app:Application)
             -[:DEPLOYED_AS]->(container:Container)
             -[:RUNS_ON]->(vm:VirtualMachine)
             -[:RUNS_ON]->(server:PhysicalServer)
RETURN bp.name AS business_process,
       app.name AS application,
       container.name AS container,
       vm.name AS virtual_machine,
       server.name AS physical_server
```

#### Query 4: Security Audit

Find all applications without firewall protection:

**SPARQL**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?name
WHERE {
  ?app a :Application ;
       :name ?name ;
       :lifecycle_status "production" .
  FILTER NOT EXISTS {
    ?app :protected_by ?firewall .
    ?firewall a :Firewall .
  }
}
```

**Cypher** (Neo4j):
```cypher
MATCH (app:Application {lifecycle_status: 'production'})
WHERE NOT (app)-[:PROTECTED_BY]->(:Firewall)
RETURN app.name AS application
```

#### Query 5: Certificate Expiration Check

Find certificates expiring within 30 days:

**SPARQL**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?cert ?name ?validTo
WHERE {
  ?cert a :Certificate ;
        :name ?name ;
        :valid_to ?validTo ;
        :lifecycle_status "active" .
  BIND(NOW() + "P30D"^^xsd:duration AS ?thirtyDaysFromNow)
  FILTER(?validTo <= ?thirtyDaysFromNow && ?validTo >= NOW())
}
ORDER BY ?validTo
```

**Cypher** (Neo4j):
```cypher
MATCH (cert:Certificate {lifecycle_status: 'active'})
WHERE cert.valid_to <= date() + duration({days: 30})
  AND cert.valid_to >= date()
RETURN cert.name AS certificate,
       cert.valid_to AS expiration_date
ORDER BY cert.valid_to
```

---

## Extension Guidelines

### Adding New Entity Types

To extend the ontology with new entity types:

1. **Identify the appropriate layer** for the new entity type based on its abstraction level and purpose.

2. **Define the entity as a subclass** of the appropriate layer class:

```turtle
:MyNewEntity
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;  # or appropriate layer
  rdfs:label "My New Entity" ;
  rdfs:comment "Description of the new entity type" ;
  skos:definition "Formal definition of the entity" ;
  skos:example "Example usage of the entity" ;
  dcterms:source "Framework or standard source" .
```

3. **Define attributes** (data properties) for the new entity:

```turtle
:myNewAttribute
  rdf:type owl:DatatypeProperty ;
  rdfs:domain :MyNewEntity ;
  rdfs:range xsd:string ;  # or appropriate datatype
  rdfs:label "My New Attribute" ;
  rdfs:comment "Description of the attribute" ;
  dcterms:source "Framework source for this attribute" .
```

4. **Define relationships** (object properties) to existing entity types:

```turtle
:myNewRelationship
  rdf:type owl:ObjectProperty ;
  rdfs:domain :MyNewEntity ;
  rdfs:range :ExistingEntity ;
  rdfs:label "My New Relationship" ;
  rdfs:comment "Description of the relationship" ;
  owl:inverseOf :inverseRelationship .
```

5. **Create SHACL validation shapes** for the new entity:

```turtle
:MyNewEntityShape
  a sh:NodeShape ;
  sh:targetClass :MyNewEntity ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :myNewAttribute ;
    sh:minCount 1 ;
    sh:in ( "value1" "value2" "value3" ) ;
  ] .
```

6. **Document the new entity** in the appropriate layer specification file.

7. **Update framework mappings** if the entity is sourced from a standard framework.

---

### Adding Custom Attributes

Organizations may need custom attributes beyond framework-sourced ones:

1. **Use a separate namespace** for custom attributes:

```turtle
@prefix custom: <http://example.org/custom#> .

custom:deploymentRegion
  rdf:type owl:DatatypeProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:string ;
  rdfs:label "Deployment Region" ;
  rdfs:comment "Custom attribute for deployment region" .
```

2. **Apply custom attributes** to entity instances:

```turtle
:MyApplication a :Application ;
  :name "My Application" ;
  :application_type "microservice" ;
  custom:deploymentRegion "us-east-1" ;
  custom:costCenter "CC-12345" .
```

3. **Create SHACL shapes** for custom attributes if validation is needed:

```turtle
:CustomApplicationShape
  a sh:NodeShape ;
  sh:targetClass :Application ;
  sh:property [
    sh:path custom:deploymentRegion ;
    sh:datatype xsd:string ;
    sh:pattern "^[a-z]{2}-[a-z]+-[0-9]$" ;
    sh:message "Deployment region must match pattern: us-east-1" ;
  ] .
```

4. **Document custom attributes** with rationale and usage guidelines.

5. **Avoid conflicts** with framework-sourced attributes.

---

### Adding New Frameworks

To integrate a new framework into the ontology:

1. **Analyze the framework** metamodel and concepts:
   - Identify entity types and their definitions
   - Extract attributes and their data types
   - Map relationships and cardinality constraints

2. **Map framework concepts** to ontology layers:
   - Determine which layer each framework concept belongs to
   - Identify overlaps with existing entity types
   - Document unique concepts not yet in the ontology

3. **Extract attributes** from the framework:
   - Identify attributes not already in the ontology
   - Document data types and constraints
   - Cite the framework as the source

4. **Update entity type definitions** with new attributes:

```turtle
:Application
  dcterms:source "TOGAF Application Architecture, CIM_ApplicationSystem, NewFramework" .

:newFrameworkAttribute
  rdf:type owl:DatatypeProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:string ;
  dcterms:source "NewFramework" .
```

5. **Create framework mapping documentation**:
   - Add a new framework analysis document
   - Create mapping tables showing framework-to-ontology mappings
   - Document semantic alignments and differences

6. **Update SHACL shapes** if new validation rules are needed.

7. **Test the integration** with sample data from the new framework.

---

### Versioning Strategy

The ontology follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible changes (e.g., removing entity types, changing relationship semantics)
- **MINOR**: Backward-compatible additions (e.g., new entity types, new attributes)
- **PATCH**: Backward-compatible fixes (e.g., documentation updates, bug fixes)

**Version declaration**:
```turtle
<http://example.org/it-infrastructure-ontology>
  a owl:Ontology ;
  owl:versionInfo "1.0.0" ;
  dcterms:created "2024-01-01"^^xsd:date ;
  dcterms:modified "2024-01-15"^^xsd:date .
```

**Version compatibility**:
- Instance data created with version 1.x should be compatible with all 1.x versions
- Major version changes may require data migration
- Deprecation warnings should be provided before removing concepts

---

### Best Practices

1. **Maintain layer separation**: Ensure new entity types belong to exactly one layer.

2. **Follow naming conventions**:
   - Use PascalCase for classes (e.g., `BusinessProcess`, `VirtualMachine`)
   - Use snake_case for properties (e.g., `lifecycle_status`, `runs_on`)
   - Use descriptive names that reflect the entity's purpose

3. **Document framework sources**: Always cite the source framework for attributes and concepts.

4. **Create comprehensive SHACL shapes**: Validate all mandatory attributes, enumerations, and relationships.

5. **Provide usage examples**: Include Turtle examples for new entity types and relationships.

6. **Test with sample data**: Validate new concepts with realistic instance data.

7. **Maintain backward compatibility**: Avoid breaking changes when possible.

8. **Update documentation**: Keep all documentation synchronized with ontology changes.

9. **Use standard datatypes**: Prefer XSD datatypes (xsd:string, xsd:integer, xsd:date, etc.).

10. **Define inverse properties**: Create inverse properties for bidirectional navigation.

---

## Conclusion

This reference documentation provides a comprehensive guide to the IT Infrastructure and Application Dependency Ontology. The ontology offers:

- **Formal specification** in OWL 2 with SHACL validation
- **50+ entity types** across six architectural layers
- **Framework alignment** with TOGAF, CIM, ITIL, ArchiMate, Kubernetes, and cloud APIs
- **Comprehensive relationships** for dependency tracking and impact analysis
- **Validation rules** for data quality enforcement
- **Query patterns** for operational analysis
- **Extension guidelines** for customization

For additional information, refer to:
- **Main ontology file**: `it-infrastructure-ontology.ttl`
- **SHACL shapes**: `shacl-shapes.ttl`
- **Layer specifications**: `layer-specifications/` directory
- **Framework analysis**: `framework-analysis/` directory
- **Deployment patterns**: `deployment-patterns.md`
- **Query patterns**: `query-patterns.md`

---

**Document Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Ontology Version**: 1.0.0  
**Status**: Complete

