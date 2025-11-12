# Layer 2: Application Layer - Complete Specification

## Overview

This document provides the complete formal specification for Layer 2 (Application Layer) of the IT Infrastructure and Application Dependency Ontology. The Application Layer represents software applications, services, and data objects that fulfill business requirements.

**Layer Purpose**: Represents software applications, services, and data objects that fulfill business requirements.

**Layer Scope**: All logical software components and data services, independent of their deployment model (containerized, VM-based, cloud-native, or legacy).

**Framework Sources**: 
- TOGAF Application Architecture metamodel
- CIM (Common Information Model) Application and Database schemas
- ITIL Application Management
- ArchiMate Application Layer

---

## Entity Type Specifications

### 1. Application

**Definition**: A software system that provides business functionality to end users or other systems.

**OWL Class Definition**:
```turtle
:Application
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Application" ;
  rdfs:comment "A software system that provides business functionality" ;
  skos:definition "An application is a software system that delivers business capabilities through one or more application components" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | TOGAF, CIM | Application name or identifier |
| description | xsd:string | 0..1 | optional | TOGAF | Purpose and scope of the application |
| version | xsd:string | 0..1 | optional | TOGAF, CIM | Version identifier (e.g., "2.5.1", "v3.0") |
| owner | xsd:string | 0..1 | optional | TOGAF | Business or technical owner |
| application_type | xsd:string | 1..1 | enum | TOGAF | Architecture pattern: monolithic, SOA_service, microservice, batch, legacy |
| deployment_model | xsd:string | 1..1 | enum | CIM | Deployment approach: containerized, vm_based, bare_metal, serverless, cloud_managed |
| runtime_environment | xsd:string | 0..1 | optional | CIM | Runtime platform (e.g., "Node.js 18", "Python 3.11", "JVM 11") |
| technology_stack | xsd:string | 0..1 | optional | TOGAF | Primary technologies (e.g., "Java EE", ".NET Core", "React/Node.js") |
| data_classification | xsd:string | 0..1 | enum | ITIL | Data sensitivity: public, internal, confidential, restricted |
| lifecycle_status | xsd:string | 1..1 | enum | TOGAF, ITIL | Current state: development, testing, production, deprecated, retired |
| criticality | xsd:string | 0..1 | enum | ITIL | Business importance: critical, high, medium, low |
| availability_requirement | xsd:decimal | 0..1 | optional | ITIL | Required availability percentage (e.g., 99.9) |

**Enumeration Values**:

- **application_type**: `monolithic`, `SOA_service`, `microservice`, `batch`, `legacy`, `mobile_app`, `web_app`
- **deployment_model**: `containerized`, `vm_based`, `bare_metal`, `serverless`, `cloud_managed`
- **data_classification**: `public`, `internal`, `confidential`, `restricted`
- **lifecycle_status**: `development`, `testing`, `staging`, `production`, `deprecated`, `retired`
- **criticality**: `critical`, `high`, `medium`, `low`

**SHACL Validation Shape**:
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
  ] ;
  sh:property [
    sh:path :application_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "monolithic" "SOA_service" "microservice" "batch" "legacy" "mobile_app" "web_app" ) ;
  ] ;
  sh:property [
    sh:path :deployment_model ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "containerized" "vm_based" "bare_metal" "serverless" "cloud_managed" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "development" "testing" "staging" "production" "deprecated" "retired" ) ;
  ] ;
  sh:property [
    sh:path :availability_requirement ;
    sh:maxCount 1 ;
    sh:datatype xsd:decimal ;
    sh:minInclusive 0.0 ;
    sh:maxInclusive 100.0 ;
  ] .
```

---

### 2. ApplicationComponent

**Definition**: A modular part of an application that provides specific functionality (e.g., servlet, EJB, web service, module).

**OWL Class Definition**:
```turtle
:ApplicationComponent
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Application Component" ;
  rdfs:comment "A modular part of an application" ;
  skos:definition "An application component is a self-contained unit of functionality within an application" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | TOGAF | Component name |
| description | xsd:string | 0..1 | optional | TOGAF | Component purpose |
| component_type | xsd:string | 1..1 | enum | TOGAF | Type: servlet, ejb, web_service, rest_api, module, library, function |
| technology | xsd:string | 0..1 | optional | TOGAF | Implementation technology (e.g., "Java Servlet", "Spring Bean") |
| interface_specification | xsd:string | 0..1 | optional | TOGAF | API or interface definition |
| lifecycle_status | xsd:string | 1..1 | enum | TOGAF | Current state: active, deprecated, retired |

**Enumeration Values**:
- **component_type**: `servlet`, `ejb`, `web_service`, `rest_api`, `soap_service`, `module`, `library`, `function`, `stored_procedure`
- **lifecycle_status**: `active`, `deprecated`, `retired`

**SHACL Validation Shape**:
```turtle
:ApplicationComponentShape
  a sh:NodeShape ;
  sh:targetClass :ApplicationComponent ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :component_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "servlet" "ejb" "web_service" "rest_api" "soap_service" "module" "library" "function" "stored_procedure" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "deprecated" "retired" ) ;
  ] .
