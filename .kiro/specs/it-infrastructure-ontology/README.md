# IT Infrastructure Ontology - Specification Documentation

## Overview

This directory contains the complete specification for the IT Infrastructure and Application Dependency Ontology, including requirements, design, implementation tasks, and all design decisions.

---

## Document Index

### Core Specification Documents

| Document | Purpose | Status |
|----------|---------|--------|
| **requirements.md** | Formal requirements using EARS syntax | ✅ Complete |
| **design.md** | Complete design with correctness properties | ✅ Complete |
| **tasks.md** | Implementation task list | ✅ Complete |

### Design Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **DESIGN_DECISIONS.md** | Complete design rationale and decisions | Read first to understand WHY |
| **IMPROVEMENTS_LOG.md** | Session-by-session improvements tracking | Review to see what changed |
| **QUICK_REFERENCE.md** | Cheat sheet for common patterns and queries | Use daily for quick lookup |

### Layer Specifications

Located in `../../layer-specifications/`:

| Layer | File | Description |
|-------|------|-------------|
| Layer 1 | `layer1-business-processes.md` | Business processes, capabilities, services, products |
| Layer 2 | `layer2-application-specification.md` | Applications, services, databases, APIs |
| Layer 3 | `layer3-container-orchestration.md` | Containers, pods, Kubernetes resources |
| Layer 4 | `layer4-physical-infrastructure.md` | Servers, VMs, storage, application servers |
| Layer 5 | `layer5-network-topology.md` | Network devices, interfaces, communication paths |
| Layer 6 | `layer6-security-infrastructure.md` | Firewalls, certificates, security policies |

---

## Quick Start

### For New Team Members

1. **Start Here**: Read `DESIGN_DECISIONS.md` to understand key design choices
2. **Learn Patterns**: Review `QUICK_REFERENCE.md` for common patterns
3. **Understand Requirements**: Read `requirements.md` for formal requirements
4. **Study Design**: Review `design.md` for complete architecture

### For Troubleshooting

1. **Quick Lookup**: Use `QUICK_REFERENCE.md` for SPARQL queries
2. **Network Issues**: See Layer 5 section in `DESIGN_DECISIONS.md`
3. **Relationship Questions**: Check visual diagrams in `../../ontology/VISUAL_DIAGRAMS.md`

### For Extending the Ontology

1. **Review Design Principles**: See `DESIGN_DECISIONS.md` section on design principles
2. **Check Existing Patterns**: Review `QUICK_REFERENCE.md` patterns
3. **Follow Conventions**: See `../../.kiro/steering/tech.md` for conventions
4. **Update Documentation**: Add to `IMPROVEMENTS_LOG.md` when making changes

---

## Critical Design Decisions Summary

### 1. Network Layer Modeling ⭐⭐⭐

**Key Principle**: CommunicationPath connects NetworkInterface endpoints, not NetworkDevices

```turtle
:Path_A_to_B
  :connects_from :eth0_source ;      # Source endpoint
  :routes_through :Router01 ;        # Intermediate device
  :connects_to :eth0_dest .          # Destination endpoint
```

**Why**: Enables precise root cause analysis and troubleshooting

### 2. NetworkInterface to NetworkDevice Connection ⭐⭐⭐

**Key Principle**: NetworkInterface connects to NetworkDevice port

```turtle
:eth0_vm01
  :attached_to :VM_App01 ;           # Attached to compute
  :connected_to_port :Switch01 .     # Connected to switch port
```

**Why**: Critical for identifying which switch port failed

### 3. ApplicationServer Placement ⭐

**Key Principle**: ApplicationServer is in Layer 4 (Infrastructure), not Layer 2 (Application)

```turtle
:AppServer_WebSphere
  rdf:type :ApplicationServer ;      # Layer 4 entity
  :runs_on :VirtualMachine .
```

**Why**: ApplicationServer is infrastructure that hosts applications

### 4. Kubernetes Networking ⭐⭐

**Key Principle**: NetworkInterface attaches to Pod, not Container

```turtle
:eth0_pod
  :attached_to :Pod_OrderService .   # Pod owns network namespace
```

**Why**: In Kubernetes, containers share the Pod's network interface

### 5. NetworkDevice is Essential ⭐⭐⭐

**Key Principle**: NetworkDevice cannot be removed

