# ITIL and ArchiMate Framework Analysis

## Overview

This document provides a comprehensive analysis of ITIL (Information Technology Infrastructure Library) and ArchiMate frameworks, extracting entity types, attributes, and relationships that complement TOGAF and CIM for the IT Infrastructure and Application Dependency Ontology.

**ITIL Version**: ITIL 4 (2019)
**ArchiMate Version**: 3.1
**Framework Sources**: AXELOS (ITIL), The Open Group (ArchiMate)
**Analysis Date**: 2025-11-09

---

## Part 1: ITIL Framework Analysis

### ITIL Overview

ITIL focuses on IT Service Management (ITSM) and provides best practices for managing IT services throughout their lifecycle. While ITIL is process-oriented rather than entity-oriented, it defines key concepts and attributes relevant to infrastructure and application management.

---

### ITIL Service Management Concepts

#### 1. Configuration Item (CI)

**ITIL Definition**: Any component that needs to be managed in order to deliver an IT service.

**Attributes**:
- `ci_name` (string, mandatory): Configuration item name
- `ci_type` (string, mandatory): Type of CI (hardware, software, service, etc.)
- `ci_status` (enum: planned, ordered, in_development, in_test, live, withdrawn, mandatory): CI lifecycle status
- `owner` (string, mandatory): CI owner
- `support_group` (string, optional): Responsible support team
- `criticality` (enum: critical, high, medium, low, mandatory): Business criticality
- `environment` (enum: development, test, staging, production, mandatory): Deployment environment
- `version` (string, optional): Version identifier
- `serial_number` (string, optional): Serial number for hardware CIs
- `asset_tag` (string, optional): Asset tracking identifier
- `warranty_expiry` (date, optional): Warranty expiration date
- `maintenance_window` (string, optional): Scheduled maintenance window

**Ontology Mapping**:
- Maps to all entity types across all layers
- Provides lifecycle and ownership attributes
- Complements TOGAF and CIM with operational attributes

---

#### 2. Service

**ITIL Definition**: A means of enabling value co-creation by facilitating outcomes that customers want to achieve, without the customer having to manage specific costs and risks.

**Attributes**:
- `service_name` (string, mandatory): Service name
- `service_type` (enum: business_service, technical_service, supporting_service, mandatory): Service classification
- `service_level` (string, optional): Service level agreement reference
- `availability_target` (string, optional): Target availability (e.g., "99.9%")
- `service_owner` (string, mandatory): Service owner
- `service_status` (enum: design, transition, operation, retired, mandatory): Service lifecycle status
- `cost_center` (string, optional): Financial cost center
- `customer` (string, optional): Primary customer or consumer

**Ontology Mapping**:
- Layer 1 (Business Processes): BusinessService
- Layer 2 (Application Layer): Service, API
- Provides service management attributes

---

#### 3. Incident

**ITIL Definition**: An unplanned interruption to a service or reduction in the quality of a service.

**Attributes**:
- `incident_id` (string, mandatory): Unique incident identifier
- `priority` (enum: critical, high, medium, low, mandatory): Incident priority
- `impact` (enum: extensive, significant, moderate, minor, mandatory): Business impact
- `urgency` (enum: critical, high, medium, low, mandatory): Time sensitivity
- `affected_ci` (string, mandatory): Configuration item affected
- `resolution_time` (duration, optional): Time to resolve

**Ontology Mapping**:
- Not directly mapped to ontology entities
- Provides operational state attributes for entities
- Informs `lifecycle_status` and health attributes

---

#### 4. Change

**ITIL Definition**: The addition, modification, or removal of anything that could have a direct or indirect effect on services.

**Attributes**:
- `change_id` (string, mandatory): Unique change identifier
- `change_type` (enum: standard, normal, emergency, mandatory): Change classification
- `change_status` (enum: requested, approved, scheduled, implementing, completed, failed, mandatory): Change state
- `risk_level` (enum: high, medium, low, mandatory): Risk assessment
- `affected_cis` (list, mandatory): List of affected configuration items
- `implementation_date` (datetime, optional): Scheduled implementation

**Ontology Mapping**:
- Not directly mapped to ontology entities
- Informs impact analysis use cases
- Provides temporal relationship context

---

#### 5. Application Management

**ITIL Definition**: The practice of managing applications throughout their lifecycle.