```

---

### 3. ApplicationServer

**Definition**: A runtime environment that hosts and executes applications (e.g., WebSphere, WebLogic, JBoss, Tomcat, IIS).

**OWL Class Definition**:
```turtle
:ApplicationServer
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Application Server" ;
  rdfs:comment "A runtime environment for hosting applications" ;
  skos:definition "An application server provides runtime services and infrastructure for executing applications" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Server instance name |
| server_type | xsd:string | 1..1 | enum | CIM | Server product: websphere, weblogic, jboss, tomcat, iis, nginx, apache |
| version | xsd:string | 0..1 | optional | CIM | Server version (e.g., "9.0.5", "8.5") |
| configuration | xsd:string | 0..1 | optional | CIM | Configuration profile or settings |
| port | xsd:integer | 0..* | optional | CIM | Listening ports |
| lifecycle_status | xsd:string | 1..1 | enum | ITIL | Current state: running, stopped, failed, maintenance |

**Enumeration Values**:
- **server_type**: `websphere`, `weblogic`, `jboss`, `wildfly`, `tomcat`, `iis`, `nginx`, `apache`, `node`, `gunicorn`, `uvicorn`
- **lifecycle_status**: `running`, `stopped`, `failed`, `maintenance`, `starting`, `stopping`

**SHACL Validation Shape**:
```turtle
:ApplicationServerShape
  a sh:NodeShape ;
  sh:targetClass :ApplicationServer ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :server_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "websphere" "weblogic" "jboss" "wildfly" "tomcat" "iis" "nginx" "apache" "node" "gunicorn" "uvicorn" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "running" "stopped" "failed" "maintenance" "starting" "stopping" ) ;
  ] .
```

---

### 4. Service

**Definition**: A service in SOA or microservices architecture that provides specific business or technical capabilities.

**OWL Class Definition**:
```turtle
:Service
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Service" ;
  rdfs:comment "A service in SOA or microservices architecture" ;
  skos:definition "A service is a self-contained unit of functionality that can be accessed remotely and independently deployed" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | TOGAF | Service name |
| description | xsd:string | 0..1 | optional | TOGAF | Service purpose |
| service_type | xsd:string | 1..1 | enum | TOGAF | Type: business_service, technical_service, integration_service |
| architecture_style | xsd:string | 1..1 | enum | TOGAF | Style: SOA, microservice, REST, SOAP, gRPC |
| endpoint_url | xsd:anyURI | 0..1 | optional | TOGAF | Service endpoint URL |
| protocol | xsd:string | 0..1 | optional | TOGAF | Communication protocol (HTTP, HTTPS, AMQP, etc.) |
| contract_specification | xsd:string | 0..1 | optional | TOGAF | Service contract or interface definition |
| lifecycle_status | xsd:string | 1..1 | enum | TOGAF | Current state: active, deprecated, retired |

**Enumeration Values**:
- **service_type**: `business_service`, `technical_service`, `integration_service`, `data_service`
- **architecture_style**: `SOA`, `microservice`, `REST`, `SOAP`, `gRPC`, `GraphQL`, `message_driven`
- **lifecycle_status**: `active`, `deprecated`, `retired`

**SHACL Validation Shape**:
```turtle
:ServiceShape
  a sh:NodeShape ;
  sh:targetClass :Service ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :service_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "business_service" "technical_service" "integration_service" "data_service" ) ;
  ] ;
  sh:property [
    sh:path :architecture_style ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "SOA" "microservice" "REST" "SOAP" "gRPC" "GraphQL" "message_driven" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "deprecated" "retired" ) ;
  ] .
```

---

### 5. API

**Definition**: An application programming interface that defines how software components interact.

**OWL Class Definition**:
```turtle
:API
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "API" ;
  rdfs:comment "An application programming interface" ;
  skos:definition "An API defines the contract for how software components communicate and exchange data" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | TOGAF | API name |
