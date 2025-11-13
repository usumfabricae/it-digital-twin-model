# Project Structure

## Directory Layout

```
.
├── ontology/                          # Core ontology files and validation
│   ├── it-infrastructure-ontology.ttl # Main OWL ontology specification
│   ├── data-properties.ttl            # Data property definitions
│   ├── shacl-shapes.ttl               # SHACL validation shapes
│   ├── sample-data-*.ttl              # Instance data examples
│   ├── test_queries.py                # SPARQL query test suite
│   ├── validate_sample_data.py        # SHACL validation script
│   ├── requirements.txt               # Python dependencies
│   └── *.md                           # Documentation and results
│
├── layer-specifications/              # Layer-by-layer specifications
│   ├── layer1-business-processes.md   # Business layer entities
│   ├── layer2-application-specification.md
│   ├── layer3-container-orchestration.md
│   ├── layer4-physical-infrastructure.md
│   ├── layer5-network-topology.md
│   ├── layer6-security-infrastructure.md
│   ├── *-relationships-guide.md       # Relationship semantics
│   ├── *-implementation-summary.md    # Implementation status
│   └── README.md                      # Layer overview
│
├── framework-analysis/                # Framework mapping analysis
│   ├── togaf-analysis.md              # TOGAF framework mapping
│   ├── cim-analysis.md                # CIM framework mapping
│   ├── itil-archimate-analysis.md     # ITIL/ArchiMate mapping
│   ├── kubernetes-openshift-analysis.md
│   ├── cloud-provider-analysis.md     # AWS/Azure/GCP mapping
│   └── framework-mapping-summary.md
│
├── deployment-patterns.md             # Deployment pattern examples
├── query-patterns.md                  # Query examples and patterns
└── Chart_Representation.png           # Visual architecture diagram
```

## Layer Architecture

The ontology is organized into **six disjoint layers**:

1. **Layer 1: Business Processes** - Business capabilities, processes, services, products
2. **Layer 2: Application Layer** - Applications, services, databases, APIs, data objects
3. **Layer 3: Container & Orchestration** - Containers, pods, clusters, Kubernetes resources
4. **Layer 4: Physical Infrastructure** - Servers, VMs, storage, cloud instances
5. **Layer 5: Network Topology** - Network devices, paths, communication infrastructure
6. **Layer 6: Security Infrastructure** - Firewalls, certificates, policies, security controls

## Key Relationships

### Cross-Layer Relationships
- `realized_by` / `realizes` - Business to Application (Layer 1 → 2)
- `deployed_as` / `deploys` - Application to Container (Layer 2 → 3)
- `packaged_in` / `packages` - Application to Container (Layer 2 → 3)
- `runs_on` / `hosts` - Container/Application to Infrastructure (Layer 3/2 → 4)
- `communicates_via` - Application to Network (Layer 2 → 5)
- `protected_by` / `protects` - Any entity to Security (Any → 6)

### Intra-Layer Relationships
- `part_of` / `contains` - Hierarchical composition
- `enables` / `enabled_by` - Capability enablement
- `supports` / `supported_by` - Service support
- `connected_to` - Network connectivity (symmetric)
- `uses` - Dependency relationships

## Documentation Patterns

### Entity Type Specifications
Each layer specification includes:
- Entity type definitions with descriptions
- Attribute tables (name, type, cardinality, framework source)
- SHACL validation shapes
- Usage examples in Turtle format
- Query patterns (SPARQL and Cypher)
- Requirements traceability

### Deployment Patterns
Organized by deployment type:
- Containerized applications (Kubernetes/OpenShift)
- Legacy applications (WebSphere, IIS)
- Storage decomposition (SAN, cloud, NFS, object storage)
- Hybrid and SOA integration patterns

### Query Patterns
Organized by use case:
- Root cause analysis queries
- Impact analysis queries
- Decomposition and traversal queries
- Performance optimization tips

## File Naming Conventions

- Layer specifications: `layer{N}-{description}.md`
- Sample data: `sample-data-{scenario}.ttl`
- Framework analysis: `{framework}-analysis.md`
- Implementation summaries: `{layer}-implementation-summary.md`
- Relationship guides: `{layer}-relationships-guide.md`

## Extension Points

When extending the ontology:
- Add new entity types as subclasses of appropriate layer classes
- Define custom attributes in separate namespaces
- Create SHACL shapes for new entity types
- Document framework sources for all new concepts
- Add deployment pattern examples
- Include query patterns for new use cases