**Attributes**:
- `application_name` (string, mandatory): Application name
- `application_owner` (string, mandatory): Application owner
- `vendor` (string, optional): Software vendor
- `license_type` (enum: perpetual, subscription, open_source, mandatory): Licensing model
- `license_count` (integer, optional): Number of licenses
- `support_contract` (string, optional): Support contract reference
- `end_of_life_date` (date, optional): End of life date
- `end_of_support_date` (date, optional): End of support date

**Ontology Mapping**:
- Layer 2 (Application Layer): Application
- Provides lifecycle and commercial attributes

---

#### 6. Technical Management

**ITIL Definition**: The practice of managing technical resources and expertise.

**Attributes**:
- `technical_domain` (enum: compute, storage, network, database, middleware, mandatory): Technical area
- `technical_owner` (string, mandatory): Technical owner or team
- `skill_level_required` (enum: expert, advanced, intermediate, basic, mandatory): Required expertise
- `documentation_url` (string, optional): Technical documentation reference
- `runbook_url` (string, optional): Operational runbook reference

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): All infrastructure entities
- Layer 5 (Network): Network entities
- Provides operational management attributes

---

### ITIL Attributes Summary for Ontology

**Complementary Attributes Not in TOGAF/CIM**:

1. **Operational Management**:
   - `support_group` (string): Responsible support team
   - `maintenance_window` (string): Scheduled maintenance window
   - `runbook_url` (string): Operational procedures reference

2. **Lifecycle and Status**:
   - `ci_status` (enum): ITIL-specific lifecycle states
   - `environment` (enum): Deployment environment (dev, test, prod)
   - `end_of_life_date` (date): Planned retirement date
   - `end_of_support_date` (date): Support termination date

3. **Service Management**:
   - `service_level` (string): SLA reference
   - `availability_target` (string): Target availability percentage
   - `cost_center` (string): Financial tracking

4. **Risk and Impact**:
   - `criticality` (enum): Business criticality level
   - `impact` (enum): Business impact classification
   - `risk_level` (enum): Risk assessment

5. **Commercial and Licensing**:
   - `vendor` (string): Software or hardware vendor
   - `license_type` (enum): Licensing model
   - `license_count` (integer): Number of licenses
   - `support_contract` (string): Support agreement reference
   - `warranty_expiry` (date): Warranty expiration

6. **Asset Management**:
   - `asset_tag` (string): Physical asset identifier
   - `serial_number` (string): Hardware serial number

---

## Part 2: ArchiMate Framework Analysis

### ArchiMate Overview

ArchiMate is an open and independent enterprise architecture modeling language that provides a uniform representation for diagrams describing enterprise architectures. It has three main layers: Business, Application, and Technology.

---

### ArchiMate Business Layer

#### 1. Business Actor

**ArchiMate Definition**: A business entity that is capable of performing behavior.

**Attributes**:
- `name` (string, mandatory): Actor name
- `description` (string, optional): Actor description
- `type` (enum: person, organization, role, mandatory): Actor type

**Ontology Mapping**:
- Layer 1 (Business Processes): Provides context for BusinessProcess ownership
- Not a primary entity type but informs `owner` attributes

---

#### 2. Business Process

**ArchiMate Definition**: A sequence of business behaviors that achieves a specific result.

**Attributes**:
- `name` (string, mandatory): Process name
- `description` (string, optional): Process description
- `process_type` (enum: core, support, management, mandatory): Process classification

**Ontology Mapping**:
- Layer 1 (Business Processes): BusinessProcess
- Aligns with TOGAF Business Architecture

---

#### 3. Business Service

**ArchiMate Definition**: A service that fulfills a business need for a customer.

**Attributes**:
- `name` (string, mandatory): Service name
- `description` (string, optional): Service description
- `service_level` (string, optional): Service level specification

**Ontology Mapping**:
- Layer 1 (Business Processes): BusinessService
- Aligns with TOGAF and ITIL service concepts

---

#### 4. Business Object

**ArchiMate Definition**: A passive element that has relevance from a business perspective.

**Attributes**:
- `name` (string, mandatory): Object name
- `description` (string, optional): Object description
- `object_type` (enum: product, contract, document, mandatory): Object classification

**Ontology Mapping**:
- Layer 1 (Business Processes): Product
- Represents business artifacts

---

### ArchiMate Application Layer

#### 1. Application Component

**ArchiMate Definition**: A modular, deployable, and replaceable part of a software system that encapsulates its behavior and data.

