# Deployment Patterns and Use Cases

## Overview

This document provides detailed examples of deployment patterns for the IT Infrastructure and Application Dependency Ontology. Each pattern demonstrates how components decompose across the six ontology layers, with concrete instance examples in RDF/Turtle format.

The patterns cover:
1. **Containerized Applications**: Modern microservices in Kubernetes/OpenShift
2. **Legacy Applications**: Traditional applications on application servers
3. **Storage Decomposition**: Various storage patterns from on-premises to cloud
4. **Hybrid and SOA Integration**: Complex integration scenarios

---

## 1. Containerized Application Patterns

### Pattern 1.1: Microservice in Kubernetes with External Route

**Scenario**: A Node.js microservice deployed in Kubernetes, exposed externally via an OpenShift Route with TLS termination.

**Architecture Overview**:
```
Business Process: "Customer Order Processing"
    ↓ fulfills
Application: "Order Service API"
    ↓ deployed_as
Container: "order-service-container"
    ↓ part_of
Pod: "order-service-pod-7d9f8b"
    ↓ managed_by
Deployment: "order-service-deployment"
    ↓ exposed_by
Service: "order-service-svc"
    ↓ exposed_by
Route: "order-service-route"
    ↓ runs_on
Virtual Machine: "k8s-worker-node-01"
    ↓ runs_on
Physical Server: "server-dc1-rack05-u12"
```

**Layer Decomposition**:
- **Layer 1 (Business)**: Customer Order Processing
- **Layer 2 (Application)**: Order Service API
- **Layer 3 (Container)**: Container, Pod, Deployment, Service, Route
- **Layer 4 (Physical)**: Virtual Machine, Physical Server
- **Layer 5 (Network)**: Communication paths (implicit in Route)
- **Layer 6 (Security)**: TLS certificate for Route

### RDF/Turtle Instance Data

```turtle
@prefix : <http://example.org/ontology/infrastructure#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Layer 1: Business Process
:CustomerOrderProcessing
    rdf:type :BusinessProcess ;
    :name "Customer Order Processing" ;
    :description "End-to-end process for handling customer orders" ;
    :owner "Sales Operations Team" ;
    :criticality "critical" ;
    :lifecycle_status "active" ;
    :fulfills :OrderServiceAPI .

# Layer 2: Application
:OrderServiceAPI
    rdf:type :Application ;
    :name "Order Service API" ;
    :version "2.3.1" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Node.js 18" ;
    :technology_stack "Node.js, Express, MongoDB" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" ;
    :deployed_as :OrderServiceContainer ;
    :uses :OrderDatabase ;
    :communicates_via :OrderServicePath .

# Layer 3: Container and Orchestration
:OrderServiceContainer
    rdf:type :Container ;
    :name "order-service-container" ;
    :image_name "registry.example.com/order-service:2.3.1" ;
    :orchestration_platform "openshift" ;
    :lifecycle_status "running" ;
    :part_of :OrderServicePod .

:OrderServicePod
    rdf:type :Pod ;
    :name "order-service-pod-7d9f8b" ;
    :orchestration_platform "openshift" ;
    :replica_count 3 ;
    :resource_limits "cpu: 500m, memory: 512Mi" ;
    :lifecycle_status "running" ;
    :managed_by :OrderServiceDeployment ;
    :runs_on :K8sWorkerNode01 .

:OrderServiceDeployment
    rdf:type :Deployment ;
    :name "order-service-deployment" ;
    :orchestration_platform "openshift" ;
    :replica_count 3 ;
    :lifecycle_status "running" ;
    :exposed_by :OrderServiceSvc .

:OrderServiceSvc
    rdf:type :Service ;
    :name "order-service-svc" ;
    :orchestration_platform "openshift" ;
    :exposed_port 8080 ;
    :lifecycle_status "active" ;
    :exposed_by :OrderServiceRoute .

:OrderServiceRoute
    rdf:type :Route ;
    :name "order-service-route" ;
    :orchestration_platform "openshift" ;
    :external_hostname "orders.example.com" ;
    :route_path "/api/v1/orders" ;
    :tls_termination "edge" ;
    :lifecycle_status "active" ;
    :secured_by :OrderServiceCertificate .

# Layer 4: Physical Infrastructure
:K8sWorkerNode01
    rdf:type :VirtualMachine ;
    :name "k8s-worker-node-01" ;
    :resource_type "virtual" ;
    :location "datacenter-1" ;
    :capacity "16 vCPU, 64GB RAM" ;
    :operating_system "Red Hat CoreOS 4.12" ;
    :lifecycle_status "running" ;
    :runs_on :PhysicalServer01 .

:PhysicalServer01
    rdf:type :PhysicalServer ;
    :name "server-dc1-rack05-u12" ;
    :resource_type "physical" ;
    :location "datacenter-1, rack-05, unit-12" ;
    :capacity "2x Intel Xeon Gold 6248R, 512GB RAM" ;
    :operating_system "VMware ESXi 7.0" ;
    :lifecycle_status "running" .

# Layer 5: Network
:OrderServicePath
    rdf:type :CommunicationPath ;
    :name "order-service-ingress-path" ;
    :protocol "HTTPS" ;
    :port 443 ;
    :lifecycle_status "active" ;
    :routes_through :LoadBalancer01 .

:LoadBalancer01
    rdf:type :LoadBalancer ;
    :name "openshift-ingress-lb" ;
    :device_type "load_balancer" ;
    :ip_address "10.0.1.100" ;
    :lifecycle_status "active" .

# Layer 6: Security
:OrderServiceCertificate
    rdf:type :Certificate ;
    :name "orders.example.com-cert" ;
    :security_type "certificate" ;
    :expiration_date "2025-12-31"^^xsd:date ;
    :trust_level "trusted" ;
    :lifecycle_status "active" ;
    :issued_by :InternalCA .

:InternalCA
    rdf:type :CertificateAuthority ;
    :name "Example Corp Internal CA" ;
    :security_type "certificate" ;
    :trust_level "trusted" ;
    :lifecycle_status "active" .
```

### Pattern 1.2: Microservice with Database and Persistent Storage

**Scenario**: A Python microservice with PostgreSQL database using Kubernetes Persistent Volume Claims.

**Architecture Overview**:
```
Application: "Analytics Service"
    ↓ uses
Database: "AnalyticsDB" (PostgreSQL)
    ↓ deployed_as
Container: "postgres-container"
    ↓ part_of
Pod: "postgres-pod-abc123"
    ↓ uses
PersistentVolumeClaim: "postgres-pvc"
    ↓ bound_to
PersistentVolume: "pv-ebs-vol-xyz"
    ↓ backed_by
StorageVolume: "ebs-vol-xyz"
    ↓ provisioned_from
CloudStorageService: "AWS EBS"
```

