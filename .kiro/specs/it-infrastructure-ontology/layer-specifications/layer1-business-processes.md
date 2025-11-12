# Layer 1: Business Processes - Detailed Specification

## Overview

Layer 1 represents the business perspective of IT infrastructure, capturing business capabilities, processes, services, and products that drive IT requirements. This layer provides the "why" behind IT investments and enables traceability from business outcomes to technical implementations.

**Layer Purpose**: Define what business outcomes and capabilities the IT infrastructure must support.

**Framework Sources**: 
- TOGAF Business Architecture Metamodel
- ArchiMate Business Layer
- ITIL Service Strategy

---

## Entity Type Specifications

### 1. BusinessProcess

**Definition**: A sequence of activities that produces a specific business outcome or delivers value to stakeholders.

**Description**: BusinessProcess represents operational workflows, procedures, or activities that the organization executes to achieve business objectives. Examples include "Order Fulfillment", "Customer Onboarding", "Invoice Processing", or "Product Development".

**OWL Class Definition**:
```turtle
:BusinessProcess
  rdf:type owl:Class ;
  rdfs:subClassOf :BusinessProcessLayer ;
  rdfs:label "Business Process" ;
  rdfs:comment "A sequence of activities that produces a business outcome" ;
  skos:example "Order Fulfillment, Customer Onboarding, Invoice Processing" .
```

**Attributes**:

| Attribute | Data Type | Mandatory | Enumeration Values | Framework Source | Description |
|-----------|-----------|-----------|-------------------|------------------|-------------|
| `name` | xsd:string | Yes | - | TOGAF | Business-friendly name of the process |
| `description` | xsd:string | No | - | TOGAF | Purpose, scope, and business context |
| `owner` | xsd:string | Yes | - | TOGAF | Business owner or stakeholder responsible |
| `criticality` | xsd:string | Yes | critical, high, medium, low | TOGAF | Business importance and priority |
| `lifecycle_status` | xsd:string | Yes | planned, active, deprecated, retired | TOGAF | Current operational state |
| `process_type` | xsd:string | No | core, supporting, management | ArchiMate | Classification of process role |
| `frequency` | xsd:string | No | real-time, hourly, daily, weekly, monthly, quarterly, annual, on-demand | ITIL | How often the process executes |
| `sla_target` | xsd:string | No | - | ITIL | Service level agreement target (e.g., "99.9% uptime", "< 2 hour response") |
| `business_value` | xsd:string | No | - | TOGAF | Quantified or qualitative business value delivered |

**Validation Rules**:
- `name` must be unique within the organization
- `owner` must reference a valid business stakeholder
- `lifecycle_status` transitions: planned → active → deprecated → retired
- If `lifecycle_status` is "retired", process should have no active relationships

---

### 2. BusinessCapability

**Definition**: An ability or capacity that a business possesses to achieve a specific purpose or outcome.

**Description**: BusinessCapability represents what the business can do, independent of how it does it. Capabilities are typically stable over time while processes and applications may change. Examples include "Customer Relationship Management", "Financial Reporting", "Supply Chain Management", or "Product Innovation".

**OWL Class Definition**:
```turtle
:BusinessCapability
  rdf:type owl:Class ;
  rdfs:subClassOf :BusinessProcessLayer ;
  rdfs:label "Business Capability" ;
  rdfs:comment "An ability that a business possesses to achieve specific outcomes" ;
  skos:example "Customer Relationship Management, Financial Reporting, Supply Chain Management" .
```

**Attributes**:

| Attribute | Data Type | Mandatory | Enumeration Values | Framework Source | Description |
|-----------|-----------|-----------|-------------------|------------------|-------------|
| `name` | xsd:string | Yes | - | TOGAF | Name of the capability |
| `description` | xsd:string | No | - | TOGAF | What the capability enables the business to do |
| `owner` | xsd:string | Yes | - | TOGAF | Business unit or executive owner |
| `criticality` | xsd:string | Yes | critical, high, medium, low | TOGAF | Strategic importance to the business |
| `lifecycle_status` | xsd:string | Yes | planned, active, deprecated, retired | TOGAF | Current state of the capability |
| `maturity_level` | xsd:string | No | initial, developing, defined, managed, optimizing | TOGAF | Capability maturity assessment |
| `capability_level` | xsd:integer | No | - | ArchiMate | Hierarchical level (1=strategic, 2=tactical, 3=operational) |
| `investment_priority` | xsd:string | No | high, medium, low | TOGAF | Priority for investment and improvement |