**Attributes**:
- `name` (string, mandatory): Component name
- `description` (string, optional): Component description
- `component_type` (enum: presentation, business_logic, data_access, integration, mandatory): Component classification
- `technology` (string, optional): Implementation technology

**Ontology Mapping**:
- Layer 2 (Application Layer): Application, ApplicationComponent
- Aligns with TOGAF Application Component

---

#### 2. Application Service

**ArchiMate Definition**: A service that exposes automated behavior.

**Attributes**:
- `name` (string, mandatory): Service name
- `description` (string, optional): Service description
- `interface_type` (enum: rest, soap, graphql, grpc, messaging, mandatory): Interface protocol

**Ontology Mapping**:
- Layer 2 (Application Layer): Service, API
- Provides interface specification attributes

---

#### 3. Application Interface

**ArchiMate Definition**: A point of access where application services are made available to a user, another application component, or a node.

**Attributes**:
- `name` (string, mandatory): Interface name
- `protocol` (string, mandatory): Communication protocol
- `endpoint_url` (string, optional): Service endpoint
- `authentication_method` (enum: none, basic, oauth, certificate, mandatory): Authentication type

**Ontology Mapping**:
- Layer 2 (Application Layer): API
- Provides detailed interface attributes

---

#### 4. Data Object

**ArchiMate Definition**: Data structured for automated processing.

**Attributes**:
- `name` (string, mandatory): Data object name
- `description` (string, optional): Data object description
- `data_type` (enum: structured, unstructured, semi_structured, mandatory): Data structure type
- `schema_version` (string, optional): Schema version

**Ontology Mapping**:
- Layer 2 (Application Layer): DataObject, DatabaseInstance
- Represents logical data structures

---

### ArchiMate Technology Layer

#### 1. Node

**ArchiMate Definition**: A computational or physical resource that hosts, manipulates, or interacts with other computational or physical resources.

**Attributes**:
- `name` (string, mandatory): Node name
- `description` (string, optional): Node description
- `node_type` (enum: device, system_software, execution_environment, mandatory): Node classification

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): PhysicalServer, VirtualMachine, CloudInstance
- Aligns with CIM ComputerSystem

---

#### 2. Device

**ArchiMate Definition**: A physical IT resource upon which system software and artifacts may be stored or deployed for execution.

**Attributes**:
- `name` (string, mandatory): Device name
- `device_type` (enum: server, storage, network, mobile, iot, mandatory): Device classification
- `location` (string, mandatory): Physical location

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): PhysicalServer, StorageArray
- Layer 5 (Network): NetworkDevice
- Aligns with CIM physical resource concepts

---

#### 3. System Software

**ArchiMate Definition**: Software that provides or contributes to an environment for storing, executing, and using software or data deployed within it.

**Attributes**:
- `name` (string, mandatory): Software name
- `software_type` (enum: operating_system, database_system, middleware, virtualization, mandatory): Software classification
- `version` (string, mandatory): Software version

**Ontology Mapping**:
- Layer 2 (Application Layer): ApplicationServer, Database
- Layer 4 (Physical Infrastructure): Hypervisor
- Provides system software attributes

---

#### 4. Technology Service

**ArchiMate Definition**: A service that exposes the functionality of a node to its environment.

**Attributes**:
- `name` (string, mandatory): Service name
- `service_type` (enum: compute, storage, network, security, mandatory): Service classification
- `protocol` (string, optional): Service protocol

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): CloudService
- Layer 5 (Network): Network services
- Represents infrastructure services

---

#### 5. Communication Network

**ArchiMate Definition**: A physical communication medium between two or more devices or nodes.

**Attributes**:
- `name` (string, mandatory): Network name
- `network_type` (enum: lan, wan, internet, vpn, mandatory): Network classification
- `bandwidth` (string, optional): Network capacity
- `protocol` (string, optional): Network protocol

**Ontology Mapping**:
- Layer 5 (Network): NetworkSegment, CommunicationPath
- Aligns with CIM Network Model

---

#### 6. Path

**ArchiMate Definition**: A link between two or more nodes through which these nodes can exchange data, energy, or material.

**Attributes**:
- `name` (string, mandatory): Path name
- `path_type` (enum: network, data, control, mandatory): Path classification
- `latency` (string, optional): Network latency
- `throughput` (string, optional): Data throughput

**Ontology Mapping**:
- Layer 5 (Network): CommunicationPath, NetworkRoute
- Provides network path attributes

