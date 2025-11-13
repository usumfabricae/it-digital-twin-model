# IT Infrastructure and Application Dependency Ontology

A formal OWL 2 ontology for modeling IT infrastructure and application dependencies across six architectural layers, enabling root cause analysis, impact assessment, and full-stack decomposition from business processes to physical infrastructure.

## Overview

This ontology provides a comprehensive, standards-based model for representing enterprise IT infrastructure and application dependencies. It integrates concepts from TOGAF, CIM, ITIL, ArchiMate, Kubernetes, and major cloud provider APIs to create a unified semantic model.

### Key Features

- **Six-Layer Architecture**: Clear separation of concerns across business, application, container, infrastructure, network, and security layers
- **50+ Entity Types**: Comprehensive coverage of modern and legacy IT components
- **Framework Alignment**: Attributes sourced from TOGAF, CIM, ITIL, ArchiMate, Kubernetes, AWS, Azure, GCP
- **SHACL Validation**: Formal validation rules for data quality enforcement
- **Deployment Patterns**: Support for containerized, legacy, hybrid, and multi-cloud architectures
- **Query Patterns**: Pre-built SPARQL and Cypher queries for common use cases

### Use Cases

- **Root Cause Analysis**: Trace application failures to underlying infrastructure issues
- **Impact Assessment**: Identify all components affected by planned changes
- **Security Compliance**: Audit security controls and certificate expiration
- **Cloud Migration**: Plan and track migration from on-premises to cloud
- **Capacity Planning**: Analyze resource utilization and plan expansions
- **CMDB Integration**: Bidirectional synchronization with CMDB systems

## Quick Start

### Prerequisites

- Python 3.8+ with `rdflib` and `pyshacl`
- OR Apache Jena for Java-based processing
- Optional: Neo4j, Amazon Neptune, or other graph database

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd it-infrastructure-ontology

# Install Python dependencies
pip install -r ontology/requirements.txt

# Verify installation
python -c "import rdflib; import pyshacl; print('Setup complete')"
```

### Basic Usage

```python
from rdflib import Graph, Namespace
from pyshacl import validate

# Load the ontology
g = Graph()
g.parse("ontology/it-infrastructure-ontology.ttl", format="turtle")

# Create an application instance
ONT = Namespace("http://example.org/it-infrastructure-ontology#")
INST = Namespace("http://example.org/instances#")

g.add((INST.MyApp, RDF.type, ONT.Application))
g.add((INST.MyApp, ONT.name, Literal("My Application")))
g.add((INST.MyApp, ONT.application_type, Literal("microservice")))
g.add((INST.MyApp, ONT.deployment_model, Literal("containerized")))
g.add((INST.MyApp, ONT.lifecycle_status, Literal("production")))

# Validate
shapes = Graph()
shapes.parse("ontology/shacl-shapes.ttl", format="turtle")
conforms, results, text = validate(g, shacl_graph=shapes)

if conforms:
    print("✓ Validation passed!")
else:
    print("✗ Validation failed:")
    print(text)
