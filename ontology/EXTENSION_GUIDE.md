# IT Infrastructure Ontology - Extension Guide

## Document Information

- **Version**: 1.0.0
- **Date**: 2024-01-15
- **Purpose**: Guide for extending and customizing the IT Infrastructure Ontology
- **Audience**: Ontology Engineers, Enterprise Architects, System Integrators

---

## Table of Contents

1. [Introduction](#introduction)
2. [Adding New Entity Types](#adding-new-entity-types)
3. [Adding New Frameworks](#adding-new-frameworks)
4. [Adding Custom Attributes](#adding-custom-attributes)
5. [Versioning Strategy](#versioning-strategy)
6. [Maintaining Consistency](#maintaining-consistency)
7. [Extension Examples](#extension-examples)

---

## Introduction

The IT Infrastructure Ontology is designed to be extensible while maintaining consistency and standards compliance. This guide provides detailed instructions for extending the ontology to meet specific organizational needs.

### Extension Principles

1. **Maintain layer separation**: New entities must belong to exactly one layer
2. **Follow framework alignment**: Source attributes from established frameworks when possible
3. **Preserve backward compatibility**: Avoid breaking changes to existing concepts
4. **Document thoroughly**: All extensions must be well-documented
5. **Validate rigorously**: Test extensions with SHACL validation

### When to Extend

Extend the ontology when:
- Your organization uses entity types not covered by the base ontology
- You need additional attributes specific to your environment
- You want to integrate a new framework or standard
- You need custom relationships for specific use cases

### When Not to Extend

Avoid extending when:
- Existing entity types can be used with custom attributes
- The extension would violate layer separation principles
- The extension duplicates existing concepts
- The extension is too specific to a single use case

---

## Adding New Entity Types

### Step-by-Step Process

#### Step 1: Identify the Appropriate Layer

Determine which layer the new entity type belongs to based on its abstraction level:

- **Layer 1**: Business-level concepts (processes, capabilities, services)
- **Layer 2**: Application-level concepts (applications, databases, APIs)
- **Layer 3**: Container-level concepts (containers, pods, orchestration)
- **Layer 4**: Infrastructure-level concepts (servers, storage, cloud resources)
- **Layer 5**: Network-level concepts (devices, paths, segments)
- **Layer 6**: Security-level concepts (firewalls, certificates, policies)

#### Step 2: Define the Entity Class

Create the OWL class definition:

```turtle
@prefix : <http://example.org/it-infrastructure-ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

:MyNewEntity
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;  # Choose appropriate layer
  rdfs:label "My New Entity" ;
  rdfs:comment "Brief description of the entity type" ;
  skos:definition "Formal definition of what this entity represents" ;
  skos:example "Example: A specific instance like 'API Gateway'" ;
  dcterms:source "Framework or standard that defines this concept" .
```

#### Step 3: Define Data Properties (Attributes)

Add attributes for the new entity type:

```turtle
# Mandatory attribute example
:myMandatoryAttribute
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :MyNewEntity ;
  rdfs:range xsd:string ;
  rdfs:label "My Mandatory Attribute" ;
  rdfs:comment "Description of what this attribute represents" ;
  dcterms:source "Framework source for this attribute" .

# Optional attribute example
:myOptionalAttribute
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :MyNewEntity ;
  rdfs:range xsd:integer ;
  rdfs:label "My Optional Attribute" ;
  rdfs:comment "Description of this optional attribute" ;
  dcterms:source "Framework source" .

# Enumeration attribute example
:myEnumAttribute
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :MyNewEntity ;
  rdfs:range xsd:string ;
  rdfs:label "My Enum Attribute" ;
  rdfs:comment "Attribute with controlled vocabulary" ;
  dcterms:source "Framework source" .
```

#### Step 4: Define Object Properties (Relationships)

Create relationships to connect the new entity to existing entities:

```turtle
# Intra-layer relationship
:myIntraLayerRelationship
  rdf:type owl:ObjectProperty ;
  rdfs:domain :MyNewEntity ;
  rdfs:range :ExistingEntityInSameLayer ;
  rdfs:label "My Intra-Layer Relationship" ;
  rdfs:comment "Relationship within the same layer" ;
  owl:inverseOf :inverseRelationship .

# Cross-layer relationship
:myCrossLayerRelationship
  rdf:type owl:ObjectProperty ;
  rdfs:domain :MyNewEntity ;
  rdfs:range :EntityInDifferentLayer ;
  rdfs:label "My Cross-Layer Relationship" ;
  rdfs:comment "Relationship across layers" ;
  owl:inverseOf :inverseRelationship .
```

#### Step 5: Create SHACL Validation Shapes

Define validation rules for the new entity:

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .

:MyNewEntityShape
  a sh:NodeShape ;
  sh:targetClass :MyNewEntity ;
  
  # Mandatory attribute validation
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
    sh:message "MyNewEntity must have exactly one name" ;
  ] ;
  
  # Enumeration validation
  sh:property [
    sh:path :myEnumAttribute ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "value1" "value2" "value3" ) ;
    sh:message "myEnumAttribute must be one of: value1, value2, value3" ;
  ] ;
  
  # Lifecycle status validation
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "inactive" "deprecated" "retired" ) ;
    sh:message "MyNewEntity must have a valid lifecycle_status" ;
  ] ;
  
  # Relationship validation
  sh:property [
    sh:path :myRelationship ;
    sh:class :TargetEntityType ;
    sh:minCount 0 ;
    sh:message "myRelationship must connect to TargetEntityType" ;
  ] .
```

#### Step 6: Document the New Entity

Create documentation in the appropriate layer specification file:

```markdown
### MyNewEntity

**Definition**: [Clear definition of what this entity represents]

**Framework Source**: [Framework or standard that defines this concept]

**OWL Class Definition**:
[Include the Turtle definition]

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | [Framework] | [Description] |
| myAttribute | xsd:string | 0..1 | optional | [Framework] | [Description] |

**Relationships**:

| Relationship | Domain | Range | Cardinality | Description |
|--------------|--------|-------|-------------|-------------|
| myRelationship | MyNewEntity | TargetEntity | Many-to-One | [Description] |

**Usage Example**:
[Include Turtle example]

**Query Patterns**:
[Include SPARQL and Cypher examples]
```

#### Step 7: Test the Extension

1. **Create sample instances**:
```turtle
:MyNewEntityInstance a :MyNewEntity ;
  :name "Example Instance" ;
  :myEnumAttribute "value1" ;
  :lifecycle_status "active" ;
  :myRelationship :ExistingEntity .
```

2. **Validate against SHACL shapes**:
```bash
pyshacl -s shacl-shapes.ttl -d sample-data.ttl
```

3. **Test queries**:
```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?entity ?name
WHERE {
  ?entity a :MyNewEntity ;
          :name ?name .
}
```

---

## Adding New Frameworks

### Framework Integration Process

#### Step 1: Analyze the Framework

1. **Study the framework metamodel**:
   - Identify core concepts and entity types
   - Extract attribute definitions and data types
   - Map relationships and cardinality constraints
   - Understand semantic meanings

2. **Document framework concepts**:
   - Create a framework analysis document
   - List all relevant concepts
   - Note overlaps with existing ontology concepts
   - Identify unique concepts not yet in ontology

#### Step 2: Map Framework to Ontology Layers

Create a mapping table:

| Framework Concept | Ontology Layer | Ontology Entity Type | Mapping Notes |
|-------------------|----------------|----------------------|---------------|
| [Framework Concept 1] | Layer X | [Entity Type] | [Notes] |
| [Framework Concept 2] | Layer Y | [New Entity Type] | [Notes] |

#### Step 3: Extract Attributes

For each framework concept, extract attributes:

```markdown
### Framework: [Framework Name]

#### Concept: [Framework Concept]

**Attributes**:

| Framework Attribute | Data Type | Ontology Property | Mapping Notes |
|---------------------|-----------|-------------------|---------------|
| [Attribute 1] | [Type] | :frameworkAttribute1 | [Notes] |
| [Attribute 2] | [Type] | :frameworkAttribute2 | [Notes] |
```

#### Step 4: Define Framework-Sourced Properties

Add new properties sourced from the framework:

```turtle
@prefix : <http://example.org/it-infrastructure-ontology#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

:frameworkAttribute1
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :RelevantEntityType ;
  rdfs:range xsd:string ;
  rdfs:label "Framework Attribute 1" ;
  rdfs:comment "Description from framework documentation" ;
  dcterms:source "Framework Name - Concept Name" .

:frameworkAttribute2
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :RelevantEntityType ;
  rdfs:range xsd:integer ;
  rdfs:label "Framework Attribute 2" ;
  rdfs:comment "Description from framework documentation" ;
  dcterms:source "Framework Name - Concept Name" .
```

#### Step 5: Update Entity Type Definitions

Add framework source to existing entity types:

```turtle
:ExistingEntity
  dcterms:source "TOGAF, CIM, NewFramework" .  # Add new framework
```

#### Step 6: Create Framework Mapping Documentation

Create `framework-analysis/newframework-analysis.md`:

```markdown
# New Framework Analysis

## Overview

[Description of the framework]

## Framework Concepts

### Concept 1: [Name]

**Definition**: [Framework definition]

**Ontology Mapping**: Maps to :EntityType in Layer X

**Attributes**:
- [List attributes and mappings]

**Relationships**:
- [List relationships and mappings]

## Mapping Summary

[Create comprehensive mapping table]

## Integration Notes

[Document any special considerations or limitations]
```

#### Step 7: Update Framework Mapping Summary

Add to `framework-analysis/framework-mapping-summary.md`:

```markdown
### New Framework

| Ontology Layer | Framework Module | Mapped Concepts |
|----------------|------------------|-----------------|
| Layer X | [Module] | [Concepts] |
```

### Example: Adding COBIT Framework

```turtle
# COBIT-sourced attributes for governance
:governanceLevel
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :BusinessProcess ;
  rdfs:range xsd:string ;
  rdfs:label "Governance Level" ;
  rdfs:comment "COBIT governance maturity level" ;
  dcterms:source "COBIT 2019 - Governance System" .

:riskLevel
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :BusinessProcess ;
  rdfs:range xsd:string ;
  rdfs:label "Risk Level" ;
  rdfs:comment "COBIT risk assessment level" ;
  dcterms:source "COBIT 2019 - Risk Management" .

# Update BusinessProcess with COBIT source
:BusinessProcess
  dcterms:source "TOGAF Business Architecture, ArchiMate Business Layer, COBIT 2019" .
```

---

## Adding Custom Attributes

### Custom Attribute Guidelines

Custom attributes should be used when:
- Organization-specific metadata is needed
- Framework-sourced attributes don't cover the requirement
- Temporary attributes are needed for migration or integration

### Custom Namespace Strategy

Use a separate namespace for custom attributes:

```turtle
@prefix : <http://example.org/it-infrastructure-ontology#> .
@prefix custom: <http://example.org/custom#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Define custom namespace
<http://example.org/custom#>
  rdf:type owl:Ontology ;
  rdfs:label "Custom Extensions for IT Infrastructure Ontology" ;
  rdfs:comment "Organization-specific custom attributes" ;
  owl:imports <http://example.org/it-infrastructure-ontology> .
```

### Defining Custom Attributes

```turtle
# Custom attribute for cost center
custom:costCenter
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:string ;
  rdfs:label "Cost Center" ;
  rdfs:comment "Organization cost center code" ;
  dcterms:source "Internal Finance System" .

# Custom attribute for deployment region
custom:deploymentRegion
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:string ;
  rdfs:label "Deployment Region" ;
  rdfs:comment "Geographic deployment region" ;
  dcterms:source "Internal Cloud Management" .

# Custom attribute for business unit
custom:businessUnit
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:string ;
  rdfs:label "Business Unit" ;
  rdfs:comment "Owning business unit" ;
  dcterms:source "Internal Organization Structure" .

# Custom enumeration attribute
custom:complianceStatus
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:string ;
  rdfs:label "Compliance Status" ;
  rdfs:comment "Internal compliance audit status" ;
  dcterms:source "Internal Compliance System" .
```

### Using Custom Attributes

```turtle
@prefix : <http://example.org/it-infrastructure-ontology#> .
@prefix custom: <http://example.org/custom#> .

:OrderManagementSystem a :Application ;
  # Standard attributes
  :name "Order Management System" ;
  :application_type "monolithic" ;
  :deployment_model "vm_based" ;
  :lifecycle_status "production" ;
  
  # Custom attributes
  custom:costCenter "CC-12345" ;
  custom:deploymentRegion "us-east-1" ;
  custom:businessUnit "Sales Operations" ;
  custom:complianceStatus "compliant" .
```

### Custom Attribute Validation

Create SHACL shapes for custom attributes:

```turtle
@prefix custom: <http://example.org/custom#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

custom:CustomApplicationShape
  a sh:NodeShape ;
  sh:targetClass :Application ;
  
  # Validate cost center format
  sh:property [
    sh:path custom:costCenter ;
    sh:datatype xsd:string ;
    sh:pattern "^CC-[0-9]{5}$" ;
    sh:message "Cost center must match pattern: CC-12345" ;
  ] ;
  
  # Validate deployment region
  sh:property [
    sh:path custom:deploymentRegion ;
    sh:datatype xsd:string ;
    sh:in ( "us-east-1" "us-west-2" "eu-west-1" "ap-southeast-1" ) ;
    sh:message "Deployment region must be a valid region code" ;
  ] ;
  
  # Validate compliance status
  sh:property [
    sh:path custom:complianceStatus ;
    sh:datatype xsd:string ;
    sh:in ( "compliant" "non-compliant" "pending" "exempt" ) ;
    sh:message "Compliance status must be valid" ;
  ] .
```

### Custom Attribute Documentation

Document custom attributes in a separate file `custom-extensions.md`:

```markdown
# Custom Extensions

## Custom Attributes

### costCenter

**Domain**: Application  
**Range**: xsd:string  
**Cardinality**: 0..1  
**Pattern**: CC-[0-9]{5}  
**Description**: Organization cost center code for billing and chargeback  
**Source**: Internal Finance System  
**Example**: "CC-12345"

### deploymentRegion

**Domain**: Application  
**Range**: xsd:string  
**Cardinality**: 0..1  
**Valid Values**: us-east-1, us-west-2, eu-west-1, ap-southeast-1  
**Description**: Geographic deployment region for the application  
**Source**: Internal Cloud Management  
**Example**: "us-east-1"

## Usage Examples

[Include examples]

## Validation Rules

[Include SHACL shapes]
```

---

## Versioning Strategy

### Semantic Versioning

The ontology follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible changes (e.g., removing entity types, changing relationship semantics)
- **MINOR**: Backward-compatible additions (e.g., new entity types, new attributes)
- **PATCH**: Backward-compatible fixes (e.g., documentation updates, bug fixes)

### Version Declaration

```turtle
<http://example.org/it-infrastructure-ontology>
  a owl:Ontology ;
  owl:versionInfo "1.0.0" ;
  owl:versionIRI <http://example.org/it-infrastructure-ontology/1.0.0> ;
  owl:priorVersion <http://example.org/it-infrastructure-ontology/0.9.0> ;
  dcterms:created "2024-01-01"^^xsd:date ;
  dcterms:modified "2024-01-15"^^xsd:date ;
  rdfs:label "IT Infrastructure and Application Dependency Ontology" ;
  rdfs:comment "Version 1.0.0 - Initial release" .
```

### Version Compatibility

#### Backward Compatibility Rules

1. **MINOR versions** must be backward compatible:
   - New entity types can be added
   - New attributes can be added
   - New relationships can be added
   - Existing concepts must not be removed or changed

2. **MAJOR versions** may break compatibility:
   - Entity types can be removed
   - Attributes can be removed
   - Relationship semantics can change
   - Layer assignments can change

#### Deprecation Process

When deprecating concepts:

1. **Mark as deprecated** in current version:
```turtle
:DeprecatedEntity
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  owl:deprecated true ;
  rdfs:comment "DEPRECATED: Use :NewEntity instead. Will be removed in version 2.0.0" .
```

2. **Provide migration path**:
```markdown
## Deprecation Notice

### Deprecated: DeprecatedEntity

**Deprecated in**: Version 1.5.0  
**Will be removed in**: Version 2.0.0  
**Replacement**: Use :NewEntity instead

**Migration Guide**:
1. Update all instances of :DeprecatedEntity to :NewEntity
2. Map attributes as follows:
   - :oldAttribute → :newAttribute
3. Update relationships:
   - :oldRelationship → :newRelationship
```

3. **Remove in next MAJOR version**

### Version Migration

#### Migration Script Example

```python
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

ONT = Namespace("http://example.org/it-infrastructure-ontology#")

def migrate_v1_to_v2(input_file, output_file):
    """Migrate data from version 1.x to 2.0."""
    
    # Load v1 data
    g = Graph()
    g.parse(input_file, format="turtle")
    
    # Migration 1: Replace deprecated entity types
    for s, p, o in g.triples((None, RDF.type, ONT.DeprecatedEntity)):
        g.remove((s, p, o))
        g.add((s, RDF.type, ONT.NewEntity))
    
    # Migration 2: Rename attributes
    for s, p, o in g.triples((None, ONT.oldAttribute, None)):
        g.remove((s, p, o))
        g.add((s, ONT.newAttribute, o))
    
    # Migration 3: Update relationship semantics
    for s, p, o in g.triples((None, ONT.oldRelationship, None)):
        g.remove((s, p, o))
        g.add((s, ONT.newRelationship, o))
    
    # Save v2 data
    g.serialize(output_file, format="turtle")
    print(f"Migration complete: {input_file} → {output_file}")

# Usage
migrate_v1_to_v2("data-v1.ttl", "data-v2.ttl")
```

### Change Log

Maintain a CHANGELOG.md file:

```markdown
# Changelog

All notable changes to this ontology will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-15

### Added
- New entity type: APIGateway in Layer 2
- New relationship: routes_through for API routing

### Changed
- BREAKING: Renamed :oldAttribute to :newAttribute
- BREAKING: Changed :oldRelationship semantics

### Deprecated
- Nothing

### Removed
- BREAKING: Removed :DeprecatedEntity (deprecated in 1.5.0)

### Fixed
- Fixed cardinality constraint on :runs_on relationship

## [1.5.0] - 2024-06-15

### Added
- New entity type: ServiceMesh in Layer 3
- New attributes for cloud-native deployments

### Deprecated
- :DeprecatedEntity - Use :NewEntity instead (will be removed in 2.0.0)

## [1.0.0] - 2024-01-15

### Added
- Initial release with 50+ entity types
- Six-layer architecture
- SHACL validation shapes
- Framework mappings for TOGAF, CIM, ITIL, ArchiMate, Kubernetes
```

---

## Maintaining Consistency

### Consistency Checks

#### 1. Layer Disjointness

Ensure entities belong to exactly one layer:

```sparql
# Check for entities in multiple layers
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?entity (COUNT(DISTINCT ?layer) AS ?layerCount)
WHERE {
  ?entity a ?type .
  ?type rdfs:subClassOf+ ?layer .
  ?layer rdfs:subClassOf :InfrastructureEntity .
  FILTER(?layer != :InfrastructureEntity)
}
GROUP BY ?entity
HAVING (COUNT(DISTINCT ?layer) > 1)
```

#### 2. Mandatory Attributes

Verify all entities have required attributes:

```sparql
# Check for entities missing mandatory attributes
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?entity ?type
WHERE {
  ?entity a ?type .
  ?type rdfs:subClassOf+ :InfrastructureEntity .
  FILTER NOT EXISTS { ?entity :name ?name }
}
```

#### 3. Relationship Validity

Check that relationships connect appropriate entity types:

```sparql
# Check for invalid cross-layer relationships
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?source ?relationship ?target
WHERE {
  ?source ?relationship ?target .
  ?relationship rdfs:domain ?domainClass .
  ?relationship rdfs:range ?rangeClass .
  ?source a ?sourceType .
  ?target a ?targetType .
  FILTER NOT EXISTS {
    ?sourceType rdfs:subClassOf* ?domainClass .
    ?targetType rdfs:subClassOf* ?rangeClass .
  }
}
```

### Consistency Maintenance Script

```python
#!/usr/bin/env python3
"""Check ontology consistency."""

from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery

ONT = Namespace("http://example.org/it-infrastructure-ontology#")

def check_consistency(ontology_file, data_file):
    """Run consistency checks on ontology and data."""
    
    # Load ontology and data
    g = Graph()
    g.parse(ontology_file, format="turtle")
    g.parse(data_file, format="turtle")
    
    issues = []
    
    # Check 1: Layer disjointness
    query1 = prepareQuery("""
        PREFIX : <http://example.org/it-infrastructure-ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?entity (COUNT(DISTINCT ?layer) AS ?layerCount)
        WHERE {
            ?entity a ?type .
            ?type rdfs:subClassOf+ ?layer .
            ?layer rdfs:subClassOf :InfrastructureEntity .
            FILTER(?layer != :InfrastructureEntity)
        }
        GROUP BY ?entity
        HAVING (COUNT(DISTINCT ?layer) > 1)
    """)
    
    results1 = g.query(query1)
    if len(results1) > 0:
        issues.append(f"Layer disjointness violation: {len(results1)} entities in multiple layers")
    
    # Check 2: Mandatory attributes
    query2 = prepareQuery("""
        PREFIX : <http://example.org/it-infrastructure-ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?entity ?type
        WHERE {
            ?entity a ?type .
            ?type rdfs:subClassOf+ :InfrastructureEntity .
            FILTER NOT EXISTS { ?entity :name ?name }
        }
    """)
    
    results2 = g.query(query2)
    if len(results2) > 0:
        issues.append(f"Missing mandatory attributes: {len(results2)} entities without name")
    
    # Report results
    if len(issues) == 0:
        print("✓ All consistency checks passed")
        return True
    else:
        print("✗ Consistency issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False

# Usage
check_consistency("it-infrastructure-ontology.ttl", "instance-data.ttl")
```

### Guidelines for Maintaining Consistency

1. **Run validation after every change**: Use SHACL validation and consistency checks
2. **Review changes with stakeholders**: Ensure changes align with organizational needs
3. **Test with sample data**: Validate extensions with realistic data
4. **Document all changes**: Update documentation and changelog
5. **Version appropriately**: Follow semantic versioning rules
6. **Maintain backward compatibility**: Avoid breaking changes in MINOR versions
7. **Provide migration paths**: Document how to migrate from deprecated concepts

---

## Extension Examples

### Example 1: Adding Edge Computing Entity Type

#### Scenario
Organization needs to model edge computing devices not covered by existing entity types.

#### Solution

**Step 1: Define the entity class**

```turtle
@prefix : <http://example.org/it-infrastructure-ontology#> .

:EdgeDevice
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Edge Device" ;
  rdfs:comment "An edge computing device deployed at remote locations" ;
  skos:definition "A computing device deployed at the edge of the network, closer to data sources" ;
  skos:example "IoT gateway, edge server, industrial controller" ;
  dcterms:source "Edge Computing Consortium - Edge Computing Reference Architecture" .
```

**Step 2: Define attributes**

```turtle
:edgeDeviceType
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :EdgeDevice ;
  rdfs:range xsd:string ;
  rdfs:label "Edge Device Type" ;
  rdfs:comment "Type of edge device" ;
  dcterms:source "Edge Computing Consortium" .

:connectivityType
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :EdgeDevice ;
  rdfs:range xsd:string ;
  rdfs:label "Connectivity Type" ;
  rdfs:comment "Network connectivity type (4G, 5G, WiFi, Ethernet)" ;
  dcterms:source "Edge Computing Consortium" .

:processingCapacity
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :EdgeDevice ;
  rdfs:range xsd:decimal ;
  rdfs:label "Processing Capacity" ;
  rdfs:comment "Processing capacity in GFLOPS" ;
  dcterms:source "Edge Computing Consortium" .
```

**Step 3: Create SHACL shape**

```turtle
:EdgeDeviceShape
  a sh:NodeShape ;
  sh:targetClass :EdgeDevice ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :edgeDeviceType ;
    sh:minCount 1 ;
    sh:in ( "iot_gateway" "edge_server" "industrial_controller" "smart_sensor" ) ;
  ] ;
  sh:property [
    sh:path :connectivityType ;
    sh:in ( "4g" "5g" "wifi" "ethernet" "lora" "satellite" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:in ( "provisioning" "running" "stopped" "maintenance" "terminated" ) ;
  ] .
```

**Step 4: Create instance**

```turtle
:EdgeGateway01 a :EdgeDevice ;
  :name "Edge Gateway 01" ;
  :edgeDeviceType "iot_gateway" ;
  :connectivityType "5g" ;
  :processingCapacity 10.5 ;
  :location "Manufacturing Plant - Building A" ;
  :lifecycle_status "running" .
```

---

### Example 2: Adding Serverless Function Entity Type

#### Scenario
Organization uses serverless functions (AWS Lambda, Azure Functions) extensively.

#### Solution

```turtle
:ServerlessFunction
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
  rdfs:label "Serverless Function" ;
  rdfs:comment "A serverless function (FaaS)" ;
  skos:definition "A function-as-a-service deployment running on cloud provider infrastructure" ;
  dcterms:source "AWS Lambda API, Azure Functions API, GCP Cloud Functions API" .

:functionRuntime
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :ServerlessFunction ;
  rdfs:range xsd:string ;
  rdfs:label "Function Runtime" ;
  rdfs:comment "Runtime environment (e.g., python3.9, nodejs18, java11)" ;
  dcterms:source "Cloud Provider APIs" .

:memoryMB
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :ServerlessFunction ;
  rdfs:range xsd:integer ;
  rdfs:label "Memory MB" ;
  rdfs:comment "Allocated memory in megabytes" ;
  dcterms:source "Cloud Provider APIs" .

:timeoutSeconds
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :ServerlessFunction ;
  rdfs:range xsd:integer ;
  rdfs:label "Timeout Seconds" ;
  rdfs:comment "Function timeout in seconds" ;
  dcterms:source "Cloud Provider APIs" .

# Instance example
:OrderProcessingFunction a :ServerlessFunction ;
  :name "Order Processing Function" ;
  :application_type "microservice" ;
  :deployment_model "serverless" ;
  :functionRuntime "python3.9" ;
  :memoryMB 512 ;
  :timeoutSeconds 30 ;
  :lifecycle_status "production" ;
  :uses :OrderDB .
```

---

### Example 3: Adding Custom Compliance Attributes

#### Scenario
Organization needs to track compliance certifications and audit status.

#### Solution

```turtle
@prefix custom: <http://example.org/custom#> .

# Custom compliance attributes
custom:complianceCertifications
  rdf:type owl:DatatypeProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:string ;
  rdfs:label "Compliance Certifications" ;
  rdfs:comment "List of compliance certifications (e.g., SOC2, ISO27001, HIPAA)" ;
  dcterms:source "Internal Compliance System" .

custom:lastAuditDate
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:date ;
  rdfs:label "Last Audit Date" ;
  rdfs:comment "Date of last compliance audit" ;
  dcterms:source "Internal Compliance System" .

custom:nextAuditDate
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:date ;
  rdfs:label "Next Audit Date" ;
  rdfs:comment "Scheduled date for next compliance audit" ;
  dcterms:source "Internal Compliance System" .

custom:complianceOfficer
  rdf:type owl:DatatypeProperty, owl:FunctionalProperty ;
  rdfs:domain :Application ;
  rdfs:range xsd:string ;
  rdfs:label "Compliance Officer" ;
  rdfs:comment "Name of responsible compliance officer" ;
  dcterms:source "Internal Compliance System" .

# SHACL validation for custom attributes
custom:ComplianceShape
  a sh:NodeShape ;
  sh:targetClass :Application ;
  sh:property [
    sh:path custom:lastAuditDate ;
    sh:datatype xsd:date ;
    sh:maxCount 1 ;
  ] ;
  sh:property [
    sh:path custom:nextAuditDate ;
    sh:datatype xsd:date ;
    sh:maxCount 1 ;
  ] ;
  # Ensure next audit is after last audit
  sh:sparql [
    sh:message "Next audit date must be after last audit date" ;
    sh:select """
      PREFIX custom: <http://example.org/custom#>
      SELECT $this
      WHERE {
        $this custom:lastAuditDate ?last ;
              custom:nextAuditDate ?next .
        FILTER(?next <= ?last)
      }
    """ ;
  ] .

# Usage example
:PaymentProcessingApp a :Application ;
  :name "Payment Processing Application" ;
  :application_type "microservice" ;
  :deployment_model "containerized" ;
  :lifecycle_status "production" ;
  custom:complianceCertifications "SOC2, PCI-DSS, ISO27001" ;
  custom:lastAuditDate "2024-01-15"^^xsd:date ;
  custom:nextAuditDate "2024-07-15"^^xsd:date ;
  custom:complianceOfficer "Jane Smith" .
```

---

## Summary

This extension guide provides comprehensive instructions for:

1. **Adding new entity types** with proper layer assignment and validation
2. **Integrating new frameworks** with complete mapping and documentation
3. **Adding custom attributes** using separate namespaces
4. **Versioning** with semantic versioning and migration paths
5. **Maintaining consistency** through validation and checks

### Key Takeaways

- Always maintain layer separation
- Document all extensions thoroughly
- Use framework sources when possible
- Validate rigorously with SHACL
- Follow semantic versioning
- Provide migration paths for breaking changes
- Test extensions with sample data

### Next Steps

1. Review the ontology reference documentation
2. Study existing entity types and relationships
3. Plan your extensions carefully
4. Test thoroughly before deployment
5. Document for future maintainers

---

**Document Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Status**: Complete

