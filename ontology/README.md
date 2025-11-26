# IT Infrastructure and Application Dependency Ontology

## Overview

This directory contains the formal OWL 2 ontology specification for the IT Infrastructure and Application Dependency Ontology. The ontology provides a comprehensive model for representing IT infrastructure and application dependencies across six distinct layers.

## Files

### Core Ontology Files

1. **it-infrastructure-ontology.ttl** - Main ontology file containing:
   - Ontology metadata and versioning information
   - Base class hierarchy (InfrastructureEntity)
   - Six layer classes (BusinessProcessLayer, ApplicationLayer, ContainerLayer, PhysicalInfrastructureLayer, NetworkLayer, SecurityLayer)
   - All entity type class definitions (50+ classes)
   - Object properties (relationships) with domains, ranges, and inverse properties
   - Data properties (attributes) with datatypes and cardinality constraints
   - Property chains for cross-layer traversal

2. **shacl-shapes.ttl** - SHACL validation shapes containing:
   - Node shapes for all major entity types
   - Property shapes with cardinality constraints
   - Enumeration validation for controlled vocabularies
   - Cross-layer relationship validation rules
   - Custom validation rules (e.g., certificate expiration checks)

## Ontology Structure

### Layer Architecture

The ontology is organized into six disjoint layers, ensuring each entity belongs to exactly one layer:

1. **Layer 1: Business Process Layer**
   - BusinessProcess, BusinessCapability, BusinessService, Product

2. **Layer 2: Application Layer**
   - Application, ApplicationComponent, Service, API
   - Database, DatabaseInstance, DataObject
   - FileStorageService, ObjectStorageService, CacheService, MessageQueue

3. **Layer 3: Container and Orchestration Layer**
   - Container, Pod, ContainerImage, Cluster, Namespace
   - Deployment, KubernetesService, Route, IngressController

4. **Layer 4: Physical Infrastructure Layer**
   - PhysicalServer, VirtualMachine, Hypervisor, CloudInstance, CloudService
   - ApplicationServer (runtime infrastructure for hosting applications)
   - StorageArray, StorageVolume, FileSystem, StoragePool
   - CloudStorageService, ObjectStorageBucket

5. **Layer 5: Network Topology and Communication Path Layer**
   - NetworkDevice, LoadBalancer, NetworkInterface, NetworkSegment
   - CommunicationPath, NetworkRoute

6. **Layer 6: Security Infrastructure Layer**
   - Firewall, WAF, Certificate, CertificateAuthority
   - SecurityPolicy, IdentityProvider, SecurityZone

### Key Relationships

#### Intra-Layer Relationships
- `part_of` / `contains` - Hierarchical composition
- `enables` / `enabled_by` - Capability enablement
- `supports` / `supported_by` - Service support
- `connected_to` - Network connectivity (symmetric)
- `issued_by` / `issues` - Certificate issuance

#### Cross-Layer Relationships
- `realized_by` / `realizes` - Business to Application
- `packaged_in` / `packages` - Application to Container
- `deployed_as` / `deploys` - Application to Container
- `runs_on` / `hosts` - Container/Application to Infrastructure
- `hosted_on` / `hosts` - Application to Infrastructure
- `communicates_via` - Application to Network
- `protected_by` / `protects` - Any entity to Security
- `secured_by` / `secures` - Any entity to Security Policy

## Framework Sources

The ontology integrates concepts and attributes from multiple industry-standard frameworks:

- **TOGAF** - Business Architecture, Application Architecture, Technology Architecture
- **CIM (Common Information Model)** - Infrastructure components, storage, network
- **ITIL** - Service management, application management
- **ArchiMate** - Enterprise architecture modeling
- **Kubernetes API** - Container orchestration
- **OpenShift API** - Container platform extensions
- **Cloud Provider APIs** - AWS, Azure, GCP specifications
- **NIST Cybersecurity Framework** - Security controls and policies
- **X.509 / PKI Standards** - Certificate management

## Usage

### Loading the Ontology

```turtle
@prefix : <http://example.org/it-infrastructure-ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

# Import the ontology
<http://example.org/it-infrastructure-ontology> a owl:Ontology .
```

### Creating Instance Data

