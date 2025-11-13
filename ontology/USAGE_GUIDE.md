# IT Infrastructure Ontology - Usage Guide

## Document Information

- **Version**: 1.0.0
- **Date**: 2024-01-15
- **Purpose**: Practical guide for using the IT Infrastructure and Application Dependency Ontology
- **Audience**: IT Architects, Data Modelers, CMDB Administrators, Application Developers

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating Entity Instances](#creating-entity-instances)
3. [Defining Relationships](#defining-relationships)
4. [Validating Data](#validating-data)
5. [Querying the Ontology](#querying-the-ontology)
6. [CMDB Integration](#cmdb-integration)
7. [Common Use Cases](#common-use-cases)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

Before using the ontology, ensure you have:

1. **RDF/OWL Tools**:
   - Apache Jena (Java)
   - RDFLib (Python)
   - Protégé (GUI editor)

2. **Validation Tools**:
   - pySHACL (Python)
   - Apache Jena SHACL
   - TopBraid SHACL Validator

3. **Graph Database** (optional):
   - Neo4j with RDF plugin
   - Amazon Neptune
   - Stardog
   - GraphDB

### Installation

#### Python Setup

```bash
# Install required packages
pip install rdflib pyshacl

# Verify installation
python -c "import rdflib; import pyshacl; print('Setup complete')"
```

#### Java Setup

```bash
# Download Apache Jena
wget https://dlcdn.apache.org/jena/binaries/apache-jena-4.x.x.tar.gz
tar -xzf apache-jena-4.x.x.tar.gz

# Add to PATH
export PATH=$PATH:/path/to/apache-jena/bin
```

### Loading the Ontology

#### Python (RDFLib)

```python
from rdflib import Graph

# Load the ontology
g = Graph()
g.parse("it-infrastructure-ontology.ttl", format="turtle")

print(f"Loaded {len(g)} triples")
```

#### Java (Apache Jena)

```java
import org.apache.jena.rdf.model.*;

// Load the ontology
Model model = ModelFactory.createDefaultModel();
model.read("it-infrastructure-ontology.ttl", "TURTLE");

System.out.println("Loaded " + model.size() + " triples");
```

---

## Creating Entity Instances

### Step-by-Step Guide

#### Step 1: Choose the Appropriate Entity Type

Identify which layer and entity type best represents your component:

- **Layer 1**: Business processes, capabilities, services
- **Layer 2**: Applications, databases, APIs, services
- **Layer 3**: Containers, pods, clusters
- **Layer 4**: Servers, VMs, storage, cloud instances
- **Layer 5**: Network devices, load balancers, paths
- **Layer 6**: Firewalls, certificates, security policies

#### Step 2: Define the Entity with Required Attributes

Every entity must have:
- `name` (mandatory)
- `lifecycle_status` (mandatory)
- Entity-specific mandatory attributes

#### Step 3: Add Optional Attributes

Include optional attributes that provide additional context.

### Example 1: Creating an Application

```turtle
@prefix : <http://example.org/it-infrastructure-ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:OrderManagementSystem a :Application ;
  # Mandatory attributes
  :name "Order Management System" ;
  :application_type "monolithic" ;
  :deployment_model "vm_based" ;
  :lifecycle_status "production" ;
  
  # Optional attributes
  :version "2.5.1" ;
  :runtime_environment "WebSphere 9.0" ;
  :technology_stack "Java EE" ;
  :data_classification "confidential" ;
  :owner "IT Operations Team" ;
  :description "Core order management application" .
```

### Example 2: Creating a Database

```turtle
:OrderDB a :Database ;
  # Mandatory attributes
  :name "OrderDB" ;
  :database_type "relational" ;
  :lifecycle_status "production" ;
  
  # Optional attributes
  :database_engine "PostgreSQL" ;
  :version "14.5" ;
  :port 5432 ;
  :data_classification "confidential" ;
  :owner "Database Team" ;
  :description "Primary order database" .
```

### Example 3: Creating a Virtual Machine

```turtle
:AppServer01 a :VirtualMachine ;
  # Mandatory attributes
  :name "app-server-01" ;
  :resource_type "virtual" ;
  :location "Datacenter-East" ;
  :lifecycle_status "running" ;
  
  # Optional attributes
  :vm_id "vm-12345" ;
  :vcpu_count 8 ;
  :memory_gb 32.0 ;
  :disk_gb 500.0 ;
  :operating_system "Red Hat Enterprise Linux 8.5" ;
  :owner "Infrastructure Team" .
```

### Example 4: Creating a Kubernetes Pod

```turtle
:OrderServicePod a :Pod ;
  # Mandatory attributes
  :name "order-service-pod-abc123" ;
  :lifecycle_status "running" ;
  
  # Optional attributes
  :pod_id "abc123-def456" ;
  :replica_count 3 ;
  :restart_policy "always" ;
  :resource_limits_cpu "2000m" ;
  :resource_limits_memory "4Gi" .
```

### Example 5: Creating a Certificate

```turtle
:WebServerCert a :Certificate ;
  # Mandatory attributes
  :name "*.example.com" ;
  :security_type "certificate" ;
  :certificate_type "ssl_tls" ;
  :lifecycle_status "active" ;
  
  # Optional attributes
  :certificate_id "cert-789" ;
  :subject "CN=*.example.com, O=Example Corp" ;
  :issuer "CN=Example CA, O=Example Corp" ;
  :valid_from "2024-01-01"^^xsd:date ;
  :valid_to "2025-01-01"^^xsd:date ;
  :key_size 2048 ;
  :serial_number "1234567890ABCDEF" .
```

### Python Helper Function

```python
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD

# Define namespace
ONT = Namespace("http://example.org/it-infrastructure-ontology#")
INST = Namespace("http://example.org/instances#")

def create_application(g, name, app_type, deployment_model, lifecycle_status, **kwargs):
    """Create an Application entity instance."""
    app_uri = INST[name.replace(" ", "_")]
    
    # Add type
    g.add((app_uri, RDF.type, ONT.Application))
    
    # Add mandatory attributes
    g.add((app_uri, ONT.name, Literal(name, datatype=XSD.string)))
    g.add((app_uri, ONT.application_type, Literal(app_type, datatype=XSD.string)))
    g.add((app_uri, ONT.deployment_model, Literal(deployment_model, datatype=XSD.string)))
    g.add((app_uri, ONT.lifecycle_status, Literal(lifecycle_status, datatype=XSD.string)))
    
    # Add optional attributes
    for key, value in kwargs.items():
        g.add((app_uri, ONT[key], Literal(value, datatype=XSD.string)))
    
    return app_uri

# Usage
g = Graph()
app = create_application(
    g,
    name="Order Management System",
    app_type="monolithic",
    deployment_model="vm_based",
    lifecycle_status="production",
    version="2.5.1",
    runtime_environment="WebSphere 9.0"
)
```

---

## Defining Relationships

### Understanding Relationship Types

Relationships connect entities across or within layers:

- **Intra-layer**: Connect entities in the same layer (e.g., `part_of`, `contains`)
- **Cross-layer**: Connect entities across layers (e.g., `runs_on`, `realized_by`)

### Relationship Syntax

```turtle
:SourceEntity :relationshipType :TargetEntity .
```

### Common Relationship Patterns

#### Pattern 1: Business Process to Application

```turtle
# Business process realized by application
:OrderFulfillmentProcess :realized_by :OrderManagementSystem .

# Inverse relationship (optional, automatically inferred)
:OrderManagementSystem :realizes :OrderFulfillmentProcess .
```

#### Pattern 2: Application to Database

```turtle
# Application uses database
:OrderManagementSystem :uses :OrderDB .

# Inverse relationship
:OrderDB :used_by :OrderManagementSystem .
```

#### Pattern 3: Application to Container

```turtle
# Application deployed as container
:OrderService :deployed_as :OrderServicePod .

# Inverse relationship
:OrderServicePod :deploys :OrderService .
```

#### Pattern 4: Container to Infrastructure

```turtle
# Pod runs on virtual machine
:OrderServicePod :runs_on :K8sWorkerNode01 .

# Inverse relationship
:K8sWorkerNode01 :hosts :OrderServicePod .
```

#### Pattern 5: Database to Storage

```turtle
# Database stored on storage volume
:OrderDB :stored_on :SAN_Volume_123 .

# Storage volume allocated from storage array
:SAN_Volume_123 :allocated_from :NetApp_SAN_01 .
```

#### Pattern 6: Application to Network

```turtle
# Application communicates via load balancer
:OrderService :communicates_via :WebLoadBalancer .

# Communication path routes through network device
:HTTPSPath :routes_through :CoreRouter01 .
```

#### Pattern 7: Application to Security

```turtle
# Application protected by firewall
:OrderService :protected_by :WebAppFirewall .

# Application secured by certificate
:OrderServiceAPI :secured_by :APIGatewayCert .

# Certificate issued by CA
:APIGatewayCert :issued_by :InternalCA .
```

### Complete Example: Full Stack

```turtle
# Layer 1: Business Process
:OrderFulfillment a :BusinessProcess ;
  :name "Order Fulfillment" ;
  :lifecycle_status "active" .

# Layer 2: Application and Database
:OrderService a :Application ;
  :name "Order Service" ;
  :application_type "microservice" ;
  :deployment_model "containerized" ;
  :lifecycle_status "production" .

:OrderDB a :Database ;
  :name "OrderDB" ;
  :database_type "relational" ;
  :lifecycle_status "production" .

# Layer 3: Container
:OrderServicePod a :Pod ;
  :name "order-service-pod" ;
  :lifecycle_status "running" .

# Layer 4: Infrastructure
:K8sWorkerNode a :VirtualMachine ;
  :name "k8s-worker-node-01" ;
  :resource_type "virtual" ;
  :location "AWS us-east-1" ;
  :lifecycle_status "running" .

:DBServer a :VirtualMachine ;
  :name "db-server-01" ;
  :resource_type "virtual" ;
  :location "AWS us-east-1" ;
  :lifecycle_status "running" .

# Layer 5: Network
:AppLoadBalancer a :LoadBalancer ;
  :name "app-lb-01" ;
  :lb_type "cloud_managed" ;
  :lifecycle_status "active" .

# Layer 6: Security
:AppFirewall a :Firewall ;
  :name "app-firewall" ;
  :security_type "firewall" ;
  :firewall_type "waf" ;
  :lifecycle_status "active" .

# Relationships
:OrderFulfillment :realized_by :OrderService .
:OrderService :uses :OrderDB .
:OrderService :deployed_as :OrderServicePod .
:OrderServicePod :runs_on :K8sWorkerNode .
:OrderDB :hosted_on :DBServer .
:OrderService :communicates_via :AppLoadBalancer .
:OrderService :protected_by :AppFirewall .
```

### Python Helper Function for Relationships

```python
def add_relationship(g, source, relationship, target):
    """Add a relationship between two entities."""
    source_uri = INST[source.replace(" ", "_")]
    target_uri = INST[target.replace(" ", "_")]
    rel_uri = ONT[relationship]
    
    g.add((source_uri, rel_uri, target_uri))
    
    return (source_uri, rel_uri, target_uri)

# Usage
g = Graph()
add_relationship(g, "Order Service", "uses", "OrderDB")
add_relationship(g, "Order Service", "deployed_as", "order-service-pod")
add_relationship(g, "order-service-pod", "runs_on", "k8s-worker-node-01")
```

---

## Validating Data

### Why Validate?

Validation ensures:
- All mandatory attributes are present
- Enumeration values are valid
- Relationships respect cardinality constraints
- Data types are correct
- Business logic rules are satisfied

### Validation with pySHACL (Python)

```python
from pyshacl import validate
from rdflib import Graph

# Load ontology and data
data_graph = Graph()
data_graph.parse("instance-data.ttl", format="turtle")

shapes_graph = Graph()
shapes_graph.parse("shacl-shapes.ttl", format="turtle")

# Validate
conforms, results_graph, results_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    inference='rdfs',
    abort_on_first=False
)

# Check results
if conforms:
    print("✓ Validation passed!")
else:
    print("✗ Validation failed:")
    print(results_text)
```

### Validation with Apache Jena

```bash
# Command-line validation
shacl validate --shapes shacl-shapes.ttl --data instance-data.ttl

# With inference
shacl validate --shapes shacl-shapes.ttl --data instance-data.ttl --rdfs it-infrastructure-ontology.ttl
```

### Common Validation Errors

#### Error 1: Missing Mandatory Attribute

**Error Message**:
```
Validation Result:
  Severity: sh:Violation
  Focus Node: :OrderService
  Result Path: :lifecycle_status
  Message: Application must have exactly one lifecycle_status
```

**Fix**:
```turtle
:OrderService a :Application ;
  :name "Order Service" ;
  :application_type "microservice" ;
  :deployment_model "containerized" ;
  :lifecycle_status "production" .  # Add missing attribute
```

#### Error 2: Invalid Enumeration Value

**Error Message**:
```
Validation Result:
  Severity: sh:Violation
  Focus Node: :OrderService
  Result Path: :application_type
  Message: application_type must be one of: monolithic, SOA_service, microservice, batch, legacy
  Value: "micro-service"
```

**Fix**:
```turtle
:OrderService a :Application ;
  :name "Order Service" ;
  :application_type "microservice" ;  # Use valid enum value
  :deployment_model "containerized" ;
  :lifecycle_status "production" .
```

#### Error 3: Cardinality Violation

**Error Message**:
```
Validation Result:
  Severity: sh:Violation
  Focus Node: :OrderServicePod
  Result Path: :runs_on
  Message: Pod must run on exactly one VirtualMachine
```

**Fix**:
```turtle
# Remove duplicate runs_on relationships
:OrderServicePod :runs_on :K8sWorkerNode01 .
# :OrderServicePod :runs_on :K8sWorkerNode02 .  # Remove this
```

#### Error 4: Invalid Relationship Target

**Error Message**:
```
Validation Result:
  Severity: sh:Violation
  Focus Node: :OrderService
  Result Path: :runs_on
  Message: Application must run on VirtualMachine, PhysicalServer, or CloudInstance
  Value: :OrderServicePod
```

**Fix**:
```turtle
# Use correct relationship
:OrderService :deployed_as :OrderServicePod .  # Not runs_on
:OrderServicePod :runs_on :K8sWorkerNode01 .
```

### Validation Script Example

```python
#!/usr/bin/env python3
"""Validate IT infrastructure instance data."""

import sys
from pyshacl import validate
from rdflib import Graph

def validate_data(data_file, shapes_file, ontology_file=None):
    """Validate instance data against SHACL shapes."""
    
    # Load data
    print(f"Loading data from {data_file}...")
    data_graph = Graph()
    data_graph.parse(data_file, format="turtle")
    print(f"  Loaded {len(data_graph)} triples")
    
    # Load shapes
    print(f"Loading shapes from {shapes_file}...")
    shapes_graph = Graph()
    shapes_graph.parse(shapes_file, format="turtle")
    print(f"  Loaded {len(shapes_graph)} triples")
    
    # Load ontology for inference (optional)
    ont_graph = None
    if ontology_file:
        print(f"Loading ontology from {ontology_file}...")
        ont_graph = Graph()
        ont_graph.parse(ontology_file, format="turtle")
        print(f"  Loaded {len(ont_graph)} triples")
    
    # Validate
    print("\nValidating...")
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        ont_graph=ont_graph,
        inference='rdfs' if ont_graph else 'none',
        abort_on_first=False
    )
    
    # Report results
    print("\n" + "="*60)
    if conforms:
        print("✓ VALIDATION PASSED")
        print("="*60)
        return 0
    else:
        print("✗ VALIDATION FAILED")
        print("="*60)
        print(results_text)
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: validate.py <data-file> <shapes-file> [ontology-file]")
        sys.exit(1)
    
    data_file = sys.argv[1]
    shapes_file = sys.argv[2]
    ontology_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    sys.exit(validate_data(data_file, shapes_file, ontology_file))
```

**Usage**:
```bash
python validate.py instance-data.ttl shacl-shapes.ttl it-infrastructure-ontology.ttl
```

---

## Querying the Ontology

### SPARQL Queries

#### Query 1: List All Applications

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?name ?type ?status
WHERE {
  ?app a :Application ;
       :name ?name ;
       :application_type ?type ;
       :lifecycle_status ?status .
}
ORDER BY ?name
```

#### Query 2: Find Applications Running on a Specific Server

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?name
WHERE {
  ?app a :Application ;
       :name ?name ;
       :runs_on :Server123 .
}
```

#### Query 3: Root Cause Analysis - Find Failed Dependencies

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?component ?layer ?status
WHERE {
  :OrderManagementSystem (:uses|:runs_on|:hosted_on|:communicates_via)+ ?component .
  ?component a ?layer ;
             :lifecycle_status ?status .
  FILTER(?status IN ("degraded", "failed"))
}
```

#### Query 4: Impact Analysis - Find Affected Components

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?affected ?type ?status
WHERE {
  ?affected (:runs_on|:hosted_on|:uses)+ :Server123 ;
            a ?type ;
            :lifecycle_status ?status .
}
```

#### Query 5: Full Stack Decomposition

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

#### Query 6: Security Audit - Find Unprotected Applications

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

#### Query 7: Certificate Expiration Check

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?cert ?name ?validTo ?daysRemaining
WHERE {
  ?cert a :Certificate ;
        :name ?name ;
        :valid_to ?validTo ;
        :lifecycle_status "active" .
  
  BIND((?validTo - NOW()) AS ?duration)
  BIND(xsd:integer(?duration / "P1D"^^xsd:duration) AS ?daysRemaining)
  
  FILTER(?daysRemaining <= 30 && ?daysRemaining >= 0)
}
ORDER BY ?daysRemaining
```

### Python SPARQL Query Example

```python
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

# Load data
g = Graph()
g.parse("instance-data.ttl", format="turtle")

# Prepare query
query = prepareQuery("""
    PREFIX : <http://example.org/it-infrastructure-ontology#>
    
    SELECT ?app ?name ?type
    WHERE {
        ?app a :Application ;
             :name ?name ;
             :application_type ?type ;
             :lifecycle_status "production" .
    }
    ORDER BY ?name
""")

# Execute query
results = g.query(query)

# Process results
print("Production Applications:")
print("-" * 60)
for row in results:
    print(f"  {row.name} ({row.type})")
```

### Cypher Queries (Neo4j)

#### Query 1: List All Applications

```cypher
MATCH (app:Application)
RETURN app.name AS name,
       app.application_type AS type,
       app.lifecycle_status AS status
ORDER BY app.name
```

#### Query 2: Root Cause Analysis

```cypher
MATCH (app:Application {name: 'Order Management System'})
      -[r:USES|RUNS_ON|HOSTED_ON|COMMUNICATES_VIA*]->(component)
WHERE component.lifecycle_status IN ['degraded', 'failed']
RETURN component.name AS component,
       labels(component) AS layer,
       component.lifecycle_status AS status
```

#### Query 3: Impact Analysis

```cypher
MATCH (affected)-[r:RUNS_ON|HOSTED_ON|USES*]->(server:PhysicalServer {name: 'Server123'})
RETURN affected.name AS affected,
       labels(affected) AS type,
       affected.lifecycle_status AS status
```

#### Query 4: Full Stack Decomposition

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

---

## CMDB Integration

### Mapping CMDB Configuration Items to Ontology Entities

| CMDB CI Type | Ontology Entity Type | Mapping Notes |
|--------------|----------------------|---------------|
| Application | Application | Direct mapping |
| Database | Database | Direct mapping |
| Server | PhysicalServer or VirtualMachine | Based on resource_type |
| Network Device | NetworkDevice | Direct mapping |
| Load Balancer | LoadBalancer | Direct mapping |
| Storage | StorageArray or StorageVolume | Based on abstraction level |
| Business Service | BusinessService | Direct mapping |
| Certificate | Certificate | Direct mapping |

### CMDB Relationship Mapping

| CMDB Relationship | Ontology Relationship | Notes |
|-------------------|----------------------|-------|
| Runs On | runs_on | Application to Server |
| Depends On | uses | Application to Database/Service |
| Hosted On | hosted_on | Database to Server |
| Connected To | connected_to | Network connectivity |
| Protected By | protected_by | Security relationships |
| Part Of | part_of | Hierarchical composition |

### Export from CMDB to Ontology

#### ServiceNow Export Example

```python
import requests
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD

# ServiceNow API configuration
SNOW_INSTANCE = "your-instance.service-now.com"
SNOW_USER = "your-username"
SNOW_PASSWORD = "your-password"

# Ontology namespaces
ONT = Namespace("http://example.org/it-infrastructure-ontology#")
INST = Namespace("http://example.org/instances#")

def export_applications_from_servicenow():
    """Export applications from ServiceNow to RDF."""
    
    # Query ServiceNow
    url = f"https://{SNOW_INSTANCE}/api/now/table/cmdb_ci_appl"
    headers = {"Accept": "application/json"}
    auth = (SNOW_USER, SNOW_PASSWORD)
    
    response = requests.get(url, headers=headers, auth=auth)
    applications = response.json()['result']
    
    # Create RDF graph
    g = Graph()
    g.bind("", ONT)
    g.bind("inst", INST)
    
    # Convert to RDF
    for app in applications:
        app_uri = INST[app['sys_id']]
        
        # Add type
        g.add((app_uri, RDF.type, ONT.Application))
        
        # Add attributes
        g.add((app_uri, ONT.name, Literal(app['name'], datatype=XSD.string)))
        g.add((app_uri, ONT.lifecycle_status, Literal(
            map_snow_status(app['operational_status']), 
            datatype=XSD.string
        )))
        
        # Map application type
        app_type = map_application_type(app.get('category', 'legacy'))
        g.add((app_uri, ONT.application_type, Literal(app_type, datatype=XSD.string)))
        
        # Map deployment model
        deployment = map_deployment_model(app.get('deployment_type', 'vm_based'))
        g.add((app_uri, ONT.deployment_model, Literal(deployment, datatype=XSD.string)))
    
    return g

def map_snow_status(snow_status):
    """Map ServiceNow operational status to ontology lifecycle_status."""
    mapping = {
        '1': 'production',      # Operational
        '2': 'degraded',        # Non-Operational
        '3': 'development',     # Under Development
        '4': 'testing',         # Testing
        '5': 'retired'          # Retired
    }
    return mapping.get(snow_status, 'unknown')

def map_application_type(category):
    """Map ServiceNow category to ontology application_type."""
    mapping = {
        'microservice': 'microservice',
        'soa': 'SOA_service',
        'monolithic': 'monolithic',
        'batch': 'batch',
        'legacy': 'legacy'
    }
    return mapping.get(category.lower(), 'legacy')

def map_deployment_model(deployment_type):
    """Map ServiceNow deployment type to ontology deployment_model."""
    mapping = {
        'container': 'containerized',
        'vm': 'vm_based',
        'physical': 'bare_metal',
        'serverless': 'serverless'
    }
    return mapping.get(deployment_type.lower(), 'vm_based')

# Usage
g = export_applications_from_servicenow()
g.serialize("servicenow-export.ttl", format="turtle")
```

### Import from Ontology to CMDB

```python
def import_to_servicenow(rdf_file):
    """Import RDF data to ServiceNow CMDB."""
    
    # Load RDF data
    g = Graph()
    g.parse(rdf_file, format="turtle")
    
    # Query for applications
    query = """
        PREFIX : <http://example.org/it-infrastructure-ontology#>
        
        SELECT ?app ?name ?type ?status
        WHERE {
            ?app a :Application ;
                 :name ?name ;
                 :application_type ?type ;
                 :lifecycle_status ?status .
        }
    """
    
    results = g.query(query)
    
    # Import to ServiceNow
    url = f"https://{SNOW_INSTANCE}/api/now/table/cmdb_ci_appl"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    auth = (SNOW_USER, SNOW_PASSWORD)
    
    for row in results:
        # Map ontology data to ServiceNow format
        data = {
            "name": str(row.name),
            "operational_status": reverse_map_status(str(row.status)),
            "category": reverse_map_app_type(str(row.type))
        }
        
        # Create or update in ServiceNow
        response = requests.post(url, json=data, headers=headers, auth=auth)
        
        if response.status_code == 201:
            print(f"✓ Created: {row.name}")
        else:
            print(f"✗ Failed: {row.name} - {response.text}")

def reverse_map_status(ontology_status):
    """Map ontology lifecycle_status to ServiceNow operational status."""
    mapping = {
        'production': '1',
        'degraded': '2',
        'development': '3',
        'testing': '4',
        'retired': '5'
    }
    return mapping.get(ontology_status, '1')

def reverse_map_app_type(ontology_type):
    """Map ontology application_type to ServiceNow category."""
    mapping = {
        'microservice': 'microservice',
        'SOA_service': 'soa',
        'monolithic': 'monolithic',
        'batch': 'batch',
        'legacy': 'legacy'
    }
    return mapping.get(ontology_type, 'legacy')
```

### Bidirectional Synchronization

```python
class CMDBOntologySync:
    """Bidirectional synchronization between CMDB and Ontology."""
    
    def __init__(self, cmdb_connector, ontology_graph):
        self.cmdb = cmdb_connector
        self.graph = ontology_graph
    
    def sync_from_cmdb(self):
        """Sync data from CMDB to ontology."""
        # Export from CMDB
        cmdb_data = self.cmdb.export_all()
        
        # Convert to RDF
        for item in cmdb_data:
            self.add_to_ontology(item)
        
        # Validate
        self.validate_ontology()
    
    def sync_to_cmdb(self):
        """Sync data from ontology to CMDB."""
        # Query ontology
        ontology_data = self.query_ontology()
        
        # Import to CMDB
        for item in ontology_data:
            self.update_cmdb(item)
    
    def detect_conflicts(self):
        """Detect conflicts between CMDB and ontology."""
        conflicts = []
        
        # Compare data
        cmdb_data = self.cmdb.export_all()
        ontology_data = self.query_ontology()
        
        for cmdb_item in cmdb_data:
            ont_item = self.find_in_ontology(cmdb_item['id'])
            if ont_item and self.has_differences(cmdb_item, ont_item):
                conflicts.append({
                    'id': cmdb_item['id'],
                    'cmdb': cmdb_item,
                    'ontology': ont_item
                })
        
        return conflicts
```

---

## Common Use Cases

### Use Case 1: Root Cause Analysis for Application Failure

**Scenario**: An application is experiencing issues. Find all infrastructure components it depends on to identify the root cause.

**Steps**:

1. **Identify the failing application**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?status
WHERE {
  ?app a :Application ;
       :name "Order Management System" ;
       :lifecycle_status ?status .
}
```

2. **Find all dependencies**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?component ?layer ?status
WHERE {
  :OrderManagementSystem (:uses|:runs_on|:hosted_on|:communicates_via)+ ?component .
  ?component a ?layer ;
             :lifecycle_status ?status .
}
```

3. **Filter for failed components**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?component ?layer ?status
WHERE {
  :OrderManagementSystem (:uses|:runs_on|:hosted_on|:communicates_via)+ ?component .
  ?component a ?layer ;
             :lifecycle_status ?status .
  FILTER(?status IN ("degraded", "failed"))
}
```

4. **Analyze results** to identify the root cause.

---

### Use Case 2: Impact Analysis for Server Maintenance

**Scenario**: A server needs maintenance. Identify all applications and business processes that will be affected.

**Steps**:

1. **Find all components running on the server**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?component ?type
WHERE {
  ?component (:runs_on|:hosted_on) :Server123 ;
             a ?type .
}
```

2. **Find applications using those components**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?name
WHERE {
  ?app a :Application ;
       :name ?name ;
       (:runs_on|:hosted_on|:uses)+ :Server123 .
}
```

3. **Find business processes affected**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?process ?app
WHERE {
  ?process a :BusinessProcess ;
           :realized_by ?app .
  ?app (:runs_on|:hosted_on|:uses)+ :Server123 .
}
```

4. **Generate maintenance impact report**.

---

### Use Case 3: Security Compliance Audit

**Scenario**: Audit all production applications to ensure they have proper security controls.

**Steps**:

1. **Find production applications without firewalls**:
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

2. **Find applications without SSL certificates**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?name
WHERE {
  ?app a :Application ;
       :name ?name ;
       :lifecycle_status "production" .
  FILTER NOT EXISTS {
    ?app :secured_by ?cert .
    ?cert a :Certificate .
  }
}
```

3. **Check certificate expiration**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?app ?cert ?validTo
WHERE {
  ?app a :Application ;
       :lifecycle_status "production" ;
       :secured_by ?cert .
  ?cert :valid_to ?validTo .
  FILTER(?validTo <= (NOW() + "P30D"^^xsd:duration))
}
```

4. **Generate compliance report**.

---

### Use Case 4: Cloud Migration Planning

**Scenario**: Plan migration of on-premises applications to cloud.

**Steps**:

1. **Identify on-premises applications**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?name ?vm
WHERE {
  ?app a :Application ;
       :name ?name ;
       :runs_on ?vm .
  ?vm a :VirtualMachine ;
      :resource_type "virtual" ;
      :location ?loc .
  FILTER(CONTAINS(?loc, "Datacenter"))
}
```

2. **Analyze dependencies**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?dependency ?depType
WHERE {
  ?app a :Application ;
       :location ?loc ;
       :uses ?dependency .
  ?dependency a ?depType .
  FILTER(CONTAINS(?loc, "Datacenter"))
}
```

3. **Estimate resource requirements**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app (SUM(?vcpu) AS ?totalCPU) (SUM(?mem) AS ?totalMemory)
WHERE {
  ?app a :Application ;
       :runs_on ?vm .
  ?vm :vcpu_count ?vcpu ;
      :memory_gb ?mem .
}
GROUP BY ?app
```

4. **Create migration plan** based on dependencies and resources.

---

### Use Case 5: Capacity Planning

**Scenario**: Analyze resource utilization and plan for capacity expansion.

**Steps**:

1. **Calculate total resource usage by application**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?name (SUM(?vcpu) AS ?totalCPU) (SUM(?mem) AS ?totalMemory)
WHERE {
  ?app a :Application ;
       :name ?name ;
       :runs_on ?vm .
  ?vm :vcpu_count ?vcpu ;
      :memory_gb ?mem .
}
GROUP BY ?app ?name
ORDER BY DESC(?totalCPU)
```

2. **Identify underutilized servers**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?server ?name (COUNT(?vm) AS ?vmCount)
WHERE {
  ?server a :PhysicalServer ;
          :name ?name ;
          :hosts ?vm .
  ?vm a :VirtualMachine .
}
GROUP BY ?server ?name
HAVING (COUNT(?vm) < 5)
```

3. **Analyze storage capacity**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?array ?name ?capacity (SUM(?used) AS ?totalUsed)
WHERE {
  ?array a :StorageArray ;
         :name ?name ;
         :capacity_tb ?capacity ;
         :allocates ?volume .
  ?volume :capacity_gb ?used .
}
GROUP BY ?array ?name ?capacity
```

4. **Generate capacity planning report**.

---

## Best Practices

### Data Modeling

1. **Use consistent naming conventions**: Use descriptive names that reflect the entity's purpose
2. **Always include mandatory attributes**: Ensure name and lifecycle_status are present
3. **Use framework-sourced attributes**: Prefer standard attributes over custom ones
4. **Document custom attributes**: Clearly document any custom attributes with rationale
5. **Maintain layer separation**: Ensure entities belong to exactly one layer

### Relationship Management

1. **Use appropriate relationship types**: Choose the correct relationship for the semantic meaning
2. **Respect cardinality constraints**: Follow the defined cardinality rules
3. **Create bidirectional relationships**: Define inverse relationships for navigation
4. **Avoid circular dependencies**: Check for and resolve circular dependency chains
5. **Document complex relationships**: Add comments for non-obvious relationships

### Validation

1. **Validate early and often**: Run validation after each significant change
2. **Fix validation errors immediately**: Don't accumulate validation errors
3. **Use inference for validation**: Enable RDFS inference for better validation
4. **Test with sample data**: Validate against realistic sample data
5. **Automate validation**: Integrate validation into CI/CD pipelines

### Query Optimization

1. **Use property paths wisely**: Property paths can be expensive, limit depth when possible
2. **Filter early**: Apply filters as early as possible in queries
3. **Use indexes**: Create indexes on frequently queried properties
4. **Limit result sets**: Use LIMIT and OFFSET for large result sets
5. **Cache common queries**: Cache results of frequently executed queries

---

## Troubleshooting

### Common Issues

#### Issue 1: Validation Fails with "Unknown Property"

**Symptom**: SHACL validation reports unknown property

**Cause**: Property not defined in ontology or typo in property name

**Solution**: Check property name spelling and ensure it's defined in the ontology

#### Issue 2: Query Returns No Results

**Symptom**: SPARQL query returns empty result set

**Causes**:
- Incorrect namespace prefixes
- Wrong entity URIs
- Missing data

**Solutions**:
- Verify namespace prefixes match ontology
- Check entity URIs are correct
- Confirm data is loaded

#### Issue 3: Performance Issues with Large Datasets

**Symptom**: Queries take too long to execute

**Solutions**:
- Add indexes on frequently queried properties
- Use more specific queries with filters
- Consider using a graph database instead of in-memory RDF
- Partition data by layer or domain

#### Issue 4: CMDB Integration Conflicts

**Symptom**: Data conflicts between CMDB and ontology

**Solutions**:
- Establish CMDB as source of truth or ontology as source of truth
- Implement conflict resolution rules
- Use timestamps to determine latest data
- Manual review for critical conflicts

---

## Additional Resources

### Documentation

- **Ontology Reference**: `ONTOLOGY_REFERENCE.md` - Complete entity and relationship reference
- **Visual Diagrams**: `VISUAL_DIAGRAMS.md` - Architecture and deployment diagrams
- **Layer Specifications**: `layer-specifications/` - Detailed layer documentation
- **Framework Analysis**: `framework-analysis/` - Framework mapping documentation

### Tools and Libraries

- **RDFLib**: https://rdflib.readthedocs.io/
- **Apache Jena**: https://jena.apache.org/
- **pySHACL**: https://github.com/RDFLib/pySHACL
- **Protégé**: https://protege.stanford.edu/
- **Neo4j**: https://neo4j.com/

### Community and Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Refer to specification documents
- **Examples**: Check sample data files for examples

---

**Document Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Status**: Complete