**Validation Rules**:
- `name` must be unique within the organization
- `capability_level` must be between 1 and 3 if specified
- `maturity_level` should align with organizational maturity assessment framework
- Parent-child capability relationships must maintain hierarchical consistency

---

### 3. BusinessService

**Definition**: A service that supports business operations and is delivered to internal or external customers.

**Description**: BusinessService represents an explicitly defined service offering that delivers value to business stakeholders. It abstracts the underlying implementation and focuses on what is delivered. Examples include "Customer Support Service", "Payment Processing Service", "Reporting Service", or "Authentication Service".

**OWL Class Definition**:
```turtle
:BusinessService
  rdf:type owl:Class ;
  rdfs:subClassOf :BusinessProcessLayer ;
  rdfs:label "Business Service" ;
  rdfs:comment "A service that supports business operations" ;
  skos:example "Customer Support Service, Payment Processing Service, Reporting Service" .
```

**Attributes**:

| Attribute | Data Type | Mandatory | Enumeration Values | Framework Source | Description |
|-----------|-----------|-----------|-------------------|------------------|-------------|
| `name` | xsd:string | Yes | - | TOGAF | Name of the business service |
| `description` | xsd:string | No | - | TOGAF | What the service provides |
| `owner` | xsd:string | Yes | - | ITIL | Service owner responsible for delivery |
| `criticality` | xsd:string | Yes | critical, high, medium, low | ITIL | Impact if service is unavailable |
| `lifecycle_status` | xsd:string | Yes | planned, active, deprecated, retired | ITIL | Current service lifecycle state |
| `service_type` | xsd:string | No | internal, external, shared | ArchiMate | Who consumes the service |
| `availability_target` | xsd:string | No | - | ITIL | Target availability (e.g., "99.9%", "24x7") |
| `performance_target` | xsd:string | No | - | ITIL | Target performance metrics |
| `cost_center` | xsd:string | No | - | ITIL | Financial cost center for the service |
| `service_catalog_id` | xsd:string | No | - | ITIL | Reference to service catalog entry |

**Validation Rules**:
- `name` must be unique within the service catalog
- `availability_target` should be specified for critical and high criticality services
- If `service_type` is "external", additional governance rules may apply
- Services with `lifecycle_status` "retired" should have migration plans documented

---

### 4. Product

**Definition**: A business product or offering delivered to customers or markets.

**Description**: Product represents tangible or intangible offerings that the business sells or provides to external customers. Products are supported by business capabilities and processes. Examples include "Mobile Banking App", "Insurance Policy", "Cloud Storage Subscription", or "Consulting Service Package".

**OWL Class Definition**:
```turtle
:Product
  rdf:type owl:Class ;
  rdfs:subClassOf :BusinessProcessLayer ;
  rdfs:label "Product" ;
  rdfs:comment "A business product or offering delivered to customers" ;
  skos:example "Mobile Banking App, Insurance Policy, Cloud Storage Subscription" .
```

**Attributes**:

| Attribute | Data Type | Mandatory | Enumeration Values | Framework Source | Description |
|-----------|-----------|-----------|-------------------|------------------|-------------|
| `name` | xsd:string | Yes | - | TOGAF | Product name |
| `description` | xsd:string | No | - | TOGAF | Product features and value proposition |
| `owner` | xsd:string | Yes | - | TOGAF | Product manager or business owner |
| `criticality` | xsd:string | Yes | critical, high, medium, low | TOGAF | Strategic importance to business |
| `lifecycle_status` | xsd:string | Yes | planned, active, deprecated, retired | TOGAF | Product lifecycle state |
| `product_type` | xsd:string | No | physical, digital, service, hybrid | ArchiMate | Nature of the product |
| `target_market` | xsd:string | No | - | TOGAF | Target customer segment or market |
| `revenue_stream` | xsd:string | No | - | TOGAF | How the product generates revenue |
| `launch_date` | xsd:date | No | - | TOGAF | Product launch or go-live date |
| `retirement_date` | xsd:date | No | - | TOGAF | Planned or actual retirement date |

**Validation Rules**:
- `name` must be unique within the product portfolio
- If `lifecycle_status` is "retired", `retirement_date` should be specified
- `launch_date` must be before `retirement_date` if both are specified
- Products should be linked to at least one BusinessCapability

---

## Intra-Layer Relationships

### Relationship: part_of

**Domain**: BusinessProcess, BusinessCapability  
**Range**: BusinessCapability  
**Cardinality**: Many-to-One  
**Inverse**: contains

**Description**: Represents hierarchical decomposition within the business layer. A BusinessProcess can be part of a BusinessCapability, or a BusinessCapability can be part of a higher-level BusinessCapability.

**Semantics**:
- Enables capability hierarchies (e.g., "Customer Service" contains "Complaint Handling")
- Enables process decomposition (e.g., "Order Fulfillment" is part of "Sales Management")
- Supports organizational structure modeling

**OWL Property Definition**:
```turtle
:part_of
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf (:BusinessProcess :BusinessCapability) ] ;
  rdfs:range :BusinessCapability ;
  owl:inverseOf :contains ;
  rdfs:label "part of" ;
  rdfs:comment "Indicates hierarchical containment relationship" .
```

**Usage Examples**:
- BusinessProcess "Order Entry" `part_of` BusinessCapability "Order Management"
- BusinessCapability "Payment Processing" `part_of` BusinessCapability "Financial Management"

**Validation Rules**:
- No circular relationships (A part_of B, B part_of A)
- Maximum hierarchy depth should be reasonable (e.g., 5 levels)
- Lifecycle status of child should be compatible with parent

---

### Relationship: enables

**Domain**: BusinessCapability  
**Range**: BusinessProcess  
**Cardinality**: One-to-Many  
**Inverse**: enabled_by

**Description**: Indicates that a BusinessCapability enables the execution of a BusinessProcess.

**Semantics**:
- Capabilities provide the organizational ability to execute processes
- One capability can enable multiple processes
- Processes require capabilities to function

**OWL Property Definition**:
```turtle
:enables
  rdf:type owl:ObjectProperty ;
  rdfs:domain :BusinessCapability ;
  rdfs:range :BusinessProcess ;
  owl:inverseOf :enabled_by ;
  rdfs:label "enables" ;
  rdfs:comment "Capability enables the execution of a process" .
```

**Usage Examples**:
- BusinessCapability "Customer Relationship Management" `enables` BusinessProcess "Customer Onboarding"
- BusinessCapability "Financial Reporting" `enables` BusinessProcess "Monthly Close"

**Validation Rules**:
- Enabled processes should have lifecycle_status compatible with enabling capability
- Critical processes should be enabled by capabilities with adequate maturity

---

### Relationship: supports

**Domain**: BusinessService  
**Range**: BusinessProcess, Product  
**Cardinality**: Many-to-Many  
**Inverse**: supported_by

**Description**: Indicates that a BusinessService supports the execution of a BusinessProcess or delivery of a Product.

**Semantics**:
- Services provide operational support to processes and products
- One service can support multiple processes/products
- Processes/products may require multiple services

**OWL Property Definition**:
```turtle
:supports
  rdf:type owl:ObjectProperty ;
  rdfs:domain :BusinessService ;
  rdfs:range [ owl:unionOf (:BusinessProcess :Product) ] ;
  owl:inverseOf :supported_by ;
  rdfs:label "supports" ;
  rdfs:comment "Service supports process or product delivery" .
```

**Usage Examples**:
- BusinessService "Authentication Service" `supports` BusinessProcess "User Login"
- BusinessService "Payment Gateway Service" `supports` Product "E-commerce Platform"

**Validation Rules**:
- Service availability_target should meet requirements of supported processes/products
- Critical processes should be supported by services with appropriate criticality

---

### Relationship: delivers

**Domain**: BusinessProcess  
**Range**: Product  
**Cardinality**: Many-to-Many  
**Inverse**: delivered_by

**Description**: Indicates that a BusinessProcess is involved in delivering a Product to customers.

**Semantics**:
- Processes operationalize product delivery
- Multiple processes may contribute to one product
- One process may support multiple products

**OWL Property Definition**:
```turtle
:delivers
  rdf:type owl:ObjectProperty ;
  rdfs:domain :BusinessProcess ;
  rdfs:range :Product ;
  owl:inverseOf :delivered_by ;
  rdfs:label "delivers" ;
  rdfs:comment "Process delivers product to customers" .
```

**Usage Examples**:
- BusinessProcess "Order Fulfillment" `delivers` Product "Online Retail Service"
- BusinessProcess "Policy Underwriting" `delivers` Product "Insurance Policy"

**Validation Rules**:
- Process frequency should align with product delivery requirements
- Retired processes should not deliver active products