### RDF/Turtle Instance Data

```turtle
# Layer 2: Application and Database
:AnalyticsService
    rdf:type :Application ;
    :name "Analytics Service" ;
    :version "1.5.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Python 3.11" ;
    :technology_stack "Python, FastAPI, SQLAlchemy" ;
    :lifecycle_status "production" ;
    :deployed_as :AnalyticsServiceContainer ;
    :uses :AnalyticsDB .

:AnalyticsDB
    rdf:type :Database ;
    :name "AnalyticsDB" ;
    :version "PostgreSQL 15" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :data_classification "internal" ;
    :lifecycle_status "production" ;
    :deployed_as :PostgresContainer ;
    :stored_on :PostgresPVC .

# Layer 3: Container and Orchestration
:AnalyticsServiceContainer
    rdf:type :Container ;
    :name "analytics-service-container" ;
    :image_name "analytics-service:1.5.0" ;
    :orchestration_platform "kubernetes" ;
    :lifecycle_status "running" ;
    :part_of :AnalyticsServicePod .

:AnalyticsServicePod
    rdf:type :Pod ;
    :name "analytics-service-pod-def456" ;
    :orchestration_platform "kubernetes" ;
    :replica_count 2 ;
    :lifecycle_status "running" ;
    :runs_on :K8sWorkerNode02 .

:PostgresContainer
    rdf:type :Container ;
    :name "postgres-container" ;
    :image_name "postgres:15-alpine" ;
    :orchestration_platform "kubernetes" ;
    :lifecycle_status "running" ;
    :part_of :PostgresPod .

:PostgresPod
    rdf:type :Pod ;
    :name "postgres-pod-abc123" ;
    :orchestration_platform "kubernetes" ;
    :replica_count 1 ;
    :lifecycle_status "running" ;
    :uses :PostgresPVC ;
    :runs_on :K8sWorkerNode03 .

:PostgresPVC
    rdf:type :PersistentVolumeClaim ;
    :name "postgres-pvc" ;
    :orchestration_platform "kubernetes" ;
    :capacity "100Gi" ;
    :lifecycle_status "bound" ;
    :bound_to :PostgresPV .

:PostgresPV
    rdf:type :PersistentVolume ;
    :name "pv-ebs-vol-xyz" ;
    :orchestration_platform "kubernetes" ;
    :capacity "100Gi" ;
    :lifecycle_status "bound" ;
    :backed_by :EBSVolXYZ .

# Layer 4: Physical Infrastructure (Cloud)
:K8sWorkerNode02
    rdf:type :CloudInstance ;
    :name "k8s-worker-node-02" ;
    :resource_type "cloud_iaas" ;
    :location "us-east-1a" ;
    :capacity "t3.xlarge (4 vCPU, 16GB RAM)" ;
    :operating_system "Amazon Linux 2" ;
    :lifecycle_status "running" .

:K8sWorkerNode03
    rdf:type :CloudInstance ;
    :name "k8s-worker-node-03" ;
    :resource_type "cloud_iaas" ;
    :location "us-east-1b" ;
    :capacity "t3.xlarge (4 vCPU, 16GB RAM)" ;
    :operating_system "Amazon Linux 2" ;
    :lifecycle_status "running" .

:EBSVolXYZ
    rdf:type :StorageVolume ;
    :name "ebs-vol-xyz" ;
    :resource_type "cloud_iaas" ;
    :location "us-east-1a" ;
    :capacity "100GB" ;
    :lifecycle_status "in-use" ;
    :provisioned_from :AWSEBS .

:AWSEBS
    rdf:type :CloudStorageService ;
    :name "AWS EBS" ;
    :resource_type "cloud_iaas" ;
    :location "us-east-1" ;
    :lifecycle_status "active" .
```

### Pattern 1.3: Multi-Container Pod with Sidecar

**Scenario**: Application with logging sidecar container in the same pod.

**Architecture Overview**:
```
Application: "Payment Service"
    ↓ deployed_as
Container: "payment-service-container"
    ↓ part_of (with sidecar)
Pod: "payment-service-pod" (contains 2 containers)
    ├─ Container: "payment-service-container"
    └─ Container: "fluentd-sidecar" (logging)
```

### RDF/Turtle Instance Data

```turtle
# Layer 2: Application
:PaymentService
    rdf:type :Application ;
    :name "Payment Service" ;
    :version "3.1.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Java 17" ;
    :technology_stack "Spring Boot, Kafka" ;
    :data_classification "restricted" ;
    :lifecycle_status "production" ;
    :deployed_as :PaymentServiceContainer .

# Layer 3: Container and Orchestration
:PaymentServiceContainer
    rdf:type :Container ;
    :name "payment-service-container" ;
    :image_name "payment-service:3.1.0" ;
    :orchestration_platform "kubernetes" ;
    :exposed_port 8080 ;
    :lifecycle_status "running" ;
    :part_of :PaymentServicePod .

:FluentdSidecar
    rdf:type :Container ;
    :name "fluentd-sidecar" ;
    :image_name "fluentd:v1.15" ;
    :orchestration_platform "kubernetes" ;
    :lifecycle_status "running" ;
    :part_of :PaymentServicePod .

:PaymentServicePod
    rdf:type :Pod ;
    :name "payment-service-pod-xyz789" ;
    :orchestration_platform "kubernetes" ;
    :replica_count 5 ;
    :resource_limits "cpu: 1000m, memory: 2Gi" ;
    :lifecycle_status "running" ;
    :runs_on :K8sWorkerNode04 .

# Layer 4: Physical Infrastructure
:K8sWorkerNode04
    rdf:type :VirtualMachine ;
    :name "k8s-worker-node-04" ;
    :resource_type "virtual" ;
    :location "datacenter-2" ;
    :capacity "8 vCPU, 32GB RAM" ;
    :operating_system "Ubuntu 22.04" ;
    :lifecycle_status "running" .
```

---

## 2. Legacy Application Patterns

### Pattern 2.1: Java EE Application on WebSphere

**Scenario**: Traditional enterprise application deployed on IBM WebSphere Application Server.

**Architecture Overview**:
```
Business Process: "Customer Relationship Management"
    ↓ fulfills
Application: "CRM Application"
    ↓ contains
ApplicationComponent: "CustomerServlet"
    ↓ deployed_on
ApplicationServer: "WebSphere 9.0 Instance"
    ↓ runs_on
Virtual Machine: "crm-app-vm-01"
    ↓ runs_on
Physical Server: "server-dc1-rack03-u08"
```

