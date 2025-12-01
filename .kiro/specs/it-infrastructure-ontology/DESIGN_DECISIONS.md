# IT Infrastructure Ontology - Design Decisions and Improvements

## Document Information
- **Created**: 2024-12-01
- **Purpose**: Record key design decisions, improvements, and rationale for the ontology model
- **Status**: Living document - updated as model evolves

---

## Critical Design Decisions

### 1. ApplicationServer Placement (Layer 4 vs Layer 2)

**Decision**: ApplicationServer belongs to **Layer 4 (Physical Infrastructure)**, not Layer 2 (Application)

**Rationale**:
- ApplicationServer is infrastructure that **hosts** applications, similar to how a VM or container runtime hosts workloads
- It provides runtime environment and resources (CPU, memory, thread pools)
- Examples: WebSphere, WebLogic, Tomcat, IIS, JBoss
- Comparable to container orchestrators (Kubernetes) which are in Layer 3

**Relationships**:
```turtle
Application :hosted_on ApplicationServer
ApplicationComponent :deployed_on ApplicationServer
ApplicationServer :runs_on VirtualMachine|PhysicalServer|CloudInstance
```

**Impact**: Enables proper modeling of legacy application deployments and clear separation between application logic and runtime infrastructure.

---

### 2. CommunicationPath Endpoints (NetworkInterface vs NetworkDevice)

**Decision**: CommunicationPath connects to **NetworkInterface** endpoints, not NetworkDevice

**Original Problem**: 
- CommunicationPath only had `routes_through` relationship to NetworkDevice
- No way to identify actual source and destination endpoints
- Missing critical information for troubleshooting

**Solution - Added Three Relationships**:

1. **connects_from**: CommunicationPath → NetworkInterface (source endpoint)
   - Functional property (one source per path)
   - Identifies the exact interface where communication originates

2. **connects_to**: CommunicationPath → NetworkInterface (destination endpoint)
   - Functional property (one destination per path)
   - Identifies the exact interface where communication terminates

3. **routes_through**: CommunicationPath → NetworkDevice (intermediate hops)
   - Many-to-many relationship
   - Identifies routers, switches, firewalls, load balancers in the path

**Complete Model**:
```
Application → communicates_via → CommunicationPath
                                      ↓ connects_from
                                  NetworkInterface (source)
                                      ↓ attached_to
                                  VirtualMachine/Pod
                                      
CommunicationPath → routes_through → Router → Firewall → LoadBalancer → Switch
                                      
                                  NetworkInterface (destination)
                                      ↑ attached_to
                                  VirtualMachine/Pod
                                      ↑ connects_to
                                  CommunicationPath
```

**Impact**: 
- Enables precise root cause analysis
- Can trace exact network path from source to destination
- Supports latency analysis and performance troubleshooting

---

### 3. NetworkInterface to NetworkDevice Connection

**Decision**: Added **connected_to_port** relationship between NetworkInterface and NetworkDevice

**Original Problem**:
- No relationship between NetworkInterface and NetworkDevice
- Couldn't identify which switch port a VM/server interface is connected to
- Missing critical topology information for troubleshooting

**Solution**:
```turtle
:connected_to_port
  rdf:type owl:ObjectProperty ;
  rdf:type owl:FunctionalProperty ;
  rdfs:domain :NetworkInterface ;
  rdfs:range :NetworkDevice ;
  rdfs:comment "Network interface is connected to a port on a network device"
```

**Properties**:
- port_number: Port identifier (e.g., "GigabitEthernet0/1", "eth0")
- connection_type: physical, virtual, trunk, access
- port_speed_mbps: Port speed
- vlan_mode: access, trunk, hybrid

**Impact**:
- Can identify which switch port failed
- Enables port-level troubleshooting
- Supports network topology visualization
- Critical for impact analysis: "Which VMs are affected if this switch fails?"

---

### 4. NetworkInterface Attachment Scope

**Decision**: NetworkInterface can attach to **VirtualMachine, PhysicalServer, CloudInstance, Container, AND Pod**

**Rationale**:
- In Kubernetes, the **Pod** has the network namespace and IP address
- Containers within a Pod **share** the Pod's network interface
- NetworkInterface should attach to Pod, not individual containers

**Updated Range**:
```turtle
:attached_to
  rdfs:domain :NetworkInterface ;
  rdfs:range [ owl:unionOf ( :PhysicalServer :VirtualMachine :CloudInstance :Container :Pod ) ]
```

**Impact**: Properly models Kubernetes networking where Pod is the network boundary.

---