---

### ArchiMate Relationships

ArchiMate defines several relationship types that map to ontology relationships:

#### 1. Serving Relationship

**ArchiMate Definition**: Represents that an element provides its functionality to another element.

**Ontology Mapping**:
- `fulfills`: Business Process → Application
- `supports`: Application → Business Process
- `provides`: Service → Consumer

---

#### 2. Realization Relationship

**ArchiMate Definition**: Represents that an entity plays a critical role in the creation, achievement, sustenance, or operation of a more abstract entity.

**Ontology Mapping**:
- `deployed_as`: Application → Container
- `runs_on`: Container → Infrastructure
- `hosted_on`: Database → Storage

---

#### 3. Assignment Relationship

**ArchiMate Definition**: Represents the allocation of responsibility, performance of behavior, storage, or execution.

**Ontology Mapping**:
- `deployed_on`: ApplicationComponent → ApplicationServer
- `allocated_from`: Volume → StorageArray

---

#### 4. Access Relationship

**ArchiMate Definition**: Represents the ability of behavior and active structure elements to observe or act upon passive structure elements.

**Ontology Mapping**:
- `uses`: Application → Database
- `reads_from`: Application → Storage
- `writes_to`: Application → Storage

---

#### 5. Flow Relationship

**ArchiMate Definition**: Represents transfer from one element to another.

**Ontology Mapping**:
- `communicates_via`: Application → Network Path
- `routes_through`: Path → NetworkDevice

---

#### 6. Association Relationship

**ArchiMate Definition**: Represents an unspecified relationship or one that is not represented by another ArchiMate relationship.

**Ontology Mapping**:
- `connected_to`: NetworkDevice → NetworkDevice
- `part_of`: Component → Parent

---

### ArchiMate Attributes Summary for Ontology

**Complementary Attributes Not in TOGAF/CIM/ITIL**:

1. **Component Classification**:
   - `component_type` (enum): Presentation, business logic, data access, integration
   - `process_type` (enum): Core, support, management
   - `node_type` (enum): Device, system software, execution environment

2. **Interface Specifications**:
   - `interface_type` (enum): REST, SOAP, GraphQL, gRPC, messaging
   - `endpoint_url` (string): Service endpoint URL
   - `authentication_method` (enum): Authentication mechanism
   - `protocol` (string): Communication protocol

3. **Network Characteristics**:
   - `network_type` (enum): LAN, WAN, Internet, VPN
   - `latency` (string): Network latency measurement
   - `throughput` (string): Data throughput capacity
   - `path_type` (enum): Network, data, control

4. **Data Characteristics**:
   - `data_type` (enum): Structured, unstructured, semi-structured
   - `schema_version` (string): Data schema version

5. **Technology Specifications**:
   - `software_type` (enum): OS, database system, middleware, virtualization
   - `device_type` (enum): Server, storage, network, mobile, IoT

---

## Part 3: Consolidated Framework Mapping

### Layer 1: Business Processes

| Entity Type | TOGAF | ITIL | ArchiMate | Complementary Attributes |
|-------------|-------|------|-----------|--------------------------|
| BusinessProcess | Business Process | - | Business Process | `process_type` (ArchiMate) |
| BusinessCapability | Business Capability | - | - | - |
| BusinessService | Business Service | Service | Business Service | `service_level`, `availability_target` (ITIL) |
| Product | - | - | Business Object | `object_type` (ArchiMate) |

**Key Attributes from Frameworks**:
- TOGAF: `name`, `description`, `owner`, `criticality`, `lifecycle_status`
- ITIL: `service_level`, `availability_target`, `cost_center`, `customer`
- ArchiMate: `process_type`, `service_level`

---

### Layer 2: Application Layer

| Entity Type | TOGAF | ITIL | ArchiMate | Complementary Attributes |
|-------------|-------|------|-----------|--------------------------|
| Application | Application Component | Application | Application Component | `component_type` (ArchiMate), `vendor`, `license_type` (ITIL) |
| ApplicationComponent | Application Component | - | Application Component | `component_type`, `technology` (ArchiMate) |
| ApplicationServer | - | Technical Management | System Software | `software_type` (ArchiMate), `support_group` (ITIL) |
| Service | Application Service | Service | Application Service | `interface_type`, `authentication_method` (ArchiMate) |
| API | - | - | Application Interface | `endpoint_url`, `protocol`, `authentication_method` (ArchiMate) |
| Database | Data Entity | Application | System Software | `software_type` (ArchiMate), `vendor`, `license_type` (ITIL) |
| DataObject | Data Entity | - | Data Object | `data_type`, `schema_version` (ArchiMate) |

**Key Attributes from Frameworks**:
- TOGAF: `name`, `version`, `application_type`, `technology_stack`
- ITIL: `vendor`, `license_type`, `license_count`, `support_contract`, `end_of_life_date`, `support_group`
- ArchiMate: `component_type`, `interface_type`, `endpoint_url`, `authentication_method`, `protocol`, `data_type`, `schema_version`

---

### Layer 3: Container and Orchestration

| Entity Type | TOGAF | ITIL | ArchiMate | Complementary Attributes |
|-------------|-------|------|-----------|--------------------------|
| Container | - | Configuration Item | Node | `node_type` (ArchiMate), `ci_status` (ITIL) |
| Pod | - | Configuration Item | Node | - |
| ContainerImage | - | Configuration Item | Artifact | - |
| Cluster | - | Configuration Item | Node | `technical_owner` (ITIL) |

**Key Attributes from Frameworks**:
- ITIL: `ci_status`, `owner`, `support_group`, `environment`
- ArchiMate: `node_type`

---

### Layer 4: Physical Infrastructure

| Entity Type | TOGAF | ITIL | ArchiMate | Complementary Attributes |
|-------------|-------|------|-----------|--------------------------|
| PhysicalServer | Technology Component | Configuration Item | Device | `device_type` (ArchiMate), `asset_tag`, `serial_number` (ITIL) |
| VirtualMachine | Platform Service | Configuration Item | Node | `node_type` (ArchiMate) |
| StorageArray | Technology Component | Configuration Item | Device | `device_type` (ArchiMate), `warranty_expiry` (ITIL) |
| StorageVolume | Technology Component | Configuration Item | - | `asset_tag` (ITIL) |
| Hypervisor | Platform Service | Technical Management | System Software | `software_type` (ArchiMate) |
| CloudInstance | Platform Service | Configuration Item | Node | `node_type` (ArchiMate) |

**Key Attributes from Frameworks**:
- TOGAF: `name`, `location`, `capacity`, `operating_system`
- ITIL: `asset_tag`, `serial_number`, `warranty_expiry`, `maintenance_window`, `support_group`
- ArchiMate: `device_type`, `node_type`, `location`

---

### Layer 5: Network Topology and Communication Path

| Entity Type | TOGAF | ITIL | ArchiMate | Complementary Attributes |
|-------------|-------|------|-----------|--------------------------|
| NetworkDevice | Technology Component | Configuration Item | Device | `device_type` (ArchiMate), `asset_tag` (ITIL) |
| LoadBalancer | Technology Component | Configuration Item | Device | - |
| NetworkSegment | Communication Infrastructure | - | Communication Network | `network_type`, `bandwidth` (ArchiMate) |
| CommunicationPath | Communication Infrastructure | - | Path | `latency`, `throughput`, `path_type` (ArchiMate) |
| NetworkRoute | - | - | Path | - |

**Key Attributes from Frameworks**:
- TOGAF: `name`, `device_type`, `ip_address`, `protocol`, `port`
- ITIL: `asset_tag`, `serial_number`, `support_group`, `maintenance_window`
- ArchiMate: `network_type`, `bandwidth`, `latency`, `throughput`, `path_type`

---

### Layer 6: Security Infrastructure

| Entity Type | TOGAF | ITIL | ArchiMate | Complementary Attributes |
|-------------|-------|------|-----------|--------------------------|
| Firewall | Security Service | Configuration Item | Device | `device_type` (ArchiMate) |
| WAF | Security Service | Configuration Item | - | - |
| Certificate | Security Service | Configuration Item | - | `expiration_date` (ITIL) |
| SecurityPolicy | Security Policy | - | - | `policy_rules` (ITIL) |
| IdentityProvider | Security Service | - | - | - |

**Key Attributes from Frameworks**:
- TOGAF: `name`, `security_type`, `trust_level`
- ITIL: `support_group`, `maintenance_window`, `warranty_expiry`
- ArchiMate: `device_type`

---

## Part 4: Attribute Recommendations

### Attributes to Add from ITIL

1. **Operational Management** (All Layers):
   - `support_group` (string, optional): Responsible support team
   - `maintenance_window` (string, optional): Scheduled maintenance window
   - `runbook_url` (string, optional): Operational procedures reference

2. **Lifecycle Management** (All Layers):
   - `environment` (enum: development, test, staging, production, optional): Deployment environment
   - `end_of_life_date` (date, optional): Planned retirement date
   - `end_of_support_date` (date, optional): Support termination date

3. **Commercial Attributes** (Layer 2, Layer 4):
   - `vendor` (string, optional): Software or hardware vendor
   - `license_type` (enum: perpetual, subscription, open_source, optional): Licensing model
   - `license_count` (integer, optional): Number of licenses
   - `support_contract` (string, optional): Support agreement reference

4. **Asset Management** (Layer 4, Layer 5):
   - `asset_tag` (string, optional): Physical asset identifier
   - `serial_number` (string, optional): Hardware serial number
   - `warranty_expiry` (date, optional): Warranty expiration date

5. **Service Management** (Layer 1, Layer 2):
   - `service_level` (string, optional): SLA reference
   - `availability_target` (string, optional): Target availability (e.g., "99.9%")
   - `cost_center` (string, optional): Financial cost center

### Attributes to Add from ArchiMate

1. **Component Classification** (Layer 2):
   - `component_type` (enum: presentation, business_logic, data_access, integration, optional): Component classification

2. **Interface Specifications** (Layer 2):
   - `interface_type` (enum: rest, soap, graphql, grpc, messaging, optional): Interface protocol
   - `endpoint_url` (string, optional): Service endpoint URL
   - `authentication_method` (enum: none, basic, oauth, certificate, optional): Authentication mechanism

3. **Network Characteristics** (Layer 5):
   - `network_type` (enum: lan, wan, internet, vpn, optional): Network classification
   - `latency` (string, optional): Network latency measurement
   - `throughput` (string, optional): Data throughput capacity
   - `path_type` (enum: network, data, control, optional): Path classification

4. **Data Characteristics** (Layer 2):
   - `data_type` (enum: structured, unstructured, semi_structured, optional): Data structure type
   - `schema_version` (string, optional): Data schema version

5. **Technology Specifications** (Layer 2, Layer 4):
   - `software_type` (enum: operating_system, database_system, middleware, virtualization, optional): Software classification
   - `device_type` (enum: server, storage, network, mobile, iot, optional): Device classification

---

## Part 5: Relationship Recommendations

### Relationships from ArchiMate

1. **Serving Relationships**:
   - `provides`: Service → Consumer (Layer 2)
   - `serves`: Infrastructure → Application (Layer 4 → Layer 2)

2. **Realization Relationships**:
   - `realizes`: Application → BusinessService (Layer 2 → Layer 1)
   - `implements`: ApplicationComponent → Service (Layer 2)

3. **Assignment Relationships**:
   - `assigned_to`: Behavior → Node (Layer 2 → Layer 4)
   - `allocated_to`: Resource → Consumer (Layer 4)

4. **Access Relationships**:
   - `accesses`: Application → DataObject (Layer 2)
   - `reads`: Application → Storage (Layer 2 → Layer 4)
   - `writes`: Application → Storage (Layer 2 → Layer 4)

5. **Flow Relationships**:
   - `flows_to`: Data → Destination (Layer 2)
   - `triggers`: Event → Process (Layer 1)

---

## Conclusion

This analysis of ITIL and ArchiMate frameworks has identified complementary attributes and relationships that enhance the IT Infrastructure and Application Dependency Ontology beyond what TOGAF and CIM provide:

**ITIL Contributions**:
- Operational management attributes (support groups, maintenance windows)
- Lifecycle management (end-of-life, end-of-support dates)
- Commercial attributes (vendor, licensing, support contracts)
- Asset management (asset tags, serial numbers, warranty)
- Service management (SLAs, availability targets, cost centers)

**ArchiMate Contributions**:
- Component classification (presentation, business logic, data access)
- Interface specifications (protocols, endpoints, authentication)
- Network characteristics (latency, throughput, network types)
- Data characteristics (data types, schema versions)
- Rich relationship semantics (serving, realization, assignment, access, flow)

These frameworks provide a more complete picture of IT infrastructure by adding operational, commercial, and detailed technical attributes that complement the structural and architectural focus of TOGAF and CIM.

---

**Analysis Complete**: 2025-11-09
**Next Steps**: Integrate these attributes into the ontology design document and update entity type specifications.