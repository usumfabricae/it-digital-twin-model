# Layer 1: Business Processes - Relationship Guide

## Overview

This document provides detailed guidance on using relationships within Layer 1 (Business Processes) and cross-layer relationships to Layer 2 (Application Layer). It includes relationship semantics, cardinality constraints, usage patterns, validation rules, and query examples.

---

## Relationship Catalog

### Summary Table

| Relationship | Type | Source Layer | Target Layer | Cardinality | Purpose |
|--------------|------|--------------|--------------|-------------|---------|
| `part_of` | Intra-layer | Layer 1 | Layer 1 | Many-to-One | Hierarchical decomposition |
| `enables` | Intra-layer | Layer 1 | Layer 1 | One-to-Many | Capability enables process |
| `supports` | Intra-layer | Layer 1 | Layer 1 | Many-to-Many | Service supports process/product |
| `delivers` | Intra-layer | Layer 1 | Layer 1 | Many-to-Many | Process delivers product |
| `realized_by` | Cross-layer | Layer 1 | Layer 2 | Many-to-Many | Business realized by application |
| `requires` | Cross-layer | Layer 1 | Layer 2 | Many-to-Many | Product requires application |

---

## Intra-Layer Relationships (Within Business Process Layer)

### 1. part_of

**Full Specification**:
- **Domain**: BusinessProcess OR BusinessCapability
- **Range**: BusinessCapability
- **Cardinality**: Many-to-One (many processes/capabilities can be part of one capability)
- **Inverse**: `contains`
- **Transitivity**: Yes (if A part_of B and B part_of C, then A part_of C)

**Semantic Rules**:
1. Creates hierarchical structures within the business layer
2. Child elements inherit context from parent capabilities
3. No circular dependencies allowed
4. Maximum recommended depth: 5 levels

**Usage Scenarios**:

#### Scenario 1: Capability Decomposition
```turtle
# Level 1: Strategic capability
:EnterpriseResourcePlanning
  a :BusinessCapability ;
  :name "Enterprise Resource Planning" ;
  :capability_level 1 .

# Level 2: Tactical capabilities
:FinancialManagement
  a :BusinessCapability ;
  :name "Financial Management" ;
  :capability_level 2 ;
  :part_of :EnterpriseResourcePlanning .

:SupplyChainManagement
  a :BusinessCapability ;
  :name "Supply Chain Management" ;
  :capability_level 2 ;
  :part_of :EnterpriseResourcePlanning .

# Level 3: Operational capabilities
:AccountsPayable
  a :BusinessCapability ;
  :name "Accounts Payable" ;
  :capability_level 3 ;
  :part_of :FinancialManagement .
```

#### Scenario 2: Process Decomposition
```turtle
# Parent capability
:OrderManagement
  a :BusinessCapability ;
  :name "Order Management" .

# Child processes
:OrderEntry
  a :BusinessProcess ;
  :name "Order Entry" ;
  :part_of :OrderManagement .

:OrderValidation
  a :BusinessProcess ;
  :name "Order Validation" ;
  :part_of :OrderManagement .

:OrderFulfillment
  a :BusinessProcess ;
  :name "Order Fulfillment" ;
  :part_of :OrderManagement .
```

**Validation Rules**:
```sparql
# Check for circular dependencies
SELECT ?entity1 ?entity2
WHERE {
  ?entity1 :part_of+ ?entity2 .
  ?entity2 :part_of+ ?entity1 .
}
# Should return empty result

# Check hierarchy depth
SELECT ?entity (COUNT(?ancestor) AS ?depth)
WHERE {
  ?entity :part_of+ ?ancestor .
}
GROUP BY ?entity
HAVING (COUNT(?ancestor) > 5)
# Should return empty result or flag for review
```

**Query Patterns**:

```sparql
# Find all descendants of a capability
SELECT ?descendant ?type
WHERE {
  ?descendant :part_of+ :CustomerManagement .
  ?descendant a ?type .
}

# Find the top-level capability for a process
SELECT ?topCapability
WHERE {
  :OrderEntry :part_of+ ?topCapability .
  FILTER NOT EXISTS { ?topCapability :part_of ?parent }
}

# Find all siblings (entities with same parent)
SELECT ?sibling
WHERE {
  :OrderEntry :part_of ?parent .
  ?sibling :part_of ?parent .
  FILTER(?sibling != :OrderEntry)
}
```

---

### 2. enables

**Full Specification**:
- **Domain**: BusinessCapability
- **Range**: BusinessProcess
- **Cardinality**: One-to-Many (one capability enables many processes)
- **Inverse**: `enabled_by`
- **Transitivity**: No

**Semantic Rules**:
1. Capabilities provide the organizational ability to execute processes
2. A process must be enabled by at least one capability
3. Capability maturity affects process effectiveness
4. Capability lifecycle status constrains process execution

**Usage Scenarios**:

#### Scenario 1: Single Capability Enables Multiple Processes
```turtle
:CustomerRelationshipManagement
  a :BusinessCapability ;
  :name "Customer Relationship Management" ;
  :maturity_level "managed" ;
  :enables :CustomerOnboarding, :CustomerSupport, :CustomerRetention .

:CustomerOnboarding
  a :BusinessProcess ;
  :name "Customer Onboarding" ;
  :enabled_by :CustomerRelationshipManagement .

:CustomerSupport
  a :BusinessProcess ;
  :name "Customer Support" ;
  :enabled_by :CustomerRelationshipManagement .

:CustomerRetention
  a :BusinessProcess ;
  :name "Customer Retention" ;
  :enabled_by :CustomerRelationshipManagement .
```

#### Scenario 2: Process Enabled by Multiple Capabilities
```turtle
:CrossBorderPayment
  a :BusinessProcess ;
  :name "Cross-Border Payment Processing" ;
  :enabled_by :PaymentProcessing, :ComplianceManagement, :CurrencyExchange .

:PaymentProcessing
  a :BusinessCapability ;
  :enables :CrossBorderPayment .

:ComplianceManagement
  a :BusinessCapability ;
  :enables :CrossBorderPayment .

:CurrencyExchange
  a :BusinessCapability ;
  :enables :CrossBorderPayment .
```

**Validation Rules**:
```sparql
# Find processes without enabling capabilities
SELECT ?process
WHERE {
  ?process a :BusinessProcess .
  FILTER NOT EXISTS { ?process :enabled_by ?capability }
}
# Should return empty result

# Find capability-process mismatches in lifecycle status
SELECT ?capability ?process ?capStatus ?procStatus
WHERE {
  ?capability :enables ?process .
  ?capability :lifecycle_status ?capStatus .
  ?process :lifecycle_status ?procStatus .
  FILTER(?capStatus = "retired" && ?procStatus = "active")
}
# Should return empty result
```

**Query Patterns**:

```sparql
# Find all processes enabled by a capability
SELECT ?process ?criticality
WHERE {
  :CustomerRelationshipManagement :enables ?process .
  ?process :criticality ?criticality .
}
ORDER BY ?criticality

# Find capabilities that enable critical processes
SELECT ?capability (COUNT(?process) AS ?criticalProcessCount)
WHERE {
  ?capability :enables ?process .
  ?process :criticality "critical" .
}
GROUP BY ?capability
ORDER BY DESC(?criticalProcessCount)

# Find capability gaps (low maturity enabling critical processes)
SELECT ?capability ?maturity ?process
WHERE {
  ?capability :enables ?process .
  ?capability :maturity_level ?maturity .
  ?process :criticality "critical" .
  FILTER(?maturity IN ("initial", "developing"))
}
```

---

### 3. supports

**Full Specification**:
- **Domain**: BusinessService
- **Range**: BusinessProcess OR Product
- **Cardinality**: Many-to-Many
- **Inverse**: `supported_by`
- **Transitivity**: No

**Semantic Rules**:
1. Services provide operational support to processes and products
2. Service availability directly impacts supported elements
3. Service criticality should match or exceed supported element criticality
4. Services can support both processes and products simultaneously

**Usage Scenarios**:

#### Scenario 1: Service Supporting Multiple Processes
```turtle
:AuthenticationService
  a :BusinessService ;
  :name "User Authentication Service" ;
  :criticality "critical" ;
  :availability_target "99.99%" ;
  :supports :UserLogin, :PasswordReset, :MultiFactorAuth .

:UserLogin
  a :BusinessProcess ;
  :name "User Login" ;
  :criticality "critical" ;
  :supported_by :AuthenticationService .
```

#### Scenario 2: Process Supported by Multiple Services
```turtle
:OrderProcessing
  a :BusinessProcess ;
  :name "Order Processing" ;
  :criticality "critical" ;
  :supported_by :PaymentService, :InventoryService, :ShippingService .

:PaymentService
  a :BusinessService ;
  :name "Payment Processing Service" ;
  :supports :OrderProcessing .

:InventoryService
  a :BusinessService ;
  :name "Inventory Management Service" ;
  :supports :OrderProcessing .
```

#### Scenario 3: Service Supporting Product
```turtle
:CloudStorageProduct
  a :Product ;
  :name "Cloud Storage Subscription" ;
  :criticality "high" ;
  :supported_by :StorageService, :BackupService, :SyncService .

:StorageService
  a :BusinessService ;
  :name "Object Storage Service" ;
  :availability_target "99.9%" ;
  :supports :CloudStorageProduct .
```

**Validation Rules**:
```sparql
# Find criticality mismatches (service less critical than what it supports)
SELECT ?service ?serviceCrit ?supported ?supportedCrit
WHERE {
  ?service :supports ?supported .
  ?service :criticality ?serviceCrit .
  ?supported :criticality ?supportedCrit .
  FILTER(
    (?serviceCrit = "low" && ?supportedCrit IN ("critical", "high", "medium")) ||
    (?serviceCrit = "medium" && ?supportedCrit IN ("critical", "high"))
  )
}

# Find services supporting retired elements
SELECT ?service ?supported ?status
WHERE {
  ?service :supports ?supported .
  ?supported :lifecycle_status "retired" .
  ?service :lifecycle_status ?status .
  FILTER(?status != "retired")
}
```

**Query Patterns**:

```sparql
# Find all services supporting a process
SELECT ?service ?availability ?criticality
WHERE {
  ?service :supports :OrderProcessing .
  ?service :availability_target ?availability .
  ?service :criticality ?criticality .
}

# Find impact of service outage
SELECT ?affected ?type ?criticality
WHERE {
  :PaymentService :supports ?affected .
  ?affected a ?type .
  ?affected :criticality ?criticality .
}
ORDER BY ?criticality

# Find services with high support load
SELECT ?service (COUNT(?supported) AS ?supportCount)
WHERE {
  ?service a :BusinessService .
  ?service :supports ?supported .
}
GROUP BY ?service
HAVING (COUNT(?supported) > 10)
ORDER BY DESC(?supportCount)
```

---

### 4. delivers

**Full Specification**:
- **Domain**: BusinessProcess
- **Range**: Product
- **Cardinality**: Many-to-Many
- **Inverse**: `delivered_by`
- **Transitivity**: No

**Semantic Rules**:
1. Processes operationalize product delivery to customers
2. Multiple processes may contribute to one product
3. One process may support multiple products
4. Process frequency should align with product delivery requirements

**Usage Scenarios**:

#### Scenario 1: Multiple Processes Deliver One Product
```turtle
:InsurancePolicy
  a :Product ;
  :name "Auto Insurance Policy" ;
  :criticality "critical" ;
  :delivered_by :PolicyUnderwriting, :PolicyIssuance, :ClaimsProcessing .

:PolicyUnderwriting
  a :BusinessProcess ;
  :name "Policy Underwriting" ;
  :delivers :InsurancePolicy .

:PolicyIssuance
  a :BusinessProcess ;
  :name "Policy Issuance" ;
  :delivers :InsurancePolicy .

:ClaimsProcessing
  a :BusinessProcess ;
  :name "Claims Processing" ;
  :delivers :InsurancePolicy .
```

#### Scenario 2: One Process Delivers Multiple Products
```turtle
:PaymentProcessing
  a :BusinessProcess ;
  :name "Payment Processing" ;
  :frequency "real-time" ;
  :delivers :CreditCardProduct, :DebitCardProduct, :DigitalWalletProduct .

:CreditCardProduct
  a :Product ;
  :name "Credit Card Service" ;
  :delivered_by :PaymentProcessing .
```

**Validation Rules**:
```sparql
# Find products without delivery processes
SELECT ?product
WHERE {
  ?product a :Product .
  ?product :lifecycle_status "active" .
  FILTER NOT EXISTS { ?product :delivered_by ?process }
}

# Find frequency mismatches
SELECT ?process ?frequency ?product ?productType
WHERE {
  ?process :delivers ?product .
  ?process :frequency ?frequency .
  ?product :product_type "digital" .
  FILTER(?frequency NOT IN ("real-time", "hourly", "on-demand"))
}
```

**Query Patterns**:

```sparql
# Find all processes delivering a product
SELECT ?process ?frequency ?criticality
WHERE {
  ?process :delivers :MobileBankingApp .
  ?process :frequency ?frequency .
  ?process :criticality ?criticality .
}

# Find products affected by process issues
SELECT ?product ?productCriticality
WHERE {
  :OrderFulfillment :delivers ?product .
  ?product :criticality ?productCriticality .
}

# Find process bottlenecks (processes delivering many products)
SELECT ?process (COUNT(?product) AS ?productCount)
WHERE {
  ?process :delivers ?product .
  ?product :lifecycle_status "active" .
}
GROUP BY ?process
HAVING (COUNT(?product) > 5)
ORDER BY DESC(?productCount)
```

---

## Cross-Layer Relationships (Business to Application)

### 5. realized_by

**Full Specification**:
- **Domain**: BusinessProcess OR BusinessCapability OR BusinessService
- **Range**: Application (Layer 2)
- **Cardinality**: Many-to-Many
- **Inverse**: `realizes`
- **Transitivity**: No

**Semantic Rules**:
1. Primary bridge from business requirements to IT implementation
2. Business elements can be realized by multiple applications (redundancy)
3. Applications can realize multiple business elements (shared services)
4. Application lifecycle must support business element lifecycle

**Usage Scenarios**:

#### Scenario 1: Process Realized by Multiple Applications
```turtle
:OrderFulfillment
  a :BusinessProcess ;
  :name "Order Fulfillment" ;
  :criticality "critical" ;
  :realized_by :OrderManagementSystem, :WarehouseManagementSystem, :ShippingSystem .

# Applications defined in Layer 2
:OrderManagementSystem
  a :Application ;
  :name "Order Management System" ;
  :realizes :OrderFulfillment .
```

#### Scenario 2: Capability Realized by Application Suite
```turtle
:CustomerAnalytics
  a :BusinessCapability ;
  :name "Customer Analytics" ;
  :criticality "high" ;
  :realized_by :DataWarehouse, :AnalyticsPlatform, :ReportingTool .

:DataWarehouse
  a :Application ;
  :realizes :CustomerAnalytics .
```

#### Scenario 3: Service Realized by Application
```turtle
:PaymentProcessingService
  a :BusinessService ;
  :name "Payment Processing Service" ;
  :criticality "critical" ;
  :availability_target "99.99%" ;
  :realized_by :PaymentGateway .

:PaymentGateway
  a :Application ;
  :application_type "SOA_service" ;
  :realizes :PaymentProcessingService .
```

**Validation Rules**:
```sparql
# Find critical business elements without redundant applications
SELECT ?businessElement ?appCount
WHERE {
  ?businessElement :criticality "critical" .
  {
    SELECT ?businessElement (COUNT(?app) AS ?appCount)
    WHERE {
      ?businessElement :realized_by ?app .
    }
    GROUP BY ?businessElement
  }
  FILTER(?appCount < 2)
}

# Find lifecycle mismatches
SELECT ?businessElement ?bizStatus ?app ?appStatus
WHERE {
  ?businessElement :realized_by ?app .
  ?businessElement :lifecycle_status ?bizStatus .
  ?app :lifecycle_status ?appStatus .
  FILTER(?bizStatus = "active" && ?appStatus IN ("deprecated", "retired"))
}
```

**Query Patterns**:

```sparql
# Find all applications realizing a business process
SELECT ?app ?appType ?status
WHERE {
  :OrderProcessing :realized_by ?app .
  ?app :application_type ?appType .
  ?app :lifecycle_status ?status .
}

# Find business impact of application failure
SELECT ?businessElement ?type ?criticality
WHERE {
  ?businessElement :realized_by :CRMSystem .
  ?businessElement a ?type .
  ?businessElement :criticality ?criticality .
}
ORDER BY ?criticality

# Find application utilization
SELECT ?app (COUNT(DISTINCT ?businessElement) AS ?businessCount)
WHERE {
  ?businessElement :realized_by ?app .
}
GROUP BY ?app
ORDER BY DESC(?businessCount)

# Full decomposition: Business to Application
SELECT ?process ?capability ?service ?app
WHERE {
  ?process a :BusinessProcess .
  ?process :enabled_by ?capability .
  ?process :supported_by ?service .
  ?process :realized_by ?app .
}
```

---

### 6. requires

**Full Specification**:
- **Domain**: Product
- **Range**: Application (Layer 2)
- **Cardinality**: Many-to-Many
- **Inverse**: `required_by`
- **Transitivity**: No

**Semantic Rules**:
1. Products have direct dependencies on applications
2. All required applications must be operational for product availability
3. Product criticality should be reflected in required application criticality
4. Enables product portfolio management and impact analysis

**Usage Scenarios**:

#### Scenario 1: Product Requiring Multiple Applications
```turtle
:MobileBankingApp
  a :Product ;
  :name "Mobile Banking Application" ;
  :criticality "critical" ;
  :product_type "digital" ;
  :requires :CoreBankingSystem, :AuthenticationService, :NotificationService .

:CoreBankingSystem
  a :Application ;
  :name "Core Banking System" ;
  :criticality "critical" ;
  :required_by :MobileBankingApp .
```

#### Scenario 2: Shared Application Required by Multiple Products
```turtle
:CustomerDatabase
  a :Application ;
  :name "Customer Database" ;
  :criticality "critical" ;
  :required_by :MobileBankingApp, :WebBankingPortal, :CallCenterApp .

:MobileBankingApp
  a :Product ;
  :requires :CustomerDatabase .

:WebBankingPortal
  a :Product ;
  :requires :CustomerDatabase .
```

**Validation Rules**:
```sparql
# Find products without required applications
SELECT ?product
WHERE {
  ?product a :Product .
  ?product :lifecycle_status "active" .
  FILTER NOT EXISTS { ?product :requires ?app }
}

# Find criticality mismatches
SELECT ?product ?productCrit ?app ?appCrit
WHERE {
  ?product :requires ?app .
  ?product :criticality ?productCrit .
  ?app :criticality ?appCrit .
  FILTER(?productCrit = "critical" && ?appCrit != "critical")
}
```

**Query Patterns**:

```sparql
# Find all applications required by a product
SELECT ?app ?appType ?criticality ?status
WHERE {
  :MobileBankingApp :requires ?app .
  ?app :application_type ?appType .
  ?app :criticality ?criticality .
  ?app :lifecycle_status ?status .
}

# Find products affected by application outage
SELECT ?product ?productType ?criticality
WHERE {
  ?product :requires :CoreBankingSystem .
  ?product :product_type ?productType .
  ?product :criticality ?criticality .
}
ORDER BY ?criticality

# Find high-impact applications (required by many products)
SELECT ?app (COUNT(?product) AS ?productCount)
WHERE {
  ?product :requires ?app .
  ?product :lifecycle_status "active" .
}
GROUP BY ?app
HAVING (COUNT(?product) > 3)
ORDER BY DESC(?productCount)
```

---

## Relationship Properties and Metadata

All relationships can be annotated with additional properties:

```turtle
:OrderProcessing :realized_by :OrderManagementSystem .

# Add relationship metadata using reification or named graphs
:OrderProcessing_realizes_OrderManagementSystem
  a rdf:Statement ;
  rdf:subject :OrderProcessing ;
  rdf:predicate :realized_by ;
  rdf:object :OrderManagementSystem ;
  :relationship_criticality "critical" ;
  :effective_date "2020-01-15"^^xsd:date ;
  :dependency_type "synchronous" ;
  :notes "Primary system for order processing workflow" .
```

---

## Complex Query Patterns

### Pattern 1: End-to-End Traceability