---

## Cross-Layer Relationships (to Application Layer)

### Relationship: realized_by

**Domain**: BusinessProcess, BusinessCapability, BusinessService  
**Range**: Application (Layer 2)  
**Cardinality**: Many-to-Many  
**Inverse**: realizes

**Description**: Indicates that a business element is realized or implemented by one or more applications.

**Semantics**:
- Business requirements are fulfilled through IT applications
- One business element may require multiple applications
- One application may realize multiple business elements
- This is the primary bridge from business to technology

**OWL Property Definition**:
```turtle
:realized_by
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf (:BusinessProcess :BusinessCapability :BusinessService) ] ;
  rdfs:range :Application ;
  owl:inverseOf :realizes ;
  rdfs:label "realized by" ;
  rdfs:comment "Business element is implemented by application" .
```

**Usage Examples**:
- BusinessProcess "Order Processing" `realized_by` Application "Order Management System"
- BusinessCapability "Customer Analytics" `realized_by` Application "Analytics Platform"
- BusinessService "Payment Processing" `realized_by` Application "Payment Gateway"

**Validation Rules**:
- Critical business elements should have redundant application support
- Application lifecycle_status should be compatible with business element status
- Retired applications should not realize active business elements

---

### Relationship: requires

**Domain**: Product  
**Range**: Application (Layer 2)  
**Cardinality**: Many-to-Many  
**Inverse**: required_by

**Description**: Indicates that a Product requires specific applications to function.

**Semantics**:
- Products have direct dependencies on applications
- Enables impact analysis for product-to-technology mapping
- Supports product portfolio management

**OWL Property Definition**:
```turtle
:requires
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Product ;
  rdfs:range :Application ;
  owl:inverseOf :required_by ;
  rdfs:label "requires" ;
  rdfs:comment "Product requires application to function" .
```

**Usage Examples**:
- Product "Mobile Banking App" `requires` Application "Core Banking System"
- Product "Cloud Storage Service" `requires` Application "Storage Management Platform"

**Validation Rules**:
- All required applications must be operational for product to be available
- Product criticality should be reflected in required application criticality

---

## Relationship Properties and Metadata

All relationships in Layer 1 can have the following optional properties:

| Property | Data Type | Description |
|----------|-----------|-------------|
| `relationship_criticality` | xsd:string (critical, high, medium, low) | Importance of the relationship |
| `effective_date` | xsd:date | When the relationship became active |
| `end_date` | xsd:date | When the relationship ended or will end |
| `relationship_type` | xsd:string | Additional classification of the relationship |
| `notes` | xsd:string | Additional context or documentation |

---

## Cardinality Summary

| Relationship | Source | Target | Cardinality |
|--------------|--------|--------|-------------|
| part_of | BusinessProcess, BusinessCapability | BusinessCapability | Many-to-One |
| enables | BusinessCapability | BusinessProcess | One-to-Many |
| supports | BusinessService | BusinessProcess, Product | Many-to-Many |
| delivers | BusinessProcess | Product | Many-to-Many |
| realized_by | BusinessProcess, BusinessCapability, BusinessService | Application | Many-to-Many |
| requires | Product | Application | Many-to-Many |

---

## SHACL Validation Shapes

### BusinessProcess Shape

```turtle
:BusinessProcessShape
  a sh:NodeShape ;
  sh:targetClass :BusinessProcess ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
    sh:message "BusinessProcess must have exactly one non-empty name" ;
  ] ;
  sh:property [
    sh:path :owner ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:message "BusinessProcess must have exactly one owner" ;
  ] ;
  sh:property [
    sh:path :criticality ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "critical" "high" "medium" "low" ) ;
    sh:message "BusinessProcess must have criticality: critical, high, medium, or low" ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "planned" "active" "deprecated" "retired" ) ;
    sh:message "BusinessProcess must have lifecycle_status: planned, active, deprecated, or retired" ;
  ] ;
  sh:property [
    sh:path :process_type ;
    sh:maxCount 1 ;
    sh:in ( "core" "supporting" "management" ) ;
    sh:message "If specified, process_type must be: core, supporting, or management" ;
  ] ;
  sh:property [
    sh:path :frequency ;
    sh:maxCount 1 ;
    sh:in ( "real-time" "hourly" "daily" "weekly" "monthly" "quarterly" "annual" "on-demand" ) ;
  ] .
```

### BusinessCapability Shape

