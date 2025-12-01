# IT Infrastructure Ontology - Quick Reference

## Essential Relationships Cheat Sheet

### Network Layer (Layer 5) - Most Important

```turtle
# Complete communication path model
:ServiceA :communicates_via :Path_A_to_B .

:Path_A_to_B
  :connects_from :eth0_vmA ;           # Source endpoint (REQUIRED)
  :routes_through :Router01 ;          # Intermediate hop (OPTIONAL, 0..*)
  :routes_through :Firewall01 ;        # Intermediate hop (OPTIONAL, 0..*)
  :routes_through :LoadBalancer01 ;    # Intermediate hop (OPTIONAL, 0..*)
  :connects_to :eth0_vmB .             # Destination endpoint (REQUIRED)

:eth0_vmA
  :attached_to :VM_ServiceA ;          # Attached to compute resource
  :connected_to_port :Switch01 ;       # Connected to switch port
  :part_of_segment :Subnet_App ;       # Part of network segment
  :ip_address "10.1.10.5" .

:eth0_vmB
  :attached_to :VM_ServiceB ;
  :connected_to_port :Switch02 ;
  :part_of_segment :Subnet_DB ;
  :ip_address "10.1.20.10" .
```

### Application Layer (Layer 2)

```turtle
:Application_OrderService
  :contains :Component_OrderServlet ;   # Application components
  :contains :Service_OrderAPI ;         # Microservices
  :exposes :API_OrderREST ;            # APIs
  :uses :Database_OrderDB ;            # Databases
  :uses :MessageQueue_Orders ;         # Message queues
  :uses :CacheService_Session ;        # Cache services
  :hosted_on :AppServer_WebSphere ;    # Hosted on app server
  :deployed_as :Pod_OrderService .     # Or deployed as pod

:Service_OrderAPI
  :calls :Service_PaymentAPI .         # Service-to-service calls

:Database_OrderDB
  :contains :DatabaseInstance_PROD ;   # Database instances
  :contains :DataObject_OrdersTable .  # Data objects (tables)
```

### Container Layer (Layer 3)

```turtle
:Cluster_Production
  :contains :Namespace_Prod .

:Namespace_Prod
  :contains :Deployment_OrderService .

:Deployment_OrderService
  :manages :Pod_OrderService_1 ;
  :manages :Pod_OrderService_2 .

:Pod_OrderService_1
  :contains :Container_OrderApp ;
  :contains :Container_Sidecar .

:Container_OrderApp
  :uses_image :Image_OrderService_v1_2 .

:KubernetesService_OrderService
  :exposes :Pod_OrderService_1 ;
  :exposes :Pod_OrderService_2 .

:Route_OrderService
  :routes_to :KubernetesService_OrderService .
```

### Infrastructure Layer (Layer 4)

```turtle
# Virtual infrastructure
:VirtualMachine_App01
  :runs_on :Hypervisor_ESXi01 .

:Hypervisor_ESXi01
  :runs_on :PhysicalServer_Rack05 .

# Application server (legacy)
:AppServer_WebSphere01
  :runs_on :VirtualMachine_App01 .

# Storage hierarchy
:StorageArray_NetApp01
  :contains :StoragePool_Production .

:StoragePool_Production
  :allocates :StorageVolume_App01 .

:FileSystem_AppData
  :mounted_from :StorageVolume_App01 .
```

### Security Layer (Layer 6)

```turtle
# Certificate hierarchy
:Certificate_WildcardExample
  :issued_by :CertificateAuthority_Intermediate .

:CertificateAuthority_Intermediate
  :trusts :CertificateAuthority_Root .

# Firewall and policies
:Firewall_DMZ
  :enforces :SecurityPolicy_NetworkAccess ;
  :protects :SecurityZone_DMZ .

:SecurityZone_DMZ
  :governed_by :SecurityPolicy_NetworkAccess .
```

---

## Essential SPARQL Queries

### 1. Trace Network Path Between Services

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

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

### 2. Find Root Cause of Communication Failure

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?component ?type ?status
WHERE {
  :ServiceA :communicates_via ?path .
  {
    ?path :routes_through ?component .
    ?component :lifecycle_status ?status .
    FILTER(?status != "active")
    BIND("NetworkDevice" AS ?type)
  } UNION {
    ?path :connects_from|:connects_to ?component .
    ?component :lifecycle_status ?status .
    FILTER(?status != "up")
    BIND("NetworkInterface" AS ?type)
  }
}
```

### 3. Impact Analysis - Services Affected by Device Failure

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT DISTINCT ?service ?serviceName
WHERE {
  ?path :routes_through :Router_Core01 .
  ?service :communicates_via ?path .
  ?service :name ?serviceName .
}
```