```

## Project Structure

```
.
├── README.md                          # This file
├── ontology/                          # Core ontology files
│   ├── it-infrastructure-ontology.ttl # Main OWL ontology
│   ├── shacl-shapes.ttl               # SHACL validation shapes
│   ├── sample-data-*.ttl              # Sample instance data
│   ├── ONTOLOGY_REFERENCE.md          # Complete entity/relationship reference
│   ├── VISUAL_DIAGRAMS.md             # Architecture diagrams (Mermaid)
│   ├── USAGE_GUIDE.md                 # Practical usage guide
│   ├── EXTENSION_GUIDE.md             # Extension and customization guide
│   ├── README.md                      # Ontology documentation
│   └── requirements.txt               # Python dependencies
│
├── layer-specifications/              # Detailed layer specifications
│   ├── layer1-business-processes.md
│   ├── layer2-application-specification.md
│   ├── layer3-container-orchestration.md
│   ├── layer4-physical-infrastructure.md
│   ├── layer5-network-topology.md
│   ├── layer6-security-infrastructure.md
│   └── README.md
│
├── framework-analysis/                # Framework mapping analysis
│   ├── togaf-analysis.md
│   ├── cim-analysis.md
│   ├── itil-archimate-analysis.md
│   ├── kubernetes-openshift-analysis.md
│   ├── cloud-provider-analysis.md
│   └── framework-mapping-summary.md
│
├── deployment-patterns.md             # Deployment pattern examples
├── query-patterns.md                  # Query examples and patterns
└── Chart_Representation.png           # Visual architecture diagram
```

## Architecture

### Six-Layer Model

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

### Entity Types by Layer

- **Layer 1**: BusinessProcess, BusinessCapability, BusinessService, Product
- **Layer 2**: Application, Database, API, Service, MessageQueue, CacheService, FileStorageService, ObjectStorageService
- **Layer 3**: Container, Pod, ContainerImage, Cluster, Namespace, Deployment, KubernetesService, Route
- **Layer 4**: PhysicalServer, VirtualMachine, CloudInstance, StorageArray, StorageVolume, FileSystem
- **Layer 5**: NetworkDevice, LoadBalancer, NetworkInterface, NetworkSegment, CommunicationPath
- **Layer 6**: Firewall, WAF, Certificate, CertificateAuthority, SecurityPolicy, IdentityProvider

### Key Relationships

- **Cross-Layer**: `realized_by`, `deployed_as`, `runs_on`, `hosted_on`, `communicates_via`, `protected_by`
- **Intra-Layer**: `part_of`, `contains`, `enables`, `supports`, `connected_to`, `issued_by`

## Documentation

### Core Documentation

- **[Ontology Reference](ontology/ONTOLOGY_REFERENCE.md)**: Complete reference for all entity types, relationships, and attributes
- **[Visual Diagrams](ontology/VISUAL_DIAGRAMS.md)**: Architecture and deployment diagrams using Mermaid
- **[Usage Guide](ontology/USAGE_GUIDE.md)**: Practical guide with examples and best practices
- **[Extension Guide](ontology/EXTENSION_GUIDE.md)**: How to extend and customize the ontology

### Layer Specifications

- **[Layer 1: Business Processes](layer-specifications/layer1-business-processes.md)**
- **[Layer 2: Application Layer](layer-specifications/layer2-application-specification.md)**
- **[Layer 3: Container & Orchestration](layer-specifications/layer3-container-orchestration.md)**
- **[Layer 4: Physical Infrastructure](layer-specifications/layer4-physical-infrastructure.md)**
- **[Layer 5: Network Topology](layer-specifications/layer5-network-topology.md)**
- **[Layer 6: Security Infrastructure](layer-specifications/layer6-security-infrastructure.md)**

### Framework Analysis

- **[TOGAF Analysis](framework-analysis/togaf-analysis.md)**
- **[CIM Analysis](framework-analysis/cim-analysis.md)**
- **[ITIL & ArchiMate Analysis](framework-analysis/itil-archimate-analysis.md)**
- **[Kubernetes & OpenShift Analysis](framework-analysis/kubernetes-openshift-analysis.md)**
- **[Cloud Provider Analysis](framework-analysis/cloud-provider-analysis.md)**

## Examples

### Example 1: Root Cause Analysis

Find all failed dependencies for an application:

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

### Example 2: Impact Analysis

Find all components affected by server maintenance:

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?affected ?type
WHERE {
  ?affected (:runs_on|:hosted_on|:uses)+ :Server123 ;
            a ?type .
}
```

### Example 3: Security Audit

Find production applications without firewall protection:

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

More examples in [query-patterns.md](query-patterns.md) and [deployment-patterns.md](deployment-patterns.md).

## Validation

Validate your instance data against SHACL shapes:

```bash
# Using pySHACL
pyshacl -s ontology/shacl-shapes.ttl -d your-data.ttl -f human

# Using Apache Jena
shacl validate --shapes ontology/shacl-shapes.ttl --data your-data.ttl
```

## Tools and Compatibility

### Ontology Editors
- Protégé - OWL ontology editor
- TopBraid Composer - Commercial ontology IDE
- WebVOWL - Ontology visualization

### RDF/OWL Libraries
- Apache Jena (Java)
- RDFLib (Python)
- RDF4J (Java)

### Graph Databases
- Neo4j with RDF plugin
- Amazon Neptune
- Stardog
- GraphDB

### Validation Tools
- pySHACL (Python)
- Apache Jena SHACL
- TopBraid SHACL Validator

## Contributing

### Adding New Entity Types

1. Identify the appropriate layer
2. Define the OWL class with proper annotations
3. Add data properties (attributes)
4. Define object properties (relationships)
5. Create SHACL validation shapes
6. Document in layer specification
7. Test with sample data

See [EXTENSION_GUIDE.md](ontology/EXTENSION_GUIDE.md) for detailed instructions.

### Framework Integration

To integrate a new framework:

1. Analyze framework metamodel
2. Map concepts to ontology layers
3. Extract attributes and relationships
4. Document mappings
5. Update entity definitions
6. Create framework analysis document

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible changes (removing entities, changing semantics)
- **MINOR**: Backward-compatible additions (new entities, attributes)
- **PATCH**: Backward-compatible fixes (documentation, bug fixes)

**Current Version**: 1.0.0

## Requirements Traceability

This ontology addresses all requirements defined in the [requirements document](.kiro/specs/it-infrastructure-ontology/requirements.md):

- ✓ Six-layer architecture with non-overlapping responsibilities
- ✓ Dependency relationships with directionality and cardinality
- ✓ Impact analysis support through transitive relationships
- ✓ TOGAF and CIM framework alignment
- ✓ On-premises and cloud infrastru