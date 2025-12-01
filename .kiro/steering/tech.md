# Technology Stack

## Core Technologies

### Ontology Languages
- **OWL 2** (Web Ontology Language) - Formal ontology specification
- **RDF** (Resource Description Framework) - Data model
- **RDFS** (RDF Schema) - Basic vocabulary
- **Turtle** (.ttl) - Human-readable RDF serialization format
- **SHACL** (Shapes Constraint Language) - Validation rules

### Python Stack
- **rdflib** (>=7.0.0) - RDF graph manipulation and SPARQL queries
- **pyshacl** (>=0.25.0) - SHACL validation engine
- Python 3.x for validation and testing scripts

### Query Languages
- **SPARQL 1.1** - RDF query language for semantic databases
- **Cypher** - Property graph query language for Neo4j

## File Organization

### Ontology Files (`ontology/`)
- `it-infrastructure-ontology.ttl` - Main OWL ontology (classes, properties, relationships)
- `data-properties.ttl` - Data property definitions
- `shacl-shapes.ttl` - SHACL validation shapes
- `sample-data-*.ttl` - Instance data for different deployment scenarios

### Layer Specifications (`layer-specifications/`)
- Markdown files documenting each of the six layers
- Entity type definitions with attributes and relationships
- Framework source attributions

### Framework Analysis (`framework-analysis/`)
- Analysis documents mapping industry frameworks to ontology concepts
- TOGAF, CIM, ITIL, ArchiMate, Kubernetes, cloud provider mappings

## Common Commands

### Git Operations
```bash
# Git commands require starting a bash shell first
bash

# Then use git normally
git status
git add .
git commit -m "message"
git push
```

### Validation
```bash
# Validate sample data against SHACL shapes
python ontology/validate_sample_data.py

# Validate specific file
pyshacl -s ontology/shacl-shapes.ttl -d ontology/sample-data-cloud.ttl
```

### Testing
```bash
# Run SPARQL query tests
python ontology/test_queries.py
```

### Dependencies
```bash
# Install Python dependencies
pip install -r ontology/requirements.txt
```

## Conventions

### Naming
- Ontology namespace: `http://example.org/it-infrastructure-ontology#`
- Instance namespace: `http://example.org/instances#`
- Use PascalCase for classes (e.g., `BusinessProcess`, `VirtualMachine`)
- Use snake_case for properties (e.g., `lifecycle_status`, `runs_on`)

### File Formats
- All ontology files use Turtle (.ttl) format
- Documentation in Markdown (.md)
- Python scripts for validation and testing

### Documentation Style
- Use EARS (Easy Approach to Requirements Syntax) for requirements
- Include framework sources for all attributes
- Provide both SPARQL and Cypher query examples
- Include sample output for all query patterns


## Critical Design Patterns

### Network Layer Modeling

**Key Principle**: CommunicationPath connects NetworkInterface endpoints, not NetworkDevices

**Correct Pattern**:
```turtle
# Communication path with explicit endpoints
:Path_ServiceA_to_ServiceB
  :connects_from :eth0_vm_serviceA ;      # Source interface
  :routes_through :Router_Core01 ;        # Intermediate device
  :routes_through :Firewall_DMZ ;         # Intermediate device
  :routes_through :LoadBalancer_Web ;     # Intermediate device
  :connects_to :eth0_vm_serviceB .        # Destination interface

# Network interface connected to switch port
:eth0_vm_serviceA
  :attached_to :VM_ServiceA ;             # Attached to compute resource
  :connected_to_port :Switch_Access01 ;   # Connected to switch port
  :part_of_segment :Subnet_AppTier .      # Part of network segment
```

**Why This Matters**:
- Enables precise root cause analysis
- Can identify exact source and destination of communication
- Can trace complete network path including intermediate hops
- Critical for troubleshooting: "Which switch port is failing?"

### Infrastructure Hosting Hierarchy

**ApplicationServer Placement**: Layer 4 (Physical Infrastructure), NOT Layer 2 (Application)

**Rationale**: ApplicationServer is infrastructure that hosts applications, similar to VMs and containers