```turtle
# Example: Business Process
:OrderFulfillment a :BusinessProcess ;
  :name "Order Fulfillment" ;
  :owner "Operations Manager" ;
  :criticality "critical" ;
  :lifecycle_status "active" ;
  :process_type "core" ;
  :frequency "real-time" .

# Example: Application
:OrderManagementSystem a :Application ;
  :name "Order Management System" ;
  :application_type "monolithic" ;
  :deployment_model "vm_based" ;
  :lifecycle_status "production" ;
  :realized_by :OrderFulfillment .

# Example: Virtual Machine
:VM_OrderApp01 a :VirtualMachine ;
  :name "VM-OrderApp-01" ;
  :resource_type "virtual" ;
  :vcpu_count 4 ;
  :memory_gb 16.0 ;
  :lifecycle_status "running" ;
  :hosts :OrderManagementSystem .
```

### Validating Instance Data

Use a SHACL validator to validate instance data against the shapes:

```bash
# Using Apache Jena SHACL
shacl validate --shapes shacl-shapes.ttl --data instance-data.ttl

# Using pySHACL (Python)
pyshacl -s shacl-shapes.ttl -d instance-data.ttl
```

### Querying the Ontology

Example SPARQL queries:

```sparql
# Find all applications and their infrastructure
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?vm ?server
WHERE {
  ?app a :Application .
  ?app :hosted_on ?vm .
  ?vm :runs_on ?server .
}

# Find all security components protecting an application
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?app ?security ?secType
WHERE {
  ?app a :Application ;
       :name "OrderManagementSystem" ;
       :protected_by ?security .
  ?security :security_type ?secType .
}

# Find full decomposition chain from business to infrastructure
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

## Validation Rules

The SHACL shapes enforce the following validation rules:

1. **Mandatory Attributes**: All entities must have required attributes (name, lifecycle_status, etc.)
2. **Enumeration Constraints**: Enumerated attributes must use defined values
3. **Cardinality Constraints**: Properties must respect min/max cardinality
4. **Layer Disjointness**: Entities belong to exactly one layer
5. **Relationship Constraints**: Cross-layer relationships must connect appropriate entity types
6. **Business Logic**: Custom rules (e.g., active certificates must not be expired)

## Extension Points

### Adding New Entity Types

1. Define the new class as a subclass of the appropriate layer class
2. Add data properties for attributes
3. Define relationships to existing entity types
4. Create SHACL shapes for validation
5. Document framework sources

### Adding Custom Attributes

Custom attributes should use a separate namespace:

```turtle
@prefix custom: <http://example.org/custom#> .

:MyApplication a :Application ;
  :name "My Application" ;
  custom:deployment_region "us-east-1" ;
  custom:cost_center "CC-12345" .
```

## Tools and Compatibility

The ontology is compatible with:

- **Protégé** - OWL ontology editor
- **Apache Jena** - RDF and OWL processing framework
- **RDFLib** - Python library for RDF
- **TopBraid Composer** - Ontology development environment
- **Neo4j** - Graph database (with RDF plugin)
- **Amazon Neptune** - Managed graph database
- **Stardog** - Enterprise knowledge graph platform
- **GraphDB** - RDF graph database

## Version Information

- **Version**: 1.0.0
- **Created**: 2024-01-01
- **Last Modified**: 2024-01-01
- **Status**: Complete formal specification

## Requirements Traceability

This ontology addresses all requirements defined in the requirements document:

- **Requirement 1**: Six-layer architecture with non-overlapping responsibilities
- **Requirement 2**: Dependency relationships with directionality and cardinality
- **Requirement 3**: Impact analysis support through transitive relationships
- **Requirements 4-5**: TOGAF and CIM framework alignment
- **Requirement 6**: On-premises and cloud infrastructure support
- **Requirement 7**: SOA and microservices patterns
- **Requirement 8**: Minimal, non-overlapping attributes with framework sources
- **Requirement 9**: Root cause analysis support
- **Requirements 10-13**: Specific domain support (integration, security, network, containers)
- **Requirement 14**: Formal OWL specification with validation
- **Requirements 15-16**: Cross-layer decomposition and CMDB mapping

## Next Steps

1. Create sample instance data for validation testing
2. Develop query patterns for common use cases
3. Implement CMDB integration mappings
4. Create visualization tools for ontology exploration
5. Develop documentation and usage guides

## Contact

For questions or contributions, please refer to the main specification documentation.