| description | xsd:string | 0..1 | optional | TOGAF | API purpose |
| api_type | xsd:string | 1..1 | enum | TOGAF | Type: REST, SOAP, GraphQL, gRPC, WebSocket |
| version | xsd:string | 0..1 | optional | TOGAF | API version (e.g., "v1", "2.0") |
| endpoint_url | xsd:anyURI | 0..1 | optional | TOGAF | Base URL for API |
| specification_format | xsd:string | 0..1 | enum | TOGAF | Spec format: OpenAPI, WSDL, GraphQL_Schema, Protobuf |
| specification_url | xsd:anyURI | 0..1 | optional | TOGAF | URL to API specification document |
| authentication_method | xsd:string | 0..1 | enum | TOGAF | Auth method: OAuth2, API_Key, Basic, JWT, mTLS |
| lifecycle_status | xsd:string | 1..1 | enum | TOGAF | Current state: active, deprecated, retired |

**Enumeration Values**:
- **api_type**: `REST`, `SOAP`, `GraphQL`, `gRPC`, `WebSocket`, `WebHook`
- **specification_format**: `OpenAPI`, `WSDL`, `GraphQL_Schema`, `Protobuf`, `AsyncAPI`
- **authentication_method**: `OAuth2`, `API_Key`, `Basic`, `JWT`, `mTLS`, `SAML`, `none`
- **lifecycle_status**: `active`, `deprecated`, `retired`

**SHACL Validation Shape**:
```turtle
:APIShape
  a sh:NodeShape ;
  sh:targetClass :API ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :api_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "REST" "SOAP" "GraphQL" "gRPC" "WebSocket" "WebHook" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "deprecated" "retired" ) ;
  ] .
```

---

## Storage Entity Type Specifications

### 6. Database

**Definition**: A logical database system that stores and manages structured or unstructured data.

**OWL Class Definition**:
```turtle
:Database
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Database" ;
  rdfs:comment "A logical database system" ;
  skos:definition "A database is a system for storing, organizing, and retrieving data with query capabilities" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Database name |
| description | xsd:string | 0..1 | optional | TOGAF | Database purpose |
| database_type | xsd:string | 1..1 | enum | CIM | Type: relational, nosql_document, nosql_keyvalue, nosql_graph, nosql_columnar, timeseries |
| database_product | xsd:string | 1..1 | optional | CIM | Product: Oracle, PostgreSQL, MySQL, MongoDB, Cassandra, Redis, Neo4j |
| version | xsd:string | 0..1 | optional | CIM | Database version |
| data_classification | xsd:string | 0..1 | enum | ITIL | Data sensitivity: public, internal, confidential, restricted |
| size_gb | xsd:decimal | 0..1 | optional | CIM | Database size in gigabytes |
| backup_frequency | xsd:string | 0..1 | optional | ITIL | Backup schedule (e.g., "daily", "hourly") |
| lifecycle_status | xsd:string | 1..1 | enum | ITIL | Current state: active, maintenance, failed, retired |

**Enumeration Values**:
- **database_type**: `relational`, `nosql_document`, `nosql_keyvalue`, `nosql_graph`, `nosql_columnar`, `nosql_wide_column`, `timeseries`, `in_memory`
- **database_product**: `Oracle`, `PostgreSQL`, `MySQL`, `MariaDB`, `SQL_Server`, `MongoDB`, `Cassandra`, `Redis`, `Neo4j`, `DynamoDB`, `CosmosDB`, `Elasticsearch`
- **data_classification**: `public`, `internal`, `confidential`, `restricted`
- **lifecycle_status**: `active`, `maintenance`, `failed`, `retired`

**SHACL Validation Shape**:
```turtle
:DatabaseShape
  a sh:NodeShape ;
  sh:targetClass :Database ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :database_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "relational" "nosql_document" "nosql_keyvalue" "nosql_graph" "nosql_columnar" "nosql_wide_column" "timeseries" "in_memory" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "maintenance" "failed" "retired" ) ;
  ] .
```

---

### 7. DatabaseInstance

**Definition**: A specific database instance or schema within a database system.

**OWL Class Definition**:
```turtle
:DatabaseInstance
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Database Instance" ;
  rdfs:comment "A specific database instance or schema" ;
  skos:definition "A database instance is a specific running instance or logical schema within a database system" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Instance or schema name |
| instance_identifier | xsd:string | 0..1 | optional | CIM | Unique instance ID (e.g., SID for Oracle) |
| connection_string | xsd:string | 0..1 | optional | CIM | Connection string or JDBC URL |
| port | xsd:integer | 0..1 | optional | CIM | Database port number |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Current state: running, stopped, failed |

**Enumeration Values**:
- **lifecycle_status**: `running`, `stopped`, `failed`, `starting`, `stopping`

**SHACL Validation Shape**:
```turtle
:DatabaseInstanceShape
  a sh:NodeShape ;
  sh:targetClass :DatabaseInstance ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "running" "stopped" "failed" "starting" "stopping" ) ;
  ] .
```

---

### 8. DataObject

**Definition**: A logical data entity or schema element (tables, collections, documents, views).