### 5. Importance of NetworkDevice for Troubleshooting

**Decision**: NetworkDevice is **ESSENTIAL** and cannot be removed

**Rationale - Critical for**:

1. **Root Cause Analysis**:
   - Identify which router/switch/firewall failed
   - Diagnose routing problems
   - Trace network path for latency issues

2. **Impact Analysis**:
   - "If this router fails, which applications are affected?"
   - "Which services depend on this firewall?"

3. **Security Analysis**:
   - Track which firewalls protect which services
   - Audit network segmentation
   - Identify security boundaries

4. **Performance Analysis**:
   - Identify bottleneck devices
   - Analyze hop-by-hop latency
   - Capacity planning

**What Would Be Lost Without NetworkDevice**:
- ❌ Cannot identify intermediate routing failures
- ❌ Cannot diagnose firewall/ACL issues
- ❌ Cannot trace network path for latency analysis
- ❌ Cannot identify which load balancer is failing
- ❌ Cannot map network topology for impact analysis

---

## Complete Network Layer Relationship Model

### Intra-Layer Relationships (Layer 5)

| Relationship | Domain | Range | Cardinality | Purpose |
|--------------|--------|-------|-------------|---------|
| **connected_to** | NetworkDevice | NetworkDevice | *..*  | Device-to-device physical/logical connections |
| **connects_from** | CommunicationPath | NetworkInterface | *..1 | Source endpoint of communication |
| **connects_to** | CommunicationPath | NetworkInterface | *..1 | Destination endpoint of communication |
| **routes_through** | CommunicationPath | NetworkDevice | *..* | Intermediate routing devices |
| **connected_to_port** | NetworkInterface | NetworkDevice | *..1 | Interface connected to device port |
| **part_of_segment** | NetworkInterface/Device | NetworkSegment | *..1 | Segment membership |
| **applies_to** | NetworkRoute | NetworkSegment | *..1 | Route applies to segment |

### Cross-Layer Relationships

| Relationship | Domain | Range | Cardinality | Purpose |
|--------------|--------|-------|-------------|---------|
| **attached_to** | NetworkInterface | Compute (VM/Pod/Server) | *..1 | Interface attached to compute resource |
| **balances_to** | LoadBalancer | Compute/Service | 1..* | Load balancer targets |
| **communicates_via** | Application/Service | CommunicationPath | *..* | Application uses communication path |
| **exposes_via** | Application/Service | LoadBalancer | *..* | Application exposed via load balancer |

---

## Key SPARQL Queries for Troubleshooting

### Query 1: Trace Network Path Between Services

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT 
  ?sourceService ?sourceIP ?sourceSwitch
  ?path ?protocol ?port
  ?router ?firewall ?loadBalancer
  ?destSwitch ?destIP ?destService
WHERE {
  # Source
  BIND(:ServiceA AS ?sourceService)
  ?sourceService :deployed_as|:hosted_on ?sourceVM .
  ?sourceVM :has_interface ?sourceInterface .
  ?sourceInterface :ip_address ?sourceIP .
  ?sourceInterface :connected_to_port ?sourceSwitch .
  
  # Path
  ?sourceService :communicates_via ?path .
  ?path :connects_from ?sourceInterface .
  ?path :protocol ?protocol .
  ?path :destination_port ?port .
  
  # Intermediate devices
  OPTIONAL { ?path :routes_through ?router . ?router :device_type "router" }
  OPTIONAL { ?path :routes_through ?firewall . ?firewall :device_type "firewall" }
  OPTIONAL { ?path :routes_through ?loadBalancer . ?loadBalancer rdf:type :LoadBalancer }
  
  # Destination
  ?path :connects_to ?destInterface .
  ?destInterface :ip_address ?destIP .
  ?destInterface :connected_to_port ?destSwitch .
  ?destInterface :attached_to ?destVM .
  ?destVM :hosts|:deploys ?destService .
  
  FILTER(?destService = :ServiceB)
}
```

### Query 2: Find Failed Components in Path

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?componentType ?componentName ?status
WHERE {
  :ServiceA :communicates_via ?path .
  ?path :used_by :ServiceB .
  
  {
    ?path :routes_through ?device .
    ?device :lifecycle_status ?status .
    FILTER(?status != "active")
    BIND("NetworkDevice" AS ?componentType)
    ?device :name ?componentName .
  } UNION {
    ?path :connects_from|:connects_to ?interface .
    ?interface :lifecycle_status ?status .
    FILTER(?status != "up")
    BIND("NetworkInterface" AS ?componentType)
    ?interface :name ?componentName .
  }
}
```