### 4. Full Stack Decomposition - Business to Infrastructure

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?business ?app ?pod ?vm ?server
WHERE {
  ?business :realized_by ?app .
  ?app :deployed_as ?pod .
  ?pod :runs_on ?vm .
  ?vm :runs_on ?server .
}
```

### 5. Find Which Switch Port a VM is Connected To

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>

SELECT ?vm ?interface ?switch ?port
WHERE {
  ?vm :has_interface ?interface .
  ?interface :connected_to_port ?switch .
  ?switch :name ?port .
}
```

---

## Common Patterns

### Pattern 1: Containerized Application

```
BusinessProcess
  ↓ realized_by
Application
  ↓ deployed_as
Pod
  ↓ contains
Container
  ↓ uses_image
ContainerImage
  ↓ runs_on
VirtualMachine
  ↓ runs_on
PhysicalServer
```

### Pattern 2: Legacy Application

```
BusinessProcess
  ↓ realized_by
Application
  ↓ hosted_on
ApplicationServer (WebSphere/Tomcat)
  ↓ runs_on
VirtualMachine
  ↓ runs_on
Hypervisor
  ↓ runs_on
PhysicalServer
```

### Pattern 3: Network Communication

```
Application (Source)
  ↓ communicates_via
CommunicationPath
  ↓ connects_from
NetworkInterface (Source)
  ↓ connected_to_port
NetworkDevice (Switch)
  ↓ connected_to
NetworkDevice (Router)
  ↓ connected_to
NetworkDevice (Firewall)
  ↓ connected_to
NetworkDevice (Switch)
  ↑ connected_to_port
NetworkInterface (Destination)
  ↑ connects_to
CommunicationPath
  ↑ communicates_via
Application (Destination)
```

---

## Key Design Principles

### ✅ DO

1. **Use NetworkInterface for endpoints**
   ```turtle
   :Path :connects_from :eth0_source ;
         :connects_to :eth0_dest .
   ```

2. **Use NetworkDevice for routing**
   ```turtle
   :Path :routes_through :Router01, :Firewall01 .
   ```

3. **Attach NetworkInterface to Pod (not Container) in Kubernetes**
   ```turtle
   :eth0 :attached_to :Pod_OrderService .
   ```

4. **Place ApplicationServer in Layer 4**
   ```turtle
   :AppServer_WebSphere rdf:type :ApplicationServer .
   # ApplicationServer is in PhysicalInfrastructureLayer
   ```

5. **Keep NetworkDevice for troubleshooting**
   - Essential for root cause analysis
   - Cannot be removed

### ❌ DON'T

1. **Don't connect CommunicationPath directly to NetworkDevice**
   ```turtle
   # WRONG
   :Path :connects_to :Switch01 .
   ```

2. **Don't attach NetworkInterface to Container in Kubernetes**
   ```turtle
   # WRONG
   :eth0 :attached_to :Container_App .
   ```

3. **Don't remove NetworkDevice**
   - Loses critical troubleshooting capability

---

## File Locations

### Core Files
- **Ontology**: `ontology/it-infrastructure-ontology.ttl`
- **Layer 5 Spec**: `layer-specifications/layer5-network-topology.md`
- **Visual Diagrams**: `ontology/VISUAL_DIAGRAMS.md`

### Documentation
- **Design Decisions**: `.kiro/specs/it-infrastructure-ontology/DESIGN_DECISIONS.md`
- **Improvements Log**: `.kiro/specs/it-infrastructure-ontology/IMPROVEMENTS_LOG.md`
- **Quick Reference**: `.kiro/specs/it-infrastructure-ontology/QUICK_REFERENCE.md` (this file)

### Steering
- **Tech Stack**: `.kiro/steering/tech.md`
- **Structure**: `.kiro/steering/structure.md`
- **Product**: `.kiro/steering/product.md`

---

## Validation Commands

```bash
# Validate ontology syntax
rapper -i turtle -o ntriples ontology/it-infrastructure-ontology.ttl > /dev/null

# Validate sample data against SHACL
pyshacl -s ontology/shacl-shapes.ttl -d ontology/sample-data-cloud.ttl

# Run SPARQL queries
python ontology/test_queries.py
```

---

**Quick Reference Version**: 1.0  
**Last Updated**: 2024-12-01  
**For**: IT Infrastructure Ontology v1.0.0