```sparql
# Trace from Product to Applications
SELECT ?product ?process ?service ?capability ?app
WHERE {
  ?product a :Product .
  ?product :delivered_by ?process .
  ?process :supported_by ?service .
  ?process :enabled_by ?capability .
  ?process :realized_by ?app .
}
```

### Pattern 2: Impact Analysis for Application Change

```sparql
# Find all business elements affected by application change
SELECT DISTINCT ?businessElement ?type ?criticality
WHERE {
  {
    ?businessElement :realized_by :CRMSystem .
  } UNION {
    ?product :requires :CRMSystem .
    BIND(?product AS ?businessElement)
  }
  ?businessElement a ?type .
  ?businessElement :criticality ?criticality .
}
ORDER BY ?criticality
```

### Pattern 3: Capability Gap Analysis

```sparql
# Find capabilities without supporting applications
SELECT ?capability ?maturity ?processCount
WHERE {
  ?capability a :BusinessCapability .
  ?capability :maturity_level ?maturity .
  {
    SELECT ?capability (COUNT(?process) AS ?processCount)
    WHERE {
      ?capability :enables ?process .
    }
    GROUP BY ?capability
  }
  FILTER NOT EXISTS { ?capability :realized_by ?app }
}
```

### Pattern 4: Service Dependency Chain

```sparql
# Find complete dependency chain for a product
SELECT ?product ?service ?process ?capability ?app
WHERE {
  BIND(:MobileBankingApp AS ?product)
  ?product :delivered_by ?process .
  ?process :supported_by ?service .
  ?process :enabled_by ?capability .
  {
    ?process :realized_by ?app .
  } UNION {
    ?service :realized_by ?app .
  } UNION {
    ?capability :realized_by ?app .
  } UNION {
    ?product :requires ?app .
  }
}
```

---

## Cypher Query Examples (Neo4j)

### Query 1: Find Business Hierarchy

```cypher
MATCH path = (child)-[:PART_OF*]->(parent:BusinessCapability)
WHERE child.name = 'Order Entry'
RETURN path
```

### Query 2: Impact Analysis

```cypher
MATCH (app:Application {name: 'CRM System'})<-[:REALIZED_BY|REQUIRES]-(business)
RETURN business.name AS affected_element,
       labels(business)[0] AS type,
       business.criticality AS criticality
ORDER BY business.criticality
```

### Query 3: Service Dependencies

```cypher
MATCH (product:Product)-[:DELIVERED_BY]->(process:BusinessProcess)
      -[:SUPPORTED_BY]->(service:BusinessService)
      -[:REALIZED_BY]->(app:Application)
WHERE product.name = 'Mobile Banking App'
RETURN product.name, process.name, service.name, app.name
```

### Query 4: Capability Maturity vs. Application Support

```cypher
MATCH (cap:BusinessCapability)-[:REALIZED_BY]->(app:Application)
RETURN cap.name AS capability,
       cap.maturity_level AS maturity,
       COUNT(app) AS app_count,
       COLLECT(app.name) AS applications
ORDER BY cap.maturity_level, app_count
```

---

## Requirements Traceability

This relationship guide addresses:

- **Requirement 2.1**: Defines relationship types for dependencies
- **Requirement 2.2**: Supports directional relationships with inverses
- **Requirement 2.4**: Specifies cardinality constraints
- **Requirement 10.2**: Defines business-to-application relationships
- **Requirement 10.3**: Supports many-to-many relationships

---

## Best Practices

1. **Relationship Naming**: Use consistent, semantic relationship names
2. **Cardinality Enforcement**: Validate cardinality constraints in SHACL
3. **Lifecycle Alignment**: Ensure related entities have compatible lifecycle states
4. **Criticality Propagation**: Higher-level elements should not depend on lower-criticality components
5. **Documentation**: Annotate relationships with effective dates and notes
6. **Versioning**: Track relationship changes over time
7. **Validation**: Regularly validate relationships against business rules
8. **Query Optimization**: Index frequently queried relationship paths

---

## Summary

Layer 1 relationships provide the foundation for:
- Business capability modeling and decomposition
- Process-to-application traceability
- Product portfolio management
- Impact analysis for changes
- Root cause analysis for incidents
- Service dependency mapping

These relationships enable comprehensive understanding of how business requirements are fulfilled through IT infrastructure.