### Query 3: Impact Analysis - Which Services Affected by Device Failure

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT DISTINCT ?service ?serviceName
WHERE {
  # Find all communication paths routing through the failed device
  ?path :routes_through :Router_Core01 .
  
  # Find services using those paths
  ?service :communicates_via ?path .
  ?service :name ?serviceName .
}
```

---

## Visual Diagram Improvements

### Added Comprehensive Intra-Layer Relationships

**Layer 1 (Business)**:
- Capability hierarchies (contains)
- Process composition (contains, part_of)
- Enablement (enables, enabled_by)
- Support (supports, supported_by)
- Product delivery (delivers)

**Layer 2 (Application)**:
- Application → contains → ApplicationComponent
- Application → contains → Service
- Application → exposes → API
- Service → calls → Service
- Database → contains → DatabaseInstance
- Database → contains → DataObject
- Application → uses → Database, MessageQueue, CacheService, FileStorageService

**Layer 3 (Container)**:
- Cluster → contains → Namespace
- Namespace → contains → Deployment
- Deployment → manages → Pod
- Pod → contains → Container
- Container → uses_image → ContainerImage
- KubernetesService → exposes → Pod
- Route → routes_to → KubernetesService

**Layer 4 (Infrastructure)**:
- Hypervisor → runs_on → PhysicalServer
- VirtualMachine → runs_on → Hypervisor
- ApplicationServer → runs_on → VirtualMachine/PhysicalServer
- StorageArray → contains → StoragePool
- StoragePool → allocates → StorageVolume
- FileSystem → mounted_from → StorageVolume

**Layer 5 (Network)**:
- NetworkDevice → connected_to → NetworkDevice
- NetworkInterface → connected_to_port → NetworkDevice
- NetworkInterface → part_of_segment → NetworkSegment
- CommunicationPath → connects_from → NetworkInterface
- CommunicationPath → connects_to → NetworkInterface
- CommunicationPath → routes_through → NetworkDevice

**Layer 6 (Security)**:
- CertificateAuthority → trusts → CertificateAuthority (hierarchy)
- Certificate → issued_by → CertificateAuthority
- Firewall → enforces → SecurityPolicy
- Firewall → protects → SecurityZone
- SecurityZone → governed_by → SecurityPolicy

---

## Implementation Status

### ✅ Completed
- [x] Layer 5 specification updated with new relationships
- [x] OWL ontology updated with new object properties
- [x] Visual diagrams updated with intra-layer relationships
- [x] Added CommunicationPath endpoint relationships
- [x] Added NetworkInterface to NetworkDevice connection
- [x] Added Pod to NetworkInterface attachment range
- [x] Created comprehensive SPARQL queries

### 📋 Recommended Next Steps
- [ ] Add SHACL validation for new relationships
- [ ] Create sample data demonstrating new relationships
- [ ] Add Cypher queries for Neo4j implementation
- [ ] Update usage guide with new query patterns
- [ ] Add performance optimization tips for path queries
- [ ] Create visualization examples using new relationships

---

## References

### Related Documents
- **Layer 5 Specification**: `layer-specifications/layer5-network-topology.md`
- **OWL Ontology**: `ontology/it-infrastructure-ontology.ttl`
- **Visual Diagrams**: `ontology/VISUAL_DIAGRAMS.md`
- **Requirements**: `.kiro/specs/it-infrastructure-ontology/requirements.md`
- **Design**: `.kiro/specs/it-infrastructure-ontology/design.md`

### Framework Sources
- CIM (Common Information Model) - Network Model
- TOGAF Technology Architecture
- IETF Network Management Standards
- Kubernetes API
- AWS/Azure/GCP Network APIs

---

## Change Log

| Date | Change | Rationale |
|------|--------|-----------|
| 2024-12-01 | Added connects_from/connects_to for CommunicationPath | Enable precise endpoint identification |
| 2024-12-01 | Added connected_to_port for NetworkInterface | Enable switch port troubleshooting |
| 2024-12-01 | Added Pod to attached_to range | Properly model Kubernetes networking |
| 2024-12-01 | Confirmed ApplicationServer in Layer 4 | Consistent with infrastructure hosting model |
| 2024-12-01 | Confirmed NetworkDevice is essential | Critical for root cause analysis |
| 2024-12-01 | Added comprehensive intra-layer diagrams | Improve model visibility and understanding |

---

**Document Maintained By**: IT Infrastructure Ontology Working Group  
**Last Updated**: 2024-12-01