```turtle
:BusinessCapabilityShape
  a sh:NodeShape ;
  sh:targetClass :BusinessCapability ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
    sh:message "BusinessCapability must have exactly one non-empty name" ;
  ] ;
  sh:property [
    sh:path :owner ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:message "BusinessCapability must have exactly one owner" ;
  ] ;
  sh:property [
    sh:path :criticality ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "critical" "high" "medium" "low" ) ;
    sh:message "BusinessCapability must have criticality: critical, high, medium, or low" ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "planned" "active" "deprecated" "retired" ) ;
    sh:message "BusinessCapability must have lifecycle_status: planned, active, deprecated, or retired" ;
  ] ;
  sh:property [
    sh:path :maturity_level ;
    sh:maxCount 1 ;
    sh:in ( "initial" "developing" "defined" "managed" "optimizing" ) ;
  ] ;
  sh:property [
    sh:path :capability_level ;
    sh:maxCount 1 ;
    sh:datatype xsd:integer ;
    sh:minInclusive 1 ;
    sh:maxInclusive 3 ;
    sh:message "If specified, capability_level must be between 1 and 3" ;
  ] ;
  sh:property [
    sh:path :investment_priority ;
    sh:maxCount 1 ;
    sh:in ( "high" "medium" "low" ) ;
  ] .
```

### BusinessService Shape

```turtle
:BusinessServiceShape
  a sh:NodeShape ;
  sh:targetClass :BusinessService ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
    sh:message "BusinessService must have exactly one non-empty name" ;
  ] ;
  sh:property [
    sh:path :owner ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:message "BusinessService must have exactly one owner" ;
  ] ;
  sh:property [
    sh:path :criticality ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "critical" "high" "medium" "low" ) ;
    sh:message "BusinessService must have criticality: critical, high, medium, or low" ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "planned" "active" "deprecated" "retired" ) ;
    sh:message "BusinessService must have lifecycle_status: planned, active, deprecated, or retired" ;
  ] ;
  sh:property [
    sh:path :service_type ;
    sh:maxCount 1 ;
    sh:in ( "internal" "external" "shared" ) ;
  ] .
```

### Product Shape

```turtle
:ProductShape
  a sh:NodeShape ;
  sh:targetClass :Product ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
    sh:message "Product must have exactly one non-empty name" ;
  ] ;
  sh:property [
    sh:path :owner ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:message "Product must have exactly one owner" ;
  ] ;
  sh:property [
    sh:path :criticality ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "critical" "high" "medium" "low" ) ;
    sh:message "Product must have criticality: critical, high, medium, or low" ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "planned" "active" "deprecated" "retired" ) ;
    sh:message "Product must have lifecycle_status: planned, active, deprecated, or retired" ;
  ] ;
  sh:property [
    sh:path :product_type ;
    sh:maxCount 1 ;
    sh:in ( "physical" "digital" "service" "hybrid" ) ;
  ] ;
  sh:property [
    sh:path :launch_date ;
    sh:maxCount 1 ;
    sh:datatype xsd:date ;
  ] ;
  sh:property [
    sh:path :retirement_date ;
    sh:maxCount 1 ;
    sh:datatype xsd:date ;
  ] .
```

### Relationship Validation Shape

```turtle
:Layer1RelationshipShape
  a sh:NodeShape ;
  sh:targetSubjectsOf :part_of, :enables, :supports, :delivers, :realized_by, :requires ;
  sh:property [
    sh:path :relationship_criticality ;
    sh:maxCount 1 ;
    sh:in ( "critical" "high" "medium" "low" ) ;
  ] ;
  sh:property [
    sh:path :effective_date ;
    sh:maxCount 1 ;
    sh:datatype xsd:date ;
  ] ;
  sh:property [
    sh:path :end_date ;
    sh:maxCount 1 ;
    sh:datatype xsd:date ;
  ] .
```

---

## Usage Patterns and Examples

### Pattern 1: Capability Hierarchy

```turtle
# Strategic capability
:CustomerManagement
  a :BusinessCapability ;
  :name "Customer Management" ;
  :owner "Chief Customer Officer" ;
  :criticality "critical" ;
  :lifecycle_status "active" ;
  :capability_level 1 ;
  :maturity_level "managed" .

# Tactical capability
:CustomerOnboarding
  a :BusinessCapability ;
  :name "Customer Onboarding" ;
  :owner "Customer Operations Manager" ;
  :criticality "high" ;
  :lifecycle_status "active" ;
  :capability_level 2 ;
  :part_of :CustomerManagement .

# Operational process
:NewCustomerRegistration
  a :BusinessProcess ;
  :name "New Customer Registration" ;
  :owner "Onboarding Team Lead" ;
  :criticality "high" ;
  :lifecycle_status "active" ;
  :process_type "core" ;
  :frequency "real-time" ;
  :enabled_by :CustomerOnboarding .
```