**Correct Pattern**:
```turtle
:Application_OrderService
  :hosted_on :AppServer_WebSphere01 .

:AppServer_WebSphere01
  rdf:type :ApplicationServer ;
  :runs_on :VM_AppServer01 .

:VM_AppServer01
  :runs_on :Hypervisor_ESXi01 .

:Hypervisor_ESXi01
  :runs_on :PhysicalServer_Rack05 .
```

### Kubernetes Networking

**Pod-Level Network Interfaces**: NetworkInterface attaches to Pod, not individual Containers

**Rationale**: In Kubernetes, the Pod has the network namespace; containers share it

**Correct Pattern**:
```turtle
:Pod_OrderService
  rdf:type :Pod ;
  :contains :Container_OrderApp ;
  :contains :Container_Sidecar .

:eth0_pod_orderservice
  rdf:type :NetworkInterface ;
  :attached_to :Pod_OrderService ;        # Attached to Pod, not Container
  :ip_address "10.1.10.5" ;
  :connected_to_port :Switch_K8s01 .
```

## Query Patterns for Troubleshooting

### Pattern 1: Trace Service-to-Service Communication

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

# Find complete network path between services
SELECT ?sourceIP ?device ?destIP
WHERE {
  :ServiceA :communicates_via ?path .
  ?path :connects_from ?srcInterface .
  ?srcInterface :ip_address ?sourceIP .
  ?path :routes_through ?device .
  ?path :connects_to ?dstInterface .
  ?dstInterface :ip_address ?destIP .
  ?dstInterface :attached_to/:hosts :ServiceB .
}
```

### Pattern 2: Find Failed Network Components

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

# Identify failures in communication path
SELECT ?component ?status
WHERE {
  :ServiceA :communicates_via ?path .
  {
    ?path :routes_through ?component .
    ?component :lifecycle_status ?status .
    FILTER(?status != "active")
  } UNION {
    ?path :connects_from|:connects_to ?component .
    ?component :lifecycle_status ?status .
    FILTER(?status != "up")
  }
}
```

### Pattern 3: Impact Analysis

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

# Find all services affected by device failure
SELECT DISTINCT ?service
WHERE {
  ?path :routes_through :Router_Core01 .
  ?service :communicates_via ?path .
}
```

## Validation Rules

### Network Layer Validation

**Required Relationships**:
- CommunicationPath MUST have exactly one `connects_from` (source interface)
- CommunicationPath MUST have exactly one `connects_to` (destination interface)
- CommunicationPath MAY have zero or more `routes_through` (intermediate devices)
- NetworkInterface MUST have exactly one `attached_to` (compute resource)
- NetworkInterface SHOULD have one `connected_to_port` (network device)

**SHACL Example**:
```turtle
:CommunicationPathEndpointValidation
  a sh:NodeShape ;
  sh:targetClass :CommunicationPath ;
  sh:property [
    sh:path :connects_from ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "Communication path must have exactly one source interface"
  ] ;
  sh:property [
    sh:path :connects_to ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "Communication path must have exactly one destination interface"
  ] .
```

## Common Pitfalls to Avoid

### ❌ Don't: Connect CommunicationPath directly to NetworkDevice
```turtle
# WRONG - Missing endpoint information
:Path_A_to_B :routes_through :Switch01 .
```

### ✅ Do: Connect through NetworkInterface endpoints
```turtle
# CORRECT - Explicit endpoints
:Path_A_to_B
  :connects_from :eth0_vmA ;
  :routes_through :Switch01 ;
  :connects_to :eth0_vmB .
```

### ❌ Don't: Attach NetworkInterface to Container in Kubernetes
```turtle
# WRONG - Containers share Pod network
:eth0 :attached_to :Container_App .
```

### ✅ Do: Attach NetworkInterface to Pod
```turtle
# CORRECT - Pod owns the network namespace
:eth0 :attached_to :Pod_OrderService .
```

### ❌ Don't: Remove NetworkDevice thinking it's redundant
```turtle
# WRONG - Loses critical troubleshooting capability
# Cannot identify which router/switch/firewall failed
```

### ✅ Do: Keep NetworkDevice for complete topology
```turtle
# CORRECT - Full visibility for root cause analysis
:Path :routes_through :Router01, :Firewall01, :Switch01 .
```