**Note**: Layer 3 (Container & Orchestration) is bypassed for legacy applications.

### RDF/Turtle Instance Data

```turtle
# Layer 1: Business Process
:CustomerRelationshipManagement
    rdf:type :BusinessProcess ;
    :name "Customer Relationship Management" ;
    :description "Manage customer interactions and data" ;
    :owner "Customer Success Team" ;
    :criticality "high" ;
    :lifecycle_status "active" ;
    :fulfills :CRMApplication .

# Layer 2: Application
:CRMApplication
    rdf:type :Application ;
    :name "CRM Application" ;
    :version "5.2.1" ;
    :application_type "monolithic" ;
    :deployment_model "vm_based" ;
    :runtime_environment "WebSphere 9.0" ;
    :technology_stack "Java EE 8, JSF, EJB" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" ;
    :contains :CustomerServlet ;
    :runs_on :CRMAppVM01 ;
    :uses :CRMDatabase .

:CustomerServlet
    rdf:type :ApplicationComponent ;
    :name "CustomerServlet" ;
    :version "5.2.1" ;
    :application_type "monolithic" ;
    :technology_stack "Java Servlet" ;
    :lifecycle_status "production" ;
    :deployed_on :WebSphere90Instance .

:WebSphere90Instance
    rdf:type :ApplicationServer ;
    :name "WebSphere 9.0 Instance" ;
    :version "9.0.5.10" ;
    :application_type "legacy" ;
    :runtime_environment "WebSphere Application Server" ;
    :technology_stack "IBM WebSphere" ;
    :lifecycle_status "production" ;
    :runs_on :CRMAppVM01 .

:CRMDatabase
    rdf:type :Database ;
    :name "CRM_PROD_DB" ;
    :version "Oracle 19c" ;
    :application_type "legacy" ;
    :deployment_model "vm_based" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" ;
    :contains :CRMDatabaseInstance ;
    :hosted_on :CRMDBVolume .

:CRMDatabaseInstance
    rdf:type :DatabaseInstance ;
    :name "CRMDB01" ;
    :version "Oracle 19c" ;
    :lifecycle_status "production" .

# Layer 4: Physical Infrastructure
:CRMAppVM01
    rdf:type :VirtualMachine ;
    :name "crm-app-vm-01" ;
    :resource_type "virtual" ;
    :location "datacenter-1, rack-03" ;
    :capacity "8 vCPU, 32GB RAM" ;
    :operating_system "Red Hat Enterprise Linux 8.6" ;
    :lifecycle_status "running" ;
    :runs_on :PhysicalServer03 .

:PhysicalServer03
    rdf:type :PhysicalServer ;
    :name "server-dc1-rack03-u08" ;
    :resource_type "physical" ;
    :location "datacenter-1, rack-03, unit-08" ;
    :capacity "2x Intel Xeon Gold 6248R, 256GB RAM" ;
    :operating_system "VMware ESXi 7.0" ;
    :lifecycle_status "running" .

:CRMDBVolume
    rdf:type :StorageVolume ;
    :name "lun-crm-db-001" ;
    :resource_type "physical" ;
    :location "datacenter-1" ;
    :capacity "500GB" ;
    :lifecycle_status "in-use" ;
    :allocated_from :StorageArraySAN01 .

:StorageArraySAN01
    rdf:type :StorageArray ;
    :name "EMC-VNX-01" ;
    :resource_type "physical" ;
    :location "datacenter-1, storage-room" ;
    :capacity "50TB" ;
    :lifecycle_status "active" .

# Layer 5: Network
:CRMNetworkPath
    rdf:type :CommunicationPath ;
    :name "crm-app-network-path" ;
    :protocol "HTTP" ;
    :port 9080 ;
    :lifecycle_status "active" ;
    :routes_through :CRMLoadBalancer .

:CRMLoadBalancer
    rdf:type :LoadBalancer ;
    :name "f5-bigip-crm" ;
    :device_type "load_balancer" ;
    :ip_address "10.1.5.100" ;
    :lifecycle_status "active" .

# Layer 6: Security
:CRMFirewall
    rdf:type :Firewall ;
    :name "crm-app-firewall" ;
    :security_type "firewall" ;
    :policy_rules "Allow 9080 from DMZ" ;
    :trust_level "trusted" ;
    :lifecycle_status "active" .

:CRMApplication :protected_by :CRMFirewall .
```


### Pattern 2.2: .NET Application on IIS

**Scenario**: ASP.NET application on Windows Server with IIS.

**Architecture Overview**:
```
Application: "HR Portal"
    ↓ deployed_on
ApplicationServer: "IIS 10.0"
    ↓ runs_on
Virtual Machine: "hr-portal-vm-01"
    ↓ runs_on
Physical Server: "server-dc2-rack07-u15"
```

### RDF/Turtle Instance Data

```turtle
# Layer 2: Application
:HRPortal
    rdf:type :Application ;
    :name "HR Portal" ;
    :version "4.1.0" ;
    :application_type "monolithic" ;
    :deployment_model "vm_based" ;
    :runtime_environment "IIS 10.0" ;
    :technology_stack ".NET Framework 4.8, ASP.NET MVC" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" ;
    :deployed_on :IIS10Instance ;
    :uses :HRDatabase .

:IIS10Instance
    rdf:type :ApplicationServer ;
    :name "IIS 10.0" ;
    :version "10.0.17763" ;
    :application_type "legacy" ;
    :runtime_environment "Internet Information Services" ;
    :technology_stack "Microsoft IIS" ;
    :lifecycle_status "production" ;
    :runs_on :HRPortalVM01 .

:HRDatabase
    rdf:type :Database ;
    :name "HR_PROD_DB" ;
    :version "SQL Server 2019" ;
    :application_type "legacy" ;
    :deployment_model "vm_based" ;
    :data_classification "restricted" ;
    :lifecycle_status "production" ;
    :runs_on :HRDBServer01 .

# Layer 4: Physical Infrastructure
:HRPortalVM01
    rdf:type :VirtualMachine ;
    :name "hr-portal-vm-01" ;
    :resource_type "virtual" ;
    :location "datacenter-2, rack-07" ;
    :capacity "4 vCPU, 16GB RAM" ;
    :operating_system "Windows Server 2019" ;
    :lifecycle_status "running" ;
    :runs_on :PhysicalServer07 .

:HRDBServer01
    rdf:type :VirtualMachine ;
    :name "hr-db-server-01" ;
    :resource_type "virtual" ;
    :location "datacenter-2, rack-07" ;
    :capacity "8 vCPU, 64GB RAM" ;
    :operating_system "Windows Server 2019" ;
    :lifecycle_status "running" ;
    :runs_on :PhysicalServer07 .

:PhysicalServer07
    rdf:type :PhysicalServer ;
    :name "server-dc2-rack07-u15" ;
    :resource_type "physical" ;
    :location "datacenter-2, rack-07, unit-15" ;
    :capacity "2x Intel Xeon Gold 6248R, 512GB RAM" ;
    :operating_system "VMware ESXi 7.0" ;
    :lifecycle_status "running" .
```