**OWL Class Definition**:
```turtle
:DataObject
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Data Object" ;
  rdfs:comment "A logical data entity or schema element" ;
  skos:definition "A data object represents a logical data structure such as a table, collection, document, or view" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | TOGAF | Object name (table, collection, etc.) |
| object_type | xsd:string | 1..1 | enum | TOGAF | Type: table, view, collection, document, index |
| schema_name | xsd:string | 0..1 | optional | CIM | Schema or namespace |
| data_classification | xsd:string | 0..1 | enum | ITIL | Data sensitivity: public, internal, confidential, restricted |
| record_count | xsd:integer | 0..1 | optional | CIM | Approximate number of records |

**Enumeration Values**:
- **object_type**: `table`, `view`, `collection`, `document`, `index`, `materialized_view`, `stored_procedure`
- **data_classification**: `public`, `internal`, `confidential`, `restricted`

**SHACL Validation Shape**:
```turtle
:DataObjectShape
  a sh:NodeShape ;
  sh:targetClass :DataObject ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :object_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "table" "view" "collection" "document" "index" "materialized_view" "stored_procedure" ) ;
  ] .
```

---

### 9. FileStorageService

**Definition**: A logical file storage service providing hierarchical file system access (NFS, CIFS, mounted paths).

**OWL Class Definition**:
```turtle
:FileStorageService
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "File Storage Service" ;
  rdfs:comment "A logical file storage service" ;
  skos:definition "A file storage service provides hierarchical file system access with directories and files" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Storage service name |
| mount_path | xsd:string | 0..1 | optional | CIM | Mount point or path (e.g., "/mnt/data") |
| protocol | xsd:string | 1..1 | enum | CIM | Protocol: NFS, CIFS, SMB, local |
| capacity_gb | xsd:decimal | 0..1 | optional | CIM | Storage capacity in gigabytes |
| used_gb | xsd:decimal | 0..1 | optional | CIM | Used storage in gigabytes |
| lifecycle_status | xsd:string | 1..1 | enum | ITIL | Current state: active, maintenance, failed |

**Enumeration Values**:
- **protocol**: `NFS`, `CIFS`, `SMB`, `local`, `AFP`, `FTP`, `SFTP`
- **lifecycle_status**: `active`, `maintenance`, `failed`, `unmounted`

**SHACL Validation Shape**:
```turtle
:FileStorageServiceShape
  a sh:NodeShape ;
  sh:targetClass :FileStorageService ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :protocol ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "NFS" "CIFS" "SMB" "local" "AFP" "FTP" "SFTP" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "maintenance" "failed" "unmounted" ) ;
  ] .
```

**Distinction from ObjectStorageService**: File storage provides hierarchical directory structures with POSIX-like semantics, while object storage provides flat namespaces with key-value access.

---

### 10. ObjectStorageService

**Definition**: A logical object storage service providing key-value access to objects (S3 buckets, Azure Blob containers, GCS buckets).

**OWL Class Definition**:
```turtle
:ObjectStorageService
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Object Storage Service" ;
  rdfs:comment "A logical object storage service" ;
  skos:definition "An object storage service provides scalable storage with key-value access patterns" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Bucket or container name |
| storage_class | xsd:string | 0..1 | enum | Cloud APIs | Storage tier: standard, infrequent_access, archive, glacier |
| region | xsd:string | 0..1 | optional | Cloud APIs | Cloud region or location |
| access_policy | xsd:string | 0..1 | optional | Cloud APIs | Access control policy (public, private, etc.) |
| versioning_enabled | xsd:boolean | 0..1 | optional | Cloud APIs | Whether versioning is enabled |
| lifecycle_status | xsd:string | 1..1 | enum | ITIL | Current state: active, suspended, deleted |

**Enumeration Values**:
- **storage_class**: `standard`, `infrequent_access`, `archive`, `glacier`, `intelligent_tiering`
- **lifecycle_status**: `active`, `suspended`, `deleted`

**SHACL Validation Shape**:
```turtle
:ObjectStorageServiceShape
  a sh:NodeShape ;
  sh:targetClass :ObjectStorageService ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "suspended" "deleted" ) ;
  ] .
```

**Distinction from FileStorageService**: Object storage uses flat namespaces with HTTP/REST APIs and key-value semantics, optimized for cloud-scale storage. File storage uses hierarchical directories with file system protocols.

**Distinction from Database**: Object storage is optimized for unstructured data (files, blobs, media) with simple key-value access, while databases provide structured data with query capabilities.

---

### 11. CacheService

**Definition**: A caching layer that provides high-speed data access (Redis, Memcached, etc.).

**OWL Class Definition**:
```turtle
:CacheService
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Cache Service" ;
  rdfs:comment "A caching layer for high-speed data access" ;
  skos:definition "A cache service provides in-memory data storage for fast access to frequently used data" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Cache service name |
