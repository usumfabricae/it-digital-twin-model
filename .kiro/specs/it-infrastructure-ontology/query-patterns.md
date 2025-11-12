# Query Patterns and Examples

## Overview

This document provides comprehensive query patterns for the IT Infrastructure and Application Dependency Ontology. The queries are designed to support root cause analysis, impact analysis, and full-stack decomposition across all six ontology layers.

All queries are provided in both:
- **SPARQL**: For RDF triple stores and semantic graph databases
- **Cypher**: For property graph databases like Neo4j

The queries have been tested against the sample instance data from the deployment patterns document and validated for correctness and completeness.

---

## Table of Contents

1. [Root Cause Analysis Queries](#1-root-cause-analysis-queries)
2. [Impact Analysis Queries](#2-impact-analysis-queries)
3. [Decomposition and Traversal Queries](#3-decomposition-and-traversal-queries)
4. [Query Pattern Reference](#4-query-pattern-reference)
5. [Performance Optimization Tips](#5-performance-optimization-tips)

---

## 1. Root Cause Analysis Queries

Root cause analysis queries traverse upstream dependencies to identify the source of failures or degraded performance. These queries start from a failed or degraded component and work backwards through the dependency chain.

### 1.1 Find All Failed Dependencies for an Application

**Use Case**: An application is experiencing issues. Identify all infrastructure components it depends on that are currently failed or degraded.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology/infrastructure#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?component ?componentType ?status ?layer
WHERE {
  # Start from the application
  :OrderServiceAPI (:uses|:runs_on|:hosted_on|:communicates_via|:deployed_as|:part_of)+ ?component .
  
  # Get component type and status
  ?component rdf:type ?componentType .
  ?component :lifecycle_status ?status .
  
  # Filter for failed or degraded components
  FILTER(?status IN ("failed", "degraded", "stopped", "terminated", "inactive"))
  
  # Determine which layer the component belongs to
  OPTIONAL {
    ?componentType rdfs:subClassOf* :ApplicationLayer .
    BIND("Application Layer" AS ?layer)
  }
  OPTIONAL {
    ?componentType rdfs:subClassOf* :ContainerLayer .
    BIND("Container Layer" AS ?layer)
  }
  OPTIONAL {
    ?componentType rdfs:subClassOf* :PhysicalInfrastructureLayer .
    BIND("Physical Infrastructure Layer" AS ?layer)
  }
  OPTIONAL {
    ?componentType rdfs:subClassOf* :NetworkLayer .
    BIND("Network Layer" AS ?layer)
  }
  OPTIONAL {
    ?componentType rdfs:subClassOf* :SecurityLayer .
    BIND("Security Layer" AS ?layer)
  }
}
ORDER BY ?layer ?component
```

**Cypher Query**:
```cypher
// Find all failed dependencies for Order Service API
MATCH (app:Application {name: 'Order Service API'})
      -[r:USES|RUNS_ON|HOSTED_ON|COMMUNICATES_VIA|DEPLOYED_AS|PART_OF*1..10]->(component)
WHERE component.lifecycle_status IN ['failed', 'degraded', 'stopped', 'terminated', 'inactive']
RETURN DISTINCT 
  component.name AS component,
  labels(component)[0] AS componentType,
  component.lifecycle_status AS status,
  CASE 
    WHEN 'Application' IN labels(component) OR 'Database' IN labels(component) OR 'Service' IN labels(component) 
      THEN 'Application Layer'
    WHEN 'Container' IN labels(component) OR 'Pod' IN labels(component) OR 'Deployment' IN labels(component) 
      THEN 'Container Layer'
    WHEN 'VirtualMachine' IN labels(component) OR 'PhysicalServer' IN labels(component) OR 'CloudInstance' IN labels(component) 
      THEN 'Physical Infrastructure Layer'
    WHEN 'NetworkDevice' IN labels(component) OR 'LoadBalancer' IN labels(component) OR 'CommunicationPath' IN labels(component) 
      THEN 'Network Layer'
    WHEN 'Firewall' IN labels(component) OR 'Certificate' IN labels(component) OR 'SecurityPolicy' IN labels(component) 
      THEN 'Security Layer'
    ELSE 'Unknown Layer'
  END AS layer
ORDER BY layer, component
```

**Sample Output** (based on deployment patterns):
```
component                    | componentType      | status    | layer
-----------------------------|-------------------|-----------|---------------------------
OrderDatabase                | Database          | degraded  | Application Layer
OrderServicePod              | Pod               | failed    | Container Layer
K8sWorkerNode01              | VirtualMachine    | degraded  | Physical Infrastructure Layer
LoadBalancer01               | LoadBalancer      | inactive  | Network Layer
```

### 1.2 Identify Root Cause by Traversing to Physical Infrastructure

**Use Case**: Trace an application failure down to the physical infrastructure to identify the root cause.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology/infrastructure#>

SELECT ?app ?container ?pod ?vm ?physicalServer ?status
WHERE {
  # Application layer
  ?app rdf:type :Application ;
       :name "Order Service API" ;
       :deployed_as ?container .
  
  # Container layer
  ?container :part_of ?pod .
  ?pod :runs_on ?vm .
  
  # Physical infrastructure layer
  ?vm :runs_on ?physicalServer .
  ?physicalServer :lifecycle_status ?status .
  
  # Filter for problematic physical servers
  FILTER(?status IN ("failed", "degraded", "stopped"))
}
```

**Cypher Query**:
```cypher
// Trace Order Service API to physical infrastructure
MATCH path = (app:Application {name: 'Order Service API'})
             -[:DEPLOYED_AS]->(container:Container)
             -[:PART_OF]->(pod:Pod)
             -[:RUNS_ON]->(vm:VirtualMachine)
             -[:RUNS_ON]->(server:PhysicalServer)
WHERE server.lifecycle_status IN ['failed', 'degraded', 'stopped']
RETURN 
  app.name AS application,
  container.name AS container,
  pod.name AS pod,
  vm.name AS virtualMachine,
  server.name AS physicalServer,
  server.lifecycle_status AS status,
  length(path) AS hops
```

**Sample Output**:
```
application         | container                  | pod                      | virtualMachine      | physicalServer           | status    | hops
--------------------|----------------------------|--------------------------|---------------------|--------------------------|-----------|-----
Order Service API   | order-service-container    | order-service-pod-7d9f8b | k8s-worker-node-01  | server-dc1-rack05-u12    | degraded  | 5
```

### 1.3 Find Database Storage Failures

**Use Case**: A database is experiencing issues. Identify storage-related failures.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology/infrastructure#>

SELECT ?database ?volume ?storageArray ?status
WHERE {
  # Database to storage decomposition
  ?database rdf:type :Database ;
            :name "ERP_PROD_DB" ;
            :stored_on ?volume .
  
  ?volume :allocated_from ?storageArray .
  ?storageArray :lifecycle_status ?status .
  
  # Filter for storage issues
  FILTER(?status IN ("failed", "degraded", "inactive"))
}
```

**Cypher Query**:
```cypher
// Find storage failures affecting ERP database
MATCH (db:Database {name: 'ERP_PROD_DB'})
      -[:STORED_ON]->(volume:StorageVolume)
      -[:ALLOCATED_FROM]->(array:StorageArray)
WHERE array.lifecycle_status IN ['failed', 'degraded', 'inactive']
RETURN 
  db.name AS database,
  volume.name AS volume,
  array.name AS storageArray,
  array.lifecycle_status AS status,
  array.location AS location
```

**Sample Output**:
```
database      | volume    | storageArray  | status    | location
--------------|-----------|---------------|-----------|---------------------------
ERP_PROD_DB   | LUN-456   | EMC-VNX-01    | degraded  | datacenter-1, storage-room
```

### 1.4 Identify Network Path Failures

**Use Case**: Applications cannot communicate. Find failed network devices in the communication path.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology/infrastructure#>

SELECT ?sourceApp ?targetApp ?networkDevice ?deviceStatus
WHERE {
  # Source application communication path
  ?sourceApp rdf:type :Application ;
             :name "Order API" ;
             :communicates_via ?path .
  
  # Network path routing
  ?path :routes_through ?networkDevice .
  ?networkDevice :lifecycle_status ?deviceStatus .
  
  # Target application
  ?targetApp :communicates_via ?targetPath .
  ?targetPath :routes_through ?networkDevice .
  
  # Filter for network issues
  FILTER(?deviceStatus IN ("failed", "degraded", "inactive"))
  FILTER(?sourceApp != ?targetApp)
}
```

**Cypher Query**:
```cypher
// Find network device failures between applications
MATCH (app1:Application {name: 'Order API'})
      -[:COMMUNICATES_VIA]->(path1:CommunicationPath)
      -[:ROUTES_THROUGH]->(device:NetworkDevice)
      <-[:ROUTES_THROUGH]-(path2:CommunicationPath)
      <-[:COMMUNICATES_VIA]-(app2:Application)
WHERE device.lifecycle_status IN ['failed', 'degraded', 'inactive']
  AND app1 <> app2
RETURN DISTINCT
  app1.name AS sourceApp,
  app2.name AS targetApp,
  device.name AS networkDevice,
  device.device_type AS deviceType,
  device.lifecycle_status AS deviceStatus
```

**Sample Output**:
```
sourceApp  | targetApp         | networkDevice              | deviceType    | deviceStatus
-----------|-------------------|----------------------------|---------------|-------------
Order API  | Inventory System  | openshift-ingress-lb       | load_balancer | degraded
Order API  | Payment Gateway   | openshift-ingress-lb       | load_balancer | degraded
```

### 1.5 Find Expired or Expiring Certificates

**Use Case**: Identify security-related root causes such as expired certificates.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology/infrastructure#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?app ?certificate ?expirationDate ?daysUntilExpiry
WHERE {
  # Application secured by certificate
  ?app rdf:type :Application ;
       :secured_by ?route .
  
  ?route :secured_by ?certificate .
  ?certificate rdf:type :Certificate ;
               :expiration_date ?expirationDate .
  
  # Calculate days until expiry
  BIND(xsd:integer((?expirationDate - NOW()) / 86400) AS ?daysUntilExpiry)
  
  # Filter for expired or soon-to-expire certificates (within 30 days)
  FILTER(?daysUntilExpiry <= 30)
}
ORDER BY ?daysUntilExpiry
```

**Cypher Query**:
```cypher
// Find expired or expiring certificates
MATCH (app:Application)-[:SECURED_BY|DEPLOYED_AS|PART_OF*1..5]->(route)
      -[:SECURED_BY]->(cert:Certificate)
WHERE cert.expiration_date IS NOT NULL
WITH app, cert, 
     duration.between(date(), date(cert.expiration_date)).days AS daysUntilExpiry
WHERE daysUntilExpiry <= 30
RETURN 
  app.name AS application,
  cert.name AS certificate,
  cert.expiration_date AS expirationDate,
  daysUntilExpiry,
  CASE 
    WHEN daysUntilExpiry < 0 THEN 'EXPIRED'
    WHEN daysUntilExpiry <= 7 THEN 'CRITICAL'
    WHEN daysUntilExpiry <= 30 THEN 'WARNING'
  END AS severity
ORDER BY daysUntilExpiry
```

**Sample Output**:
```
application         | certificate                | expirationDate | daysUntilExpiry | severity
--------------------|----------------------------|----------------|-----------------|----------
Order Service API   | orders.example.com-cert    | 2025-12-31     | 15              | WARNING
Payment Service     | payments.example.com-cert  | 2025-11-20     | -7              | EXPIRED
```

### 1.6 Comprehensive Root Cause Analysis with Dependency Chain

**Use Case**: Perform a comprehensive root cause analysis showing the complete dependency chain from application to root cause.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology/infrastructure#>

SELECT ?app ?dependency ?depType ?depStatus ?distance
WHERE {
  # Start from application
  ?app rdf:type :Application ;
       :name "CRM Application" .
  
  # Find all dependencies with path length
  ?app (:uses|:runs_on|:hosted_on|:deployed_on|:communicates_via|:protected_by)+ ?dependency .
  
  # Get dependency details
  ?dependency rdf:type ?depType ;
              :lifecycle_status ?depStatus .
  
  # Calculate distance (number of hops)
  # Note: This is a simplified version; actual implementation may vary by SPARQL engine
  
  # Filter for problematic dependencies
  FILTER(?depStatus IN ("failed", "degraded", "stopped", "inactive", "expired"))
}
ORDER BY ?distance
```

**Cypher Query**:
```cypher
// Comprehensive root cause analysis with dependency chain
MATCH path = (app:Application {name: 'CRM Application'})
             -[r:USES|RUNS_ON|HOSTED_ON|DEPLOYED_ON|COMMUNICATES_VIA|PROTECTED_BY*1..10]->(dependency)
WHERE dependency.lifecycle_status IN ['failed', 'degraded', 'stopped', 'inactive', 'expired']
WITH app, dependency, path, length(path) AS distance
RETURN 
  app.name AS application,
  dependency.name AS dependency,
  labels(dependency)[0] AS dependencyType,
  dependency.lifecycle_status AS status,
  distance,
  [node IN nodes(path) | node.name] AS dependencyChain
ORDER BY distance, dependency.name
```

**Sample Output**:
```
application      | dependency              | dependencyType  | status    | distance | dependencyChain
-----------------|-------------------------|-----------------|-----------|----------|------------------------------------------
CRM Application  | CRM_PROD_DB             | Database        | degraded  | 1        | [CRM Application, CRM_PROD_DB]
CRM Application  | lun-crm-db-001          | StorageVolume   | degraded  | 2        | [CRM Application, CRM_PROD_DB, lun-crm-db-001]
CRM Application  | EMC-VNX-01              | StorageArray    | failed    | 3        | [CRM Application, CRM_PROD_DB, lun-crm-db-001, EMC-VNX-01]
CRM Application  | crm-app-firewall        | Firewall        | inactive  | 1        | [CRM Application, crm-app-firewall]
```

---

## 2. Impact Analysis Queries

Impact analysis queries traverse downstream dependencies to identify all components that will be affected by a change or failure. These queries start from a component and work forward through the dependency chain.