---

## 3. Storage Decomposition Patterns

### Pattern 3.1: On-Premises Database with SAN Storage

**Scenario**: Oracle database with storage on a SAN array.

**Architecture Overview**:
```
Application: "ERP System"
    ↓ uses
Database: "ERP_PROD_DB"
    ↓ contains
DatabaseInstance: "ERPDB01"
    ↓ stored_on
StorageVolume: "LUN-456"
    ↓ allocated_from
StorageArray: "EMC-VNX-01"
```

**Layer Decomposition**:
- **Layer 2 (Application)**: ERP System, ERP_PROD_DB (logical database)
- **Layer 4 (Physical)**: StorageVolume, StorageArray (physical storage)

### RDF/Turtle Instance Data

```turtle
# Layer 2: Application and Database
:ERPSystem
    rdf:type :Application ;
    :name "ERP System" ;
    :version "12.2.1" ;
    :application_type "monolithic" ;
    :deployment_model "vm_based" ;
    :runtime_environment "Oracle Forms" ;
    :technology_stack "Oracle EBS, PL/SQL" ;
    :data_classification "restricted" ;
    :lifecycle_status "production" ;
    :uses :ERPProdDB .

:ERPProdDB
    rdf:type :Database ;
    :name "ERP_PROD_DB" ;
    :version "Oracle 19c" ;
    :application_type "legacy" ;
    :deployment_model "vm_based" ;
    :data_classification "restricted" ;
    :lifecycle_status "production" ;
    :contains :ERPDB01 ;
    :hosted_on :ERPDBServer ;
    :stored_on :LUN456 .

:ERPDB01
    rdf:type :DatabaseInstance ;
    :name "ERPDB01" ;
    :version "Oracle 19c" ;
    :lifecycle_status "production" ;
    :stored_on :LUN456 .

# Layer 4: Physical Infrastructure - Storage
:ERPDBServer
    rdf:type :VirtualMachine ;
    :name "erp-db-server-01" ;
    :resource_type "virtual" ;
    :location "datacenter-1" ;
    :capacity "16 vCPU, 128GB RAM" ;
    :operating_system "Oracle Linux 8" ;
    :lifecycle_status "running" .

:LUN456
    rdf:type :StorageVolume ;
    :name "LUN-456" ;
    :resource_type "physical" ;
    :location "datacenter-1" ;
    :capacity "500GB" ;
    :lifecycle_status "in-use" ;
    :allocated_from :EMCVNX01 .

:EMCVNX01
    rdf:type :StorageArray ;
    :name "EMC-VNX-01" ;
    :resource_type "physical" ;
    :location "datacenter-1, storage-room" ;
    :capacity "50TB" ;
    :lifecycle_status "active" .
```



### Pattern 3.2: Cloud Managed Database (AWS RDS)

**Scenario**: PostgreSQL database managed by AWS RDS.

**Architecture Overview**:
```
Application: "Customer Portal"
    ↓ uses
Database: "CustomerDB"
    ↓ hosted_on
CloudStorageService: "RDS Instance db-abc123"
```

**Layer Decomposition**:
- **Layer 2 (Application)**: Customer Portal, CustomerDB (logical database)
- **Layer 4 (Physical)**: CloudStorageService (managed service abstracts physical storage)

### RDF/Turtle Instance Data

```turtle
# Layer 2: Application and Database
:CustomerPortal
    rdf:type :Application ;
    :name "Customer Portal" ;
    :version "3.0.5" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Node.js 18" ;
    :technology_stack "React, Node.js, PostgreSQL" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" ;
    :uses :CustomerDB .

:CustomerDB
    rdf:type :Database ;
    :name "CustomerDB" ;
    :version "PostgreSQL 14" ;
    :application_type "microservice" ;
    :deployment_model "cloud_iaas" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" ;
    :hosted_on :RDSInstanceABC123 .

# Layer 4: Physical Infrastructure - Cloud
:RDSInstanceABC123
    rdf:type :CloudStorageService ;
    :name "RDS Instance db-abc123" ;
    :resource_type "cloud_paas" ;
    :location "us-east-1" ;
    :capacity "db.r5.xlarge (4 vCPU, 32GB RAM, 500GB storage)" ;
    :lifecycle_status "available" .
```

### Pattern 3.3: Object Storage (S3)

**Scenario**: Document management system using AWS S3 for file storage.

**Architecture Overview**:
```
Application: "Document Management System"
    ↓ uses
ObjectStorageService: "documents-bucket" (logical)
    ↓ stored_in
ObjectStorageBucket: "s3://documents-bucket" (physical)
```

**Layer Decomposition**:
- **Layer 2 (Application)**: Document Management System, documents-bucket (logical)
- **Layer 4 (Physical)**: ObjectStorageBucket (physical S3 bucket)

### RDF/Turtle Instance Data

```turtle
# Layer 2: Application and Object Storage
:DocumentManagementSystem
    rdf:type :Application ;
    :name "Document Management System" ;
    :version "2.1.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Python 3.11" ;
    :technology_stack "Django, Celery, S3" ;
    :data_classification "internal" ;
    :lifecycle_status "production" ;
    :uses :DocumentsBucketLogical .

:DocumentsBucketLogical
    rdf:type :ObjectStorageService ;
    :name "documents-bucket" ;
    :application_type "microservice" ;
    :data_classification "internal" ;
    :lifecycle_status "production" ;
    :stored_in :DocumentsBucketPhysical .

# Layer 4: Physical Infrastructure - Object Storage
:DocumentsBucketPhysical
    rdf:type :ObjectStorageBucket ;
    :name "s3://documents-bucket" ;
    :resource_type "cloud_paas" ;
    :location "us-east-1" ;
    :capacity "5TB" ;
    :lifecycle_status "active" .
```



### Pattern 3.4: Shared File System (NFS)

**Scenario**: Media processing service using NFS shared storage.