| cache_type | xsd:string | 1..1 | enum | CIM | Type: in_memory, distributed, local |
| cache_product | xsd:string | 0..1 | optional | CIM | Product: Redis, Memcached, Hazelcast, Ehcache |
| capacity_mb | xsd:decimal | 0..1 | optional | CIM | Cache capacity in megabytes |
| ttl_seconds | xsd:integer | 0..1 | optional | CIM | Default time-to-live in seconds |
| lifecycle_status | xsd:string | 1..1 | enum | ITIL | Current state: active, failed, maintenance |

**Enumeration Values**:
- **cache_type**: `in_memory`, `distributed`, `local`, `hybrid`
- **cache_product**: `Redis`, `Memcached`, `Hazelcast`, `Ehcache`, `Varnish`, `CDN`
- **lifecycle_status**: `active`, `failed`, `maintenance`

**SHACL Validation Shape**:
```turtle
:CacheServiceShape
  a sh:NodeShape ;
  sh:targetClass :CacheService ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :cache_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "in_memory" "distributed" "local" "hybrid" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "failed" "maintenance" ) ;
  ] .
```

---

### 12. MessageQueue

**Definition**: A message-oriented middleware component for asynchronous communication (MQ, RabbitMQ, Kafka).

**OWL Class Definition**:
```turtle
:MessageQueue
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Message Queue" ;
  rdfs:comment "A message-oriented middleware component" ;
  skos:definition "A message queue enables asynchronous communication between applications through message passing" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | TOGAF | Queue or topic name |
| queue_type | xsd:string | 1..1 | enum | TOGAF | Type: queue, topic, stream |
| messaging_product | xsd:string | 0..1 | optional | CIM | Product: RabbitMQ, Kafka, ActiveMQ, IBM_MQ, AWS_SQS |
| protocol | xsd:string | 0..1 | enum | TOGAF | Protocol: AMQP, MQTT, STOMP, JMS |
| persistence_enabled | xsd:boolean | 0..1 | optional | CIM | Whether messages are persisted |
| message_retention_hours | xsd:integer | 0..1 | optional | CIM | Message retention period in hours |
| lifecycle_status | xsd:string | 1..1 | enum | ITIL | Current state: active, failed, maintenance |

**Enumeration Values**:
- **queue_type**: `queue`, `topic`, `stream`, `exchange`
- **messaging_product**: `RabbitMQ`, `Kafka`, `ActiveMQ`, `IBM_MQ`, `AWS_SQS`, `AWS_SNS`, `Azure_ServiceBus`, `Google_PubSub`
- **protocol**: `AMQP`, `MQTT`, `STOMP`, `JMS`, `HTTP`, `Kafka_Protocol`
- **lifecycle_status**: `active`, `failed`, `maintenance`

**SHACL Validation Shape**:
```turtle
:MessageQueueShape
  a sh:NodeShape ;
  sh:targetClass :MessageQueue ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :queue_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "queue" "topic" "stream" "exchange" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "failed" "maintenance" ) ;
  ] .
```

---

## Application Layer Relationships

### Intra-Layer Relationships (within Application Layer)

#### 1. contains

**Definition**: An application contains application components.

**OWL Property Definition**:
```turtle
:contains
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Application ;
  rdfs:range :ApplicationComponent ;
  rdfs:label "contains" ;
  rdfs:comment "An application contains application components" .
```

**Cardinality**: 1 Application to many ApplicationComponents (1..*)

**Inverse Property**: `part_of`

---

#### 2. deployed_on

**Definition**: An application component is deployed on an application server.

**OWL Property Definition**:
```turtle
:deployed_on
  rdf:type owl:ObjectProperty ;
  rdfs:domain :ApplicationComponent ;
  rdfs:range :ApplicationServer ;
  rdfs:label "deployed on" ;
  rdfs:comment "An application component is deployed on an application server" .
```

**Cardinality**: Many ApplicationComponents to 1 ApplicationServer (*.1)

**Inverse Property**: `hosts_component`

---

#### 3. uses

**Definition**: An application uses a data service (Database, Cache, FileStorage, ObjectStorage).

**OWL Property Definition**:
```turtle
:uses
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Application ;
  rdfs:range [ owl:unionOf ( :Database :CacheService :FileStorageService :ObjectStorageService :MessageQueue ) ] ;
  rdfs:label "uses" ;
  rdfs:comment "An application uses a data or messaging service" .