### Pattern 2: Product Delivery Chain

```turtle
# Product
:MobileBankingApp
  a :Product ;
  :name "Mobile Banking App" ;
  :owner "Digital Banking Product Manager" ;
  :criticality "critical" ;
  :lifecycle_status "active" ;
  :product_type "digital" ;
  :launch_date "2020-01-15"^^xsd:date .

# Process delivering product
:MobileAccountAccess
  a :BusinessProcess ;
  :name "Mobile Account Access" ;
  :owner "Digital Banking Operations" ;
  :criticality "critical" ;
  :lifecycle_status "active" ;
  :process_type "core" ;
  :frequency "real-time" ;
  :delivers :MobileBankingApp .

# Service supporting process
:AuthenticationService
  a :BusinessService ;
  :name "Customer Authentication Service" ;
  :owner "Security Services Manager" ;
  :criticality "critical" ;
  :lifecycle_status "active" ;
  :service_type "internal" ;
  :availability_target "99.99%" ;
  :supports :MobileAccountAccess .
```

### Pattern 3: Business-to-Application Mapping

```turtle
# Business capability
:FinancialReporting
  a :BusinessCapability ;
  :name "Financial Reporting" ;
  :owner "CFO" ;
  :criticality "critical" ;
  :lifecycle_status "active" ;
  :capability_level 1 .

# Business process
:MonthlyFinancialClose
  a :BusinessProcess ;
  :name "Monthly Financial Close" ;
  :owner "Controller" ;
  :criticality "critical" ;
  :lifecycle_status "active" ;
  :process_type "core" ;
  :frequency "monthly" ;
  :sla_target "Complete within 5 business days" ;
  :enabled_by :FinancialReporting .

# Cross-layer relationship to application
:MonthlyFinancialClose
  :realized_by :ERPSystem, :ReportingPlatform .

:FinancialReporting
  :realized_by :ERPSystem, :ReportingPlatform, :DataWarehouse .
```

---

## Requirements Traceability

This specification addresses the following requirements:

- **Requirement 1.1**: Defines Business Processes layer as one of six infrastructure layers
- **Requirement 1.3**: Supports decomposition across layers through cross-layer relationships
- **Requirement 1.4**: Enables component decomposition (BusinessProcess → Application)
- **Requirement 2.1**: Defines relationship types for dependency representation
- **Requirement 2.2**: Supports directional relationships with inverse properties
- **Requirement 2.4**: Defines cardinality constraints for all relationship types
- **Requirement 8.1**: Defines minimal, non-overlapping attributes for Business Process layer
- **Requirement 8.2**: Sources attributes from TOGAF, ArchiMate, and ITIL frameworks
- **Requirement 8.3**: Documents framework source for each attribute
- **Requirement 8.5**: Specifies mandatory vs. optional attributes
- **Requirement 10.2**: Defines relationships between business processes and applications
- **Requirement 10.3**: Supports many-to-many relationships between business and IT

---

## Implementation Notes

1. **Namespace Prefix**: Use `:` for the ontology namespace (e.g., `http://example.org/it-infrastructure-ontology#`)
2. **Unique Identifiers**: Entity instances should use URI-based identifiers (e.g., `:BusinessProcess_OrderFulfillment`)
3. **Framework Citations**: Include `dcterms:source` annotations to cite specific framework documents
4. **Versioning**: Use OWL versioning properties (`owl:versionInfo`, `owl:priorVersion`) to track ontology evolution
5. **Documentation**: Use `rdfs:comment`, `rdfs:label`, and `skos:example` for human-readable documentation
6. **Extensibility**: Organizations can add custom attributes using separate namespaces (e.g., `custom:`)

---

## Next Steps

After implementing Layer 1, proceed to:
1. Define Layer 2: Application Layer entity types and relationships
2. Create sample instance data for Layer 1 entities
3. Test cross-layer queries from Business Processes to Applications
4. Validate SHACL shapes against sample data
5. Review with business stakeholders for completeness and accuracy