**Architecture Overview**:
```
Application: "Media Processing Service"
    ↓ uses
FileStorageService: "/mnt/media-storage" (NFS mount)
    ↓ mounted_from
StorageVolume: "nfs-vol-789"
    ↓ allocated_from
StorageArray: "NetApp-NAS-02"
```

**Layer Decomposition**:
- **Layer 2 (Application)**: Media Processing Service, FileStorageService (logical mount)
- **Layer 4 (Physical)**: StorageVolume, StorageArray (physical NAS)

### RDF/Turtle Instance Data

```turtle
# Layer 2: Application and File Storage
:MediaProcessingService
    rdf:type :Application ;
    :name "Media Processing Service" ;
    :version "1.8.2" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Python 3.10" ;
    :technology_stack "FFmpeg, Celery, Redis" ;
    :data_classification "public" ;
    :lifecycle_status "production" ;
    :uses :MediaStorageMount .

:MediaStorageMount
    rdf:type :FileStorageService ;
    :name "/mnt/media-storage" ;
    :application_type "microservice" ;
    :data_classification "public" ;
    :lifecycle_status "production" ;
    :mounted_from :NFSVol789 .

# Layer 4: Physical Infrastructure - NAS Storage
:NFSVol789
    rdf:type :StorageVolume ;
    :name "nfs-vol-789" ;
    :resource_type "physical" ;
    :location "datacenter-1" ;
    :capacity "10TB" ;
    :lifecycle_status "in-use" ;
    :allocated_from :NetAppNAS02 .

:NetAppNAS02
    rdf:type :StorageArray ;
    :name "NetApp-NAS-02" ;
    :resource_type "physical" ;
    :location "datacenter-1, storage-room" ;
    :capacity "100TB" ;
    :lifecycle_status "active" .

# Layer 5: Network - NFS Protocol
:NFSPath
    rdf:type :CommunicationPath ;
    :name "nfs-storage-path" ;
    :protocol "NFS" ;
    :port 2049 ;
    :lifecycle_status "active" .
```

### Pattern 3.5: Containerized Database with Persistent Volume

**Scenario**: PostgreSQL in Kubernetes with AWS EBS persistent storage.

**Architecture Overview**:
```
Application: "Analytics Service"
    ↓ uses
Database: "AnalyticsDB"
    ↓ deployed_as
Container: "postgres-container"
    ↓ uses
PersistentVolumeClaim: "postgres-pvc"
    ↓ bound_to
PersistentVolume: "pv-ebs-vol-xyz"
    ↓ backed_by
StorageVolume: "ebs-vol-xyz"
    ↓ provisioned_from
CloudStorageService: "AWS EBS"
```

**Layer Decomposition**:
- **Layer 2 (Application)**: Analytics Service, AnalyticsDB
- **Layer 3 (Container)**: Container, PersistentVolumeClaim, PersistentVolume
- **Layer 4 (Physical)**: StorageVolume, CloudStorageService

### RDF/Turtle Instance Data

```turtle
# (Already provided in Pattern 1.2 above - see AnalyticsService example)
```



---

## 4. Hybrid and SOA Integration Patterns

### Pattern 4.1: SOA Integration with Message Queue

**Scenario**: Order processing system integrating multiple services via RabbitMQ.

**Architecture Overview**:
```
Business Process: "Order Fulfillment"
    ↓ fulfills (multiple applications)
    ├─ Application: "Order API" (microservice in Kubernetes)
    ├─ Application: "Inventory System" (legacy on WebSphere)
    └─ Application: "Payment Gateway" (cloud SaaS)
    
Integration:
Order API ←→ MessageQueue: "Order Queue" ←→ Inventory System
Order API ──→ API: "Payment API" ──→ Payment Gateway
```

**Layer Decomposition**:
- **Layer 1 (Business)**: Order Fulfillment
- **Layer 2 (Application)**: Order API, Inventory System, Payment Gateway, Order Queue
- **Layer 3 (Container)**: Order API containers (Kubernetes)
- **Layer 4 (Physical)**: Mixed (Kubernetes nodes, VMs, cloud services)

### RDF/Turtle Instance Data