```

**Cardinality**: Many Applications to many Services (*..*)

**Relationship Properties**:
- `criticality` (enum: critical, high, medium, low): Importance of the dependency
- `dependency_type` (enum: read_only, read_write, write_only): Access pattern
- `access_frequency` (enum: continuous, frequent, occasional, rare): Usage frequency

---

#### 4. calls

**Definition**: A service calls another service (service-to-service communication).

**OWL Property Definition**:
```turtle
:calls
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Service :Application ) ] ;
  rdfs:range [ owl:unionOf ( :Service :API ) ] ;
  rdfs:label "calls" ;
  rdfs:comment "A service or application calls another service or API" .
```

**Cardinality**: Many to many (*..*)

**Relationship Properties**:
- `criticality` (enum: critical, high, medium, low): Importance of the call
- `dependency_type` (enum: synchronous, asynchronous, batch): Communication pattern
- `protocol` (string): Communication protocol (HTTP, gRPC, etc.)

---

#### 5. exposes

**Definition**: An application exposes an API.

**OWL Property Definition**:
```turtle
:exposes
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Application :Service ) ] ;
  rdfs:range :API ;
  rdfs:label "exposes" ;
  rdfs:comment "An application or service exposes an API" .
```

**Cardinality**: 1 Application/Service to many APIs (1..*)

**Inverse Property**: `exposed_by`

---

#### 6. publishes_to / subscribes_to

**Definition**: An application publishes messages to or subscribes from a message queue.

**OWL Property Definition**:
```turtle
:publishes_to
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Application :Service ) ] ;
  rdfs:range :MessageQueue ;
  rdfs:label "publishes to" ;
  rdfs:comment "An application publishes messages to a message queue" .

:subscribes_to
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Application :Service ) ] ;
  rdfs:range :MessageQueue ;
  rdfs:label "subscribes to" ;
  rdfs:comment "An application subscribes to messages from a message queue" .
```

**Cardinality**: Many to many (*..*)

---

#### 7. stores_data_in

**Definition**: A database stores data in data objects (tables, collections).

**OWL Property Definition**:
```turtle
:stores_data_in
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Database :DatabaseInstance ) ] ;
  rdfs:range :DataObject ;
  rdfs:label "stores data in" ;
  rdfs:comment "A database stores data in data objects" .
```

**Cardinality**: 1 Database to many DataObjects (1..*)

**Inverse Property**: `contained_in`

---

### Cross-Layer Relationships

#### 8. deployed_as (Application Layer → Container Layer)

**Definition**: An application is deployed as containers.

**OWL Property Definition**:
```turtle
:deployed_as
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Application ;
  rdfs:range :Container ;  # Container is from Layer 3
  rdfs:label "deployed as" ;
  rdfs:comment "An application is deployed as containers" .
```

**Cardinality**: 1 Application to many Containers (1..*)

**Note**: This relationship is only applicable for containerized applications. Legacy applications skip Layer 3.

---

#### 9. runs_on (Application Layer → Physical Infrastructure Layer)

**Definition**: An application or application server runs on physical infrastructure (VM, physical server, cloud instance).

**OWL Property Definition**:
```turtle
:runs_on
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Application :ApplicationServer ) ] ;
  rdfs:range [ owl:unionOf ( :VirtualMachine :PhysicalServer :CloudInstance ) ] ;  # From Layer 4
  rdfs:label "runs on" ;
  rdfs:comment "An application or application server runs on physical infrastructure" .
```

**Cardinality**: Many Applications to 1 Infrastructure (*..1) or 1 Application to many Infrastructure (1..*) for distributed apps

**Relationship Properties**:
- `criticality` (enum: critical, high, medium, low): Importance of the infrastructure
- `resource_allocation` (string): Allocated resources (CPU, memory)

---

#### 10. hosted_on (Application Layer → Physical Infrastructure Layer)

**Definition**: A database or storage service is hosted on physical storage infrastructure.

**OWL Property Definition**:
```turtle
:hosted_on
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Database :FileStorageService :ObjectStorageService ) ] ;
  rdfs:range [ owl:unionOf ( :StorageVolume :CloudStorageService :VirtualMachine ) ] ;  # From Layer 4
  rdfs:label "hosted on" ;
  rdfs:comment "A database or storage service is hosted on physical infrastructure" .
```

**Cardinality**: Many to 1 or many to many depending on architecture

**Relationship Properties**:
- `criticality` (enum: critical, high, medium, low): Importance of the storage
- `storage_type` (enum: primary, backup, archive): Storage purpose

---

#### 11. communicates_via (Application Layer → Network Layer)

**Definition**: An application communicates via a network path or load balancer.

**OWL Property Definition**:
```turtle
:communicates_via
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Application :Service :API ) ] ;
  rdfs:range [ owl:unionOf ( :CommunicationPath :LoadBalancer :NetworkSegment ) ] ;  # From Layer 5
  rdfs:label "communicates via" ;
  rdfs:comment "An application communicates via network infrastructure" .