**Why**: 
- Essential for root cause analysis
- Identifies which router/switch/firewall failed
- Enables network topology mapping
- Critical for impact analysis

---

## Most Important Queries

### 1. Trace Network Path
```sparql
SELECT ?sourceIP ?device ?destIP
WHERE {
  :ServiceA :communicates_via ?path .
  ?path :connects_from ?srcIf .
  ?srcIf :ip_address ?sourceIP .
  ?path :routes_through ?device .
  ?path :connects_to ?dstIf .
  ?dstIf :ip_address ?destIP .
}
```

### 2. Find Root Cause
```sparql
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

### 3. Impact Analysis
```sparql
SELECT DISTINCT ?service
WHERE {
  ?path :routes_through :Router_Core01 .
  ?service :communicates_via ?path .
}
```

---

## File Structure

```
.kiro/specs/it-infrastructure-ontology/
├── README.md                    # This file - start here
├── requirements.md              # Formal requirements (EARS)
├── design.md                    # Complete design document
├── tasks.md                     # Implementation tasks
├── DESIGN_DECISIONS.md          # Design rationale (READ FIRST)
├── IMPROVEMENTS_LOG.md          # Change history
└── QUICK_REFERENCE.md           # Daily reference guide

../../layer-specifications/
├── layer1-business-processes.md
├── layer2-application-specification.md
├── layer3-container-orchestration.md
├── layer4-physical-infrastructure.md
├── layer5-network-topology.md       # Network layer (CRITICAL)
└── layer6-security-infrastructure.md

../../ontology/
├── it-infrastructure-ontology.ttl   # OWL ontology
├── VISUAL_DIAGRAMS.md               # Mermaid diagrams
├── ONTOLOGY_REFERENCE.md            # Complete reference
└── USAGE_GUIDE.md                   # Usage examples

../../.kiro/steering/
├── tech.md                          # Tech stack & patterns
├── structure.md                     # Project structure
└── product.md                       # Product overview
```

---

## Common Tasks

### View Visual Diagrams
```bash
# Open in VS Code with Mermaid extension
code ../../ontology/VISUAL_DIAGRAMS.md

# Or view in browser
# Copy diagram to https://mermaid.live/
```

### Validate Ontology
```bash
# Check syntax
rapper -i turtle -o ntriples ../../ontology/it-infrastructure-ontology.ttl

# Validate with SHACL
pyshacl -s ../../ontology/shacl-shapes.ttl -d ../../ontology/sample-data-cloud.ttl
```

### Run Queries
```bash
# Run test queries
python ../../ontology/test_queries.py

# Interactive SPARQL
# Use Apache Jena or RDFLib
```

### Update Documentation
```bash
# After making changes, update:
1. IMPROVEMENTS_LOG.md - Add entry for the change
2. DESIGN_DECISIONS.md - Update if design rationale changes
3. QUICK_REFERENCE.md - Add new patterns if applicable

# Commit with descriptive message
git add .
git commit -m "Description of changes"
```

---

## Getting Help

### Questions About Design
- **Why was this designed this way?** → Read `DESIGN_DECISIONS.md`
- **What changed recently?** → Read `IMPROVEMENTS_LOG.md`
- **How do I model X?** → Check `QUICK_REFERENCE.md` patterns

### Questions About Implementation
- **What are the requirements?** → Read `requirements.md`
- **What's the architecture?** → Read `design.md`
- **What needs to be done?** → Read `tasks.md`

### Questions About Specific Layers
- **Network layer questions** → Read `layer5-network-topology.md`
- **Application layer questions** → Read `layer2-application-specification.md`
- **Container layer questions** → Read `layer3-container-orchestration.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-01 | Initial complete specification |
| 1.1.0 | 2024-12-01 | Network layer improvements (endpoints, device connections) |

---

## Contributing

When making changes:

1. ✅ Update the relevant specification document
2. ✅ Update the OWL ontology if needed
3. ✅ Update visual diagrams if relationships change
4. ✅ Add entry to `IMPROVEMENTS_LOG.md`
5. ✅ Update `QUICK_REFERENCE.md` if adding new patterns
6. ✅ Commit with descriptive message

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../../../LICENSE) file for details.

Copyright 2024 IT Infrastructure Ontology Contributors

---

**Maintained By**: IT Infrastructure Ontology Working Group  
**Last Updated**: 2024-12-01  
**Version**: 1.1.0