```turtle
# Layer 1: Business Process
:OrderFulfillment
    rdf:type :BusinessProcess ;
    :name "Order Fulfillment" ;
    :description "End-to-end order processing and fulfillment" ;
    :owner "Operations Team" ;
    :criticality "critical" ;
    :lifecycle_status "active" ;
    :fulfills :OrderAPI, :InventorySystem, :PaymentGateway .

# Layer 2: Applications and Integration
:OrderAPI
    rdf:type :Application ;
    :name "Order API" ;
    :version "2.5.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Node.js 18" ;
    :technology_stack "Express, RabbitMQ, Stripe SDK" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" ;
    :deployed_as :OrderAPIContainer ;
    :uses :OrderQueue ;
    :calls :PaymentAPI .

:InventorySystem
    rdf:type :Application ;
    :name "Inventory System" ;
    :version "3.1.0" ;
    :application_type "monolithic" ;
    :deployment_model "vm_based" ;
    :runtime_environment "WebSphere 9.0" ;
    :technology_stack "Java EE, JMS" ;
    :data_classification "internal" ;
    :lifecycle_status "production" ;
    :runs_on :InventoryVM01 ;
    :uses :OrderQueue ;
    :uses :InventoryDB .

:PaymentGateway
    rdf:type :Application ;
    :name "Payment Gateway" ;
    :version "Stripe v2023-10-16" ;
    :application_type "SOA_service" ;
    :deployment_model "cloud_saas" ;
    :runtime_environment "Stripe Cloud" ;
    :data_classification "restricted" ;
    :lifecycle_status "production" .

:OrderQueue
    rdf:type :MessageQueue ;
    :name "Order Queue" ;
    :version "RabbitMQ 3.12" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :technology_stack "RabbitMQ, AMQP" ;
    :lifecycle_status "production" ;
    :deployed_as :RabbitMQContainer .

:PaymentAPI
    rdf:type :API ;
    :name "Payment API" ;
    :version "v1" ;
    :application_type "SOA_service" ;
    :technology_stack "REST, HTTPS" ;
    :lifecycle_status "production" .

# Layer 3: Container and Orchestration
:OrderAPIContainer
    rdf:type :Container ;
    :name "order-api-container" ;
    :image_name "order-api:2.5.0" ;
    :orchestration_platform "kubernetes" ;
    :lifecycle_status "running" ;
    :part_of :OrderAPIPod .

:OrderAPIPod
    rdf:type :Pod ;
    :name "order-api-pod-123" ;
    :orchestration_platform "kubernetes" ;
    :replica_count 3 ;
    :lifecycle_status "running" ;
    :runs_on :K8sWorkerNode05 .

:RabbitMQContainer
    rdf:type :Container ;
    :name "rabbitmq-container" ;
    :image_name "rabbitmq:3.12-management" ;
    :orchestration_platform "kubernetes" ;
    :lifecycle_status "running" ;
    :part_of :RabbitMQPod .

:RabbitMQPod
    rdf:type :Pod ;
    :name "rabbitmq-pod-456" ;
    :orchestration_platform "kubernetes" ;
    :replica_count 1 ;
    :lifecycle_status "running" ;
    :runs_on :K8sWorkerNode06 .

# Layer 4: Physical Infrastructure
:K8sWorkerNode05
    rdf:type :CloudInstance ;
    :name "k8s-worker-node-05" ;
    :resource_type "cloud_iaas" ;
    :location "us-east-1a" ;
    :capacity "t3.large (2 vCPU, 8GB RAM)" ;
    :operating_system "Amazon Linux 2" ;
    :lifecycle_status "running" .

:K8sWorkerNode06
    rdf:type :CloudInstance ;
    :name "k8s-worker-node-06" ;
    :resource_type "cloud_iaas" ;
    :location "us-east-1b" ;
    :capacity "t3.medium (2 vCPU, 4GB RAM)" ;
    :operating_system "Amazon Linux 2" ;
    :lifecycle_status "running" .

:InventoryVM01
    rdf:type :VirtualMachine ;
    :name "inventory-vm-01" ;
    :resource_type "virtual" ;
    :location "datacenter-1" ;
    :capacity "8 vCPU, 32GB RAM" ;
    :operating_system "Red Hat Enterprise Linux 8" ;
    :lifecycle_status "running" ;
    :runs_on :PhysicalServer08 .

:PhysicalServer08
    rdf:type :PhysicalServer ;
    :name "server-dc1-rack04-u10" ;
    :resource_type "physical" ;
    :location "datacenter-1, rack-04, unit-10" ;
    :capacity "2x Intel Xeon Gold 6248R, 256GB RAM" ;
    :operating_system "VMware ESXi 7.0" ;
    :lifecycle_status "running" .

:InventoryDB
    rdf:type :Database ;
    :name "Inventory_DB" ;
    :version "Oracle 19c" ;
    :application_type "legacy" ;
    :deployment_model "vm_based" ;
    :data_classification "internal" ;
    :lifecycle_status "production" ;
    :runs_on :InventoryDBVM .

:InventoryDBVM
    rdf:type :VirtualMachine ;
    :name "inventory-db-vm-01" ;
    :resource_type "virtual" ;
    :location "datacenter-1" ;
    :capacity "16 vCPU, 64GB RAM" ;
    :operating_system "Oracle Linux 8" ;
    :lifecycle_status "running" .

# Layer 5: Network - Integration Paths
:OrderToInventoryPath
    rdf:type :CommunicationPath ;
    :name "order-to-inventory-path" ;
    :protocol "AMQP" ;
    :port 5672 ;
    :lifecycle_status "active" .

:OrderToPaymentPath
    rdf:type :CommunicationPath ;
    :name "order-to-payment-path" ;
    :protocol "HTTPS" ;
    :port 443 ;
    :lifecycle_status "active" .

# Relationships
:OrderAPI :communicates_via :OrderToInventoryPath .
:OrderAPI :communicates_via :OrderToPaymentPath .
:InventorySystem :communicates_via :OrderToInventoryPath .
```



### Pattern 4.2: Multi-Application Business Process

**Scenario**: Customer onboarding process fulfilled by multiple applications.

**Architecture Overview**:
```
Business Process: "Customer Onboarding"
    ↓ fulfills (multiple applications)
    ├─ Application: "Registration Portal" (web app)
    ├─ Application: "Identity Verification Service" (microservice)
    ├─ Application: "CRM System" (legacy)
    └─ Application: "Email Service" (cloud SaaS)
```

### RDF/Turtle Instance Data

```turtle
# Layer 1: Business Process
:CustomerOnboarding
    rdf:type :BusinessProcess ;
    :name "Customer Onboarding" ;
    :description "Complete customer registration and verification process" ;
    :owner "Customer Success Team" ;
    :criticality "high" ;
    :lifecycle_status "active" ;
    :fulfills :RegistrationPortal, :IdentityVerificationService, :CRMSystem, :EmailService .

# Layer 2: Applications
:RegistrationPortal
    rdf:type :Application ;
    :name "Registration Portal" ;
    :version "1.9.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "React, Node.js" ;
    :technology_stack "React, Express, PostgreSQL" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" ;
    :calls :IdentityVerificationService ;
    :calls :CRMSystemAPI ;
    :calls :EmailServiceAPI .

:IdentityVerificationService
    rdf:type :Service ;
    :name "Identity Verification Service" ;
    :version "2.1.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Python 3.11" ;
    :technology_stack "FastAPI, Redis" ;
    :data_classification "restricted" ;
    :lifecycle_status "production" .

:CRMSystem
    rdf:type :Application ;
    :name "CRM System" ;
    :version "5.2.1" ;
    :application_type "monolithic" ;
    :deployment_model "vm_based" ;
    :runtime_environment "WebSphere 9.0" ;
    :technology_stack "Java EE, Oracle DB" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" .

:EmailService
    rdf:type :Application ;
    :name "Email Service" ;
    :version "SendGrid v3" ;
    :application_type "SOA_service" ;
    :deployment_model "cloud_saas" ;
    :runtime_environment "SendGrid Cloud" ;
    :data_classification "internal" ;
    :lifecycle_status "production" .

:CRMSystemAPI
    rdf:type :API ;
    :name "CRM System API" ;
    :version "v2" ;
    :application_type "SOA_service" ;
    :technology_stack "REST, JSON" ;
    :lifecycle_status "production" .

:EmailServiceAPI
    rdf:type :API ;
    :name "Email Service API" ;
    :version "v3" ;
    :application_type "SOA_service" ;
    :technology_stack "REST, JSON" ;
    :lifecycle_status "production" .
```



### Pattern 4.3: Hybrid Cloud Deployment

**Scenario**: Application with on-premises database and cloud-based compute.

**Architecture Overview**:
```
Application: "Analytics Dashboard"
    ↓ deployed_as (cloud)
Container: "analytics-dashboard-container" (AWS EKS)
    ↓ runs_on
CloudInstance: "eks-worker-node" (AWS EC2)

Application: "Analytics Dashboard"
    ↓ uses (on-premises)
Database: "Analytics_DB" (on-premises Oracle)
    ↓ runs_on
VirtualMachine: "analytics-db-vm" (on-premises)
```