```

**Cardinality**: Many to many (*..*)

**Relationship Properties**:
- `protocol` (string): Communication protocol (HTTP, HTTPS, TCP, etc.)
- `port` (integer): Network port
- `bandwidth_requirement` (string): Required bandwidth

---

#### 12. fulfills (Business Process Layer → Application Layer)

**Definition**: An application fulfills business processes or capabilities.

**OWL Property Definition**:
```turtle
:fulfills
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Application ;
  rdfs:range [ owl:unionOf ( :BusinessProcess :BusinessCapability :BusinessService ) ] ;  # From Layer 1
  rdfs:label "fulfills" ;
  rdfs:comment "An application fulfills business processes or capabilities" .
```

**Cardinality**: Many Applications to many Business Processes (*..*)

**Inverse Property**: `supported_by`

---

## Validation Rules

### Entity Validation Rules

1. **Mandatory Attributes**: All entities MUST have `name` and `lifecycle_status` attributes
2. **Enumeration Compliance**: All enumeration attributes MUST use only defined values
3. **Lifecycle Transitions**: Lifecycle status changes MUST follow valid state transitions
4. **Unique Naming**: Entity names SHOULD be unique within their type and scope

### Relationship Validation Rules

1. **Cardinality Enforcement**: Relationships MUST respect defined cardinality constraints
2. **Cross-Layer Validity**: Cross-layer relationships MUST only connect to valid target layers
3. **Deployment Model Consistency**: 
   - Containerized applications (deployment_model=containerized) MUST have `deployed_as` relationships to Container layer
   - Legacy applications (deployment_model=vm_based) SHOULD have `runs_on` relationships directly to Physical Infrastructure
4. **Storage Relationships**: 
   - Database entities MUST have either `hosted_on` relationship to storage OR be cloud_managed
   - FileStorageService MUST have `mounted_from` relationship to physical storage
5. **Service Communication**: Services with `calls` relationships MUST have compatible protocols

### Data Integrity Rules

1. **Database-Instance Relationship**: DatabaseInstance entities MUST be associated with a parent Database
2. **DataObject Containment**: DataObject entities MUST be contained within a Database or DatabaseInstance
3. **API Exposure**: API entities MUST be exposed by at least one Application or Service
4. **Component Deployment**: ApplicationComponent entities MUST be either:
   - Deployed on an ApplicationServer, OR
   - Part of an Application that is deployed_as Container

### SHACL Validation Example for Relationships

```turtle
:ApplicationRelationshipShape
  a sh:NodeShape ;
  sh:targetClass :Application ;
  
  # Application must fulfill at least one business process
  sh:property [
    sh:path :fulfills ;
    sh:minCount 1 ;
    sh:class :BusinessProcessLayer ;
  ] ;
  
  # If deployment_model is containerized, must have deployed_as relationship
  sh:sparql [
    sh:message "Containerized applications must have deployed_as relationship" ;
    sh:select """
      SELECT $this
      WHERE {
        $this :deployment_model "containerized" .
        FILTER NOT EXISTS { $this :deployed_as ?container }
      }
    """ ;
  ] ;
  
  # If deployment_model is vm_based, must have runs_on relationship
  sh:sparql [
    sh:message "VM-based applications must have runs_on relationship" ;
    sh:select """
      SELECT $this
      WHERE {
        $this :deployment_model "vm_based" .
        FILTER NOT EXISTS { $this :runs_on ?infrastructure }
      }
    """ ;
  ] .
```

---

## Framework Mapping Summary

### TOGAF Application Architecture Mapping

| Ontology Entity | TOGAF Concept | TOGAF Metamodel Element |
|-----------------|---------------|-------------------------|
| Application | Application Component | Application Component |
| ApplicationComponent | Application Module | Application Component (granular) |
| Service | Application Service | Application Service |
| API | Application Interface | Application Interface |
| Database | Data Entity | Data Entity |
| DataObject | Logical Data Component | Logical Data Component |

### CIM (Common Information Model) Mapping

| Ontology Entity | CIM Class | CIM Namespace |
|-----------------|-----------|---------------|
| Application | CIM_ApplicationSystem | CIM_Application |
| ApplicationServer | CIM_ApplicationServer | CIM_Application |
| Database | CIM_DatabaseSystem | CIM_Database |
| DatabaseInstance | CIM_DatabaseService | CIM_Database |
| FileStorageService | CIM_FileSystem | CIM_FileSystem |
| CacheService | CIM_CacheMemory | CIM_Memory |

### ITIL Application Management Mapping

| Ontology Entity | ITIL Concept |
|-----------------|--------------|
| Application | Application |
| ApplicationServer | Application Infrastructure |
| Database | Data Management Service |
| lifecycle_status | Service Lifecycle Stage |
| criticality | Service Priority |

---

## Usage Examples

### Example 1: Microservice Application

```turtle
:OrderService
  rdf:type :Application ;
  :name "Order Service" ;
  :application_type "microservice" ;
  :deployment_model "containerized" ;
  :runtime_environment "Node.js 18" ;
  :technology_stack "Express.js, TypeScript" ;
  :lifecycle_status "production" ;
  :criticality "high" ;
  :fulfills :OrderProcessing ;  # Business Process from Layer 1
  :uses :OrderDatabase ;
  :uses :OrderCache ;
  :exposes :OrderAPI ;
  :publishes_to :OrderQueue ;
  :deployed_as :OrderServiceContainer .  # Container from Layer 3