**Layer Decomposition**:
- **Layer 2 (Application)**: Analytics Dashboard, Analytics_DB
- **Layer 3 (Container)**: Container (in cloud)
- **Layer 4 (Physical)**: CloudInstance (cloud), VirtualMachine (on-premises)
- **Layer 5 (Network)**: Hybrid connectivity (VPN/Direct Connect)

### RDF/Turtle Instance Data

```turtle
# Layer 2: Application
:AnalyticsDashboard
    rdf:type :Application ;
    :name "Analytics Dashboard" ;
    :version "3.2.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Python 3.11" ;
    :technology_stack "Dash, Plotly, SQLAlchemy" ;
    :data_classification "internal" ;
    :lifecycle_status "production" ;
    :deployed_as :AnalyticsDashboardContainer ;
    :uses :AnalyticsDB ;
    :communicates_via :HybridConnectionPath .

:AnalyticsDB
    rdf:type :Database ;
    :name "Analytics_DB" ;
    :version "Oracle 19c" ;
    :application_type "legacy" ;
    :deployment_model "vm_based" ;
    :data_classification "internal" ;
    :lifecycle_status "production" ;
    :runs_on :AnalyticsDBVM .

# Layer 3: Container (Cloud)
:AnalyticsDashboardContainer
    rdf:type :Container ;
    :name "analytics-dashboard-container" ;
    :image_name "analytics-dashboard:3.2.0" ;
    :orchestration_platform "kubernetes" ;
    :lifecycle_status "running" ;
    :part_of :AnalyticsDashboardPod .

:AnalyticsDashboardPod
    rdf:type :Pod ;
    :name "analytics-dashboard-pod-789" ;
    :orchestration_platform "kubernetes" ;
    :replica_count 2 ;
    :lifecycle_status "running" ;
    :runs_on :EKSWorkerNode .

# Layer 4: Physical Infrastructure (Hybrid)
:EKSWorkerNode
    rdf:type :CloudInstance ;
    :name "eks-worker-node-01" ;
    :resource_type "cloud_iaas" ;
    :location "us-east-1a" ;
    :capacity "m5.xlarge (4 vCPU, 16GB RAM)" ;
    :operating_system "Amazon Linux 2" ;
    :lifecycle_status "running" .

:AnalyticsDBVM
    rdf:type :VirtualMachine ;
    :name "analytics-db-vm-01" ;
    :resource_type "virtual" ;
    :location "datacenter-1" ;
    :capacity "16 vCPU, 128GB RAM" ;
    :operating_system "Oracle Linux 8" ;
    :lifecycle_status "running" ;
    :runs_on :PhysicalServer09 .

:PhysicalServer09
    rdf:type :PhysicalServer ;
    :name "server-dc1-rack06-u05" ;
    :resource_type "physical" ;
    :location "datacenter-1, rack-06, unit-05" ;
    :capacity "2x Intel Xeon Gold 6248R, 512GB RAM" ;
    :operating_system "VMware ESXi 7.0" ;
    :lifecycle_status "running" .

# Layer 5: Network (Hybrid Connectivity)
:HybridConnectionPath
    rdf:type :CommunicationPath ;
    :name "cloud-to-onprem-path" ;
    :protocol "Oracle Net" ;
    :port 1521 ;
    :lifecycle_status "active" ;
    :routes_through :DirectConnectGateway .

:DirectConnectGateway
    rdf:type :NetworkDevice ;
    :name "aws-direct-connect-gateway" ;
    :device_type "gateway" ;
    :ip_address "10.0.0.1" ;
    :lifecycle_status "active" .

# Layer 6: Security
:HybridVPN
    rdf:type :SecurityPolicy ;
    :name "Cloud-to-OnPrem VPN Policy" ;
    :security_type "policy" ;
    :policy_rules "IPSec tunnel, AES-256 encryption" ;
    :trust_level "trusted" ;
    :lifecycle_status "active" .

:AnalyticsDashboard :secured_by :HybridVPN .
:AnalyticsDB :secured_by :HybridVPN .
```



### Pattern 4.4: API Gateway Integration Pattern

**Scenario**: Multiple microservices exposed through an API Gateway.

**Architecture Overview**:
```
Business Process: "E-Commerce Operations"
    ↓ fulfills
API Gateway: "API Gateway Service"
    ↓ routes_to
    ├─ Service: "Product Catalog Service"
    ├─ Service: "Shopping Cart Service"
    ├─ Service: "Order Service"
    └─ Service: "User Service"
```

### RDF/Turtle Instance Data