:OrderDatabase
  rdf:type :Database ;
  :name "OrderDB" ;
  :database_type "relational" ;
  :database_product "PostgreSQL" ;
  :version "14.5" ;
  :data_classification "confidential" ;
  :lifecycle_status "active" ;
  :hosted_on :PostgresVolume .  # Storage from Layer 4

:OrderAPI
  rdf:type :API ;
  :name "Order API" ;
  :api_type "REST" ;
  :version "v2" ;
  :specification_format "OpenAPI" ;
  :authentication_method "OAuth2" ;
  :lifecycle_status "active" ;
  :exposed_by :OrderService .
```

### Example 2: Legacy Java EE Application

```turtle
:CRMApplication
  rdf:type :Application ;
  :name "CRM Application" ;
  :application_type "monolithic" ;
  :deployment_model "vm_based" ;
  :runtime_environment "Java EE 8" ;
  :technology_stack "Java EE, JSF, EJB" ;
  :lifecycle_status "production" ;
  :criticality "critical" ;
  :fulfills :CustomerManagement ;  # Business Process from Layer 1
  :contains :CustomerServlet ;
  :uses :CRMDatabase ;
  :runs_on :CRMAppVM .  # VM from Layer 4 (skips Layer 3)

:CustomerServlet
  rdf:type :ApplicationComponent ;
  :name "CustomerServlet" ;
  :component_type "servlet" ;
  :technology "Java Servlet 4.0" ;
  :lifecycle_status "active" ;
  :deployed_on :WebSphereServer .

:WebSphereServer
  rdf:type :ApplicationServer ;
  :name "WebSphere 9.0 Instance" ;
  :server_type "websphere" ;
  :version "9.0.5" ;
  :port 9080 ;
  :lifecycle_status "running" ;
  :runs_on :CRMAppVM .  # VM from Layer 4
```

### Example 3: SOA Integration Pattern

```turtle
:PaymentGateway
  rdf:type :Service ;
  :name "Payment Gateway Service" ;
  :service_type "integration_service" ;
  :architecture_style "SOA" ;
  :endpoint_url "https://api.example.com/payment" ;
  :protocol "HTTPS" ;
  :lifecycle_status "active" ;
  :exposes :PaymentAPI ;
  :calls :BankingService ;
  :calls :FraudDetectionService ;
  :uses :PaymentQueue .

:PaymentQueue
  rdf:type :MessageQueue ;
  :name "payment-transactions" ;
  :queue_type "queue" ;
  :messaging_product "RabbitMQ" ;
  :protocol "AMQP" ;
  :persistence_enabled true ;
  :lifecycle_status "active" .
```

---

## Extension Guidelines

### Adding New Application Entity Types

1. Define the entity as a subclass of `:ApplicationLayer`
2. Specify mandatory attributes: `name`, `lifecycle_status`
3. Add type-specific attributes with framework sources
4. Define relationships to existing entities
5. Create SHACL validation shape
6. Document framework mappings

### Adding Custom Attributes

Custom attributes should use a separate namespace:

```turtle
@prefix custom: <http://example.org/ontology/custom#> .

:MyApplication
  rdf:type :Application ;
  :name "My Application" ;
  custom:cost_center "CC-12345" ;
  custom:compliance_level "SOC2" .
```

---

## Summary

This specification defines 12 entity types for Layer 2 (Application Layer):

**Application Entities**: Application, ApplicationComponent, ApplicationServer, Service, API

**Storage Entities**: Database, DatabaseInstance, DataObject, FileStorageService, ObjectStorageService, CacheService, MessageQueue

**Relationships**: 12 relationship types (7 intra-layer, 5 cross-layer)

**Framework Sources**: TOGAF, CIM, ITIL, ArchiMate, Cloud Provider APIs

**Validation**: SHACL shapes for all entity types and key relationship patterns

This layer provides the foundation for modeling software applications and their dependencies across modern and legacy architectures.