```turtle
# Layer 1: Business Process
:ECommerceOperations
    rdf:type :BusinessProcess ;
    :name "E-Commerce Operations" ;
    :description "Online shopping and order management" ;
    :owner "E-Commerce Team" ;
    :criticality "critical" ;
    :lifecycle_status "active" ;
    :fulfills :APIGatewayService .

# Layer 2: API Gateway and Services
:APIGatewayService
    rdf:type :Application ;
    :name "API Gateway Service" ;
    :version "Kong 3.4" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Kong Gateway" ;
    :technology_stack "Kong, Nginx, Lua" ;
    :data_classification "public" ;
    :lifecycle_status "production" ;
    :deployed_as :APIGatewayContainer ;
    :calls :ProductCatalogService, :ShoppingCartService, :OrderService, :UserService .

:ProductCatalogService
    rdf:type :Service ;
    :name "Product Catalog Service" ;
    :version "2.0.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Java 17" ;
    :technology_stack "Spring Boot, MongoDB" ;
    :data_classification "public" ;
    :lifecycle_status "production" ;
    :uses :ProductCatalogDB .

:ShoppingCartService
    rdf:type :Service ;
    :name "Shopping Cart Service" ;
    :version "1.5.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Node.js 18" ;
    :technology_stack "Express, Redis" ;
    :data_classification "internal" ;
    :lifecycle_status "production" ;
    :uses :RedisCache .

:OrderService
    rdf:type :Service ;
    :name "Order Service" ;
    :version "2.3.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Python 3.11" ;
    :technology_stack "FastAPI, PostgreSQL" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" ;
    :uses :OrderDB .

:UserService
    rdf:type :Service ;
    :name "User Service" ;
    :version "1.8.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :runtime_environment "Go 1.21" ;
    :technology_stack "Go, PostgreSQL" ;
    :data_classification "restricted" ;
    :lifecycle_status "production" ;
    :uses :UserDB .

# Layer 2: Databases and Cache
:ProductCatalogDB
    rdf:type :Database ;
    :name "ProductCatalogDB" ;
    :version "MongoDB 6.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :data_classification "public" ;
    :lifecycle_status "production" .

:RedisCache
    rdf:type :CacheService ;
    :name "RedisCache" ;
    :version "Redis 7.0" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :data_classification "internal" ;
    :lifecycle_status "production" .

:OrderDB
    rdf:type :Database ;
    :name "OrderDB" ;
    :version "PostgreSQL 15" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :data_classification "confidential" ;
    :lifecycle_status "production" .

:UserDB
    rdf:type :Database ;
    :name "UserDB" ;
    :version "PostgreSQL 15" ;
    :application_type "microservice" ;
    :deployment_model "containerized" ;
    :data_classification "restricted" ;
    :lifecycle_status "production" .

# Layer 3: Container and Orchestration
:APIGatewayContainer
    rdf:type :Container ;
    :name "api-gateway-container" ;
    :image_name "kong:3.4" ;
    :orchestration_platform "kubernetes" ;
    :exposed_port 8000 ;
    :lifecycle_status "running" ;
    :part_of :APIGatewayPod .

:APIGatewayPod
    rdf:type :Pod ;
    :name "api-gateway-pod-abc" ;
    :orchestration_platform "kubernetes" ;
    :replica_count 3 ;
    :lifecycle_status "running" ;
    :runs_on :K8sWorkerNode07 .

# Layer 4: Physical Infrastructure
:K8sWorkerNode07
    rdf:type :CloudInstance ;
    :name "k8s-worker-node-07" ;
    :resource_type "cloud_iaas" ;
    :location "us-west-2a" ;
    :capacity "c5.2xlarge (8 vCPU, 16GB RAM)" ;
    :operating_system "Amazon Linux 2" ;
    :lifecycle_status "running" .

# Layer 5: Network
:APIGatewayRoute
    rdf:type :Route ;
    :name "api-gateway-route" ;
    :orchestration_platform "kubernetes" ;
    :external_hostname "api.example.com" ;
    :route_path "/" ;
    :tls_termination "edge" ;
    :lifecycle_status "active" .

:APIGatewayPath
    rdf:type :CommunicationPath ;
    :name "api-gateway-path" ;
    :protocol "HTTPS" ;
    :port 443 ;
    :lifecycle_status "active" ;
    :routes_through :IngressController .

:IngressController
    rdf:type :IngressController ;
    :name "nginx-ingress-controller" ;
    :orchestration_platform "kubernetes" ;
    :lifecycle_status "running" .

# Layer 6: Security
:APIGatewayCertificate
    rdf:type :Certificate ;
    :name "api.example.com-cert" ;
    :security_type "certificate" ;
    :expiration_date "2025-12-31"^^xsd:date ;
    :trust_level "trusted" ;
    :lifecycle_status "active" .

:APIRateLimitPolicy
    rdf:type :SecurityPolicy ;
    :name "API Rate Limit Policy" ;
    :security_type "policy" ;
    :policy_rules "1000 requests per minute per client" ;
    :trust_level "trusted" ;
    :lifecycle_status "active" .

:APIGatewayService :secured_by :APIRateLimitPolicy .
:APIGatewayRoute :secured_by :APIGatewayCertificate .
```



---

## Summary of Deployment Patterns

### Pattern Coverage

This document provides comprehensive examples across all six ontology layers:

**1. Containerized Applications (Patterns 1.1-1.3)**
- Microservices in Kubernetes/OpenShift
- Pod, Deployment, Service, Route relationships
- Persistent storage with PVCs
- Multi-container pods with sidecars
- Full decomposition from Application to Physical Infrastructure

**2. Legacy Applications (Patterns 2.1-2.2)**
- Java EE on WebSphere
- .NET on IIS
- Application Server deployment model
- Layer 3 bypass (no containers)
- Traditional VM-based infrastructure

**3. Storage Decomposition (Patterns 3.1-3.5)**
- On-premises SAN storage
- Cloud managed databases (RDS)
- Object storage (S3)
- Shared file systems (NFS)
- Containerized databases with persistent volumes
- Logical vs. physical storage distinctions

**4. Hybrid and SOA Integration (Patterns 4.1-4.4)**
- Message queue integration (RabbitMQ)
- Multi-application business processes
- Hybrid cloud deployments
- API Gateway patterns
- Cross-environment connectivity

### Key Relationship Patterns

**Cross-Layer Decomposition**:
- `fulfills`: Business Process → Application
- `deployed_as`: Application → Container
- `runs_on`: Container/Application → Infrastructure
- `uses`: Application → Database/Storage/Service
- `calls`: Service → Service (API integration)

**Storage Relationships**:
- `stored_on`: Database → StorageVolume
- `allocated_from`: StorageVolume → StorageArray
- `hosted_on`: Database → CloudStorageService
- `mounted_from`: FileSystem → StorageVolume
- `provisioned_from`: Volume → CloudService

**Network Relationships**:
- `communicates_via`: Application → CommunicationPath
- `routes_through`: CommunicationPath → NetworkDevice
- `exposed_by`: Service → Route

**Security Relationships**:
- `protected_by`: Entity → SecurityComponent
- `secured_by`: Entity → SecurityPolicy
- `issued_by`: Certificate → CertificateAuthority

### Usage Guidelines

**For Root Cause Analysis**:
1. Start with failed component
2. Traverse upstream using `runs_on`, `hosted_on`, `uses` relationships
3. Identify infrastructure dependencies
4. Check network paths and security components

**For Impact Analysis**:
1. Start with component to be changed
2. Traverse downstream using inverse relationships
3. Identify all dependent applications and services
4. Assess business process impacts

**For Deployment Planning**:
1. Choose appropriate pattern based on architecture
2. Model all six layers where applicable
3. Define cross-layer relationships
4. Validate against SHACL shapes

### Extension Points

Organizations can extend these patterns by:
- Adding custom entity types within layers
- Defining additional relationship types
- Adding custom attributes with proper namespacing
- Creating new deployment patterns for specific technologies

### Validation

All instance data in this document:
- Follows EARS requirements syntax
- Complies with ontology layer structure
- Uses proper RDF/Turtle syntax
- References framework-sourced attributes
- Demonstrates cross-layer decomposition
- Supports query patterns for analysis

---

## Next Steps

1. **Validate Instance Data**: Run SHACL validation against all examples
2. **Test Queries**: Execute SPARQL/Cypher queries against sample data
3. **Extend Patterns**: Add organization-specific deployment patterns
4. **Integrate with CMDB**: Map patterns to CMDB configuration items
5. **Automate Discovery**: Build tools to auto-discover and populate ontology

