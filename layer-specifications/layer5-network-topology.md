# Layer 5: Network Topology and Communication Path - Complete Specification

## Overview

This document provides the complete formal specification for Layer 5 (Network Topology and Communication Path) of the IT Infrastructure and Application Dependency Ontology. The Network layer represents network infrastructure and communication paths that enable connectivity between components across all other layers.

**Layer Purpose**: Represents network infrastructure and communication paths between components.

**Layer Scope**: All network components including network devices (routers, switches, load balancers), network interfaces, network segments (subnets, VLANs), communication paths, and routing configurations. This layer provides the connectivity fabric for all other layers.

**Framework Sources**: 
- CIM (Common Information Model) - Network Model
- TOGAF Technology Architecture - Communication Infrastructure
- IETF Network Management Standards
- Cloud Provider Network APIs (AWS VPC, Azure Virtual Network, GCP VPC)

**Key Characteristics**:
- Enables connectivity between all infrastructure components
- Supports both physical and virtual networking
- Models network topology and communication paths
- Provides routing and load balancing abstractions
- Supports on-premises, cloud, and hybrid networking

---

## Entity Type Specifications

### 1. NetworkDevice

**Definition**: A network device such as a router, switch, firewall, or gateway.

**OWL Class Definition**:
```turtle
:NetworkDevice
  rdf:type owl:Class ;
  rdfs:subClassOf :NetworkLayer ;
  rdfs:label "Network Device" ;
  rdfs:comment "A network device such as router, switch, or gateway" ;
  skos:definition "A network device is a hardware or virtual appliance that routes, switches, or processes network traffic" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Device name or hostname |
| device_id | xsd:string | 0..1 | optional | CIM | Unique device identifier |
| device_type | xsd:string | 1..1 | enum | CIM | Device type: router, switch, load_balancer, firewall, gateway, proxy |
| manufacturer | xsd:string | 0..1 | optional | CIM | Device manufacturer (e.g., "Cisco", "Juniper", "F5") |
| model | xsd:string | 0..1 | optional | CIM | Device model number |
| serial_number | xsd:string | 0..1 | optional | CIM | Hardware serial number |
| firmware_version | xsd:string | 0..1 | optional | CIM | Firmware or OS version |
| management_ip | xsd:string | 0..1 | optional | CIM | Management IP address |
| location | xsd:string | 1..1 | mandatory | CIM | Physical or logical location |
| is_virtual | xsd:boolean | 0..1 | optional | CIM | Whether device is virtual (e.g., virtual router) |
| port_count | xsd:integer | 0..1 | optional | CIM | Number of network ports |
| throughput_gbps | xsd:decimal | 0..1 | optional | CIM | Maximum throughput in Gbps |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Operational state: active, inactive, degraded, failed, maintenance |

**Enumeration Values**:
- **device_type**: `router`, `switch`, `load_balancer`, `firewall`, `gateway`, `proxy`, `vpn_gateway`
- **lifecycle_status**: `active`, `inactive`, `degraded`, `failed`, `maintenance`, `provisioning`

**SHACL Validation Shape**:
```turtle
:NetworkDeviceShape
  a sh:NodeShape ;
  sh:targetClass :NetworkDevice ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
  ] ;
  sh:property [
    sh:path :device_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "router" "switch" "load_balancer" "firewall" "gateway" "proxy" "vpn_gateway" ) ;
  ] ;
  sh:property [
    sh:path :location ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "inactive" "degraded" "failed" "maintenance" "provisioning" ) ;
  ] .
```

---

### 2. LoadBalancer

**Definition**: A load balancing device or service that distributes traffic across multiple targets.

**OWL Class Definition**:
```turtle
:LoadBalancer
  rdf:type owl:Class ;
  rdfs:subClassOf :NetworkLayer ;
  rdfs:label "Load Balancer" ;
  rdfs:comment "A load balancing device or service" ;
  skos:definition "A load balancer distributes network traffic across multiple backend targets for high availability and performance" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Load balancer name |
| lb_id | xsd:string | 0..1 | optional | Cloud APIs | Unique load balancer identifier |
| lb_type | xsd:string | 1..1 | enum | CIM | Load balancer type: hardware, software, cloud |
| algorithm | xsd:string | 0..1 | enum | CIM | Load balancing algorithm: round_robin, least_connections, ip_hash, weighted |
| protocol | xsd:string | 0..* | enum | CIM | Supported protocols: http, https, tcp, udp |
| frontend_ip | xsd:string | 0..1 | optional | CIM | Frontend IP address |
| frontend_port | xsd:integer | 0..1 | optional | CIM | Frontend port number |
| backend_port | xsd:integer | 0..1 | optional | CIM | Backend port number |
| health_check_enabled | xsd:boolean | 0..1 | optional | Cloud APIs | Whether health checks are enabled |
| health_check_interval | xsd:integer | 0..1 | optional | Cloud APIs | Health check interval in seconds |
| session_persistence | xsd:boolean | 0..1 | optional | CIM | Whether session persistence is enabled |
| ssl_termination | xsd:boolean | 0..1 | optional | CIM | Whether SSL/TLS termination is enabled |
| location | xsd:string | 1..1 | mandatory | CIM | Physical or cloud location |
| cloud_provider | xsd:string | 0..1 | enum | Cloud APIs | Cloud provider if cloud-based: aws, azure, gcp |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Operational state: active, inactive, degraded, failed, provisioning |

**Enumeration Values**:
- **lb_type**: `hardware`, `software`, `cloud`, `virtual`
- **algorithm**: `round_robin`, `least_connections`, `ip_hash`, `weighted`, `least_response_time`
- **protocol**: `http`, `https`, `tcp`, `udp`, `grpc`
- **cloud_provider**: `aws`, `azure`, `gcp`, `alibaba`, `oracle`
- **lifecycle_status**: `active`, `inactive`, `degraded`, `failed`, `provisioning`, `deleting`

**SHACL Validation Shape**:
```turtle
:LoadBalancerShape
  a sh:NodeShape ;
  sh:targetClass :LoadBalancer ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lb_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "hardware" "software" "cloud" "virtual" ) ;
  ] ;
  sh:property [
    sh:path :location ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "inactive" "degraded" "failed" "provisioning" "deleting" ) ;
  ] .
```

---

### 3. NetworkInterface

**Definition**: A network interface card (NIC) or virtual network interface.

**OWL Class Definition**:
```turtle
:NetworkInterface
  rdf:type owl:Class ;
  rdfs:subClassOf :NetworkLayer ;
  rdfs:label "Network Interface" ;
  rdfs:comment "A network interface card or virtual NIC" ;
  skos:definition "A network interface provides network connectivity for a compute resource" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Interface name (e.g., "eth0", "ens192") |
| interface_id | xsd:string | 0..1 | optional | CIM | Unique interface identifier |
| interface_type | xsd:string | 1..1 | enum | CIM | Interface type: physical, virtual, loopback |
| mac_address | xsd:string | 0..1 | optional | CIM | MAC address |
| ip_address | xsd:string | 0..1 | optional | CIM | IPv4 address |
| ipv6_address | xsd:string | 0..1 | optional | CIM | IPv6 address |
| subnet_mask | xsd:string | 0..1 | optional | CIM | Subnet mask |
| gateway | xsd:string | 0..1 | optional | CIM | Default gateway IP |
| speed_mbps | xsd:integer | 0..1 | optional | CIM | Interface speed in Mbps |
| duplex | xsd:string | 0..1 | enum | CIM | Duplex mode: full, half, auto |
| mtu | xsd:integer | 0..1 | optional | CIM | Maximum transmission unit |
| is_primary | xsd:boolean | 0..1 | optional | CIM | Whether this is the primary interface |
| vlan_id | xsd:integer | 0..1 | optional | CIM | VLAN identifier if tagged |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Interface state: up, down, disabled, testing |

**Enumeration Values**:
- **interface_type**: `physical`, `virtual`, `loopback`, `tunnel`
- **duplex**: `full`, `half`, `auto`
- **lifecycle_status**: `up`, `down`, `disabled`, `testing`, `dormant`

**SHACL Validation Shape**:
```turtle
:NetworkInterfaceShape
  a sh:NodeShape ;
  sh:targetClass :NetworkInterface ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :interface_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "physical" "virtual" "loopback" "tunnel" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "up" "down" "disabled" "testing" "dormant" ) ;
  ] .
```

---

### 4. NetworkSegment

**Definition**: A network subnet or VLAN that groups network resources.

**OWL Class Definition**:
```turtle
:NetworkSegment
  rdf:type owl:Class ;
  rdfs:subClassOf :NetworkLayer ;
  rdfs:label "Network Segment" ;
  rdfs:comment "A network subnet or VLAN" ;
  skos:definition "A network segment is a logical subdivision of a network" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Segment name |
| segment_id | xsd:string | 0..1 | optional | CIM | Unique segment identifier |
| segment_type | xsd:string | 1..1 | enum | CIM | Segment type: subnet, vlan, vpc, vnet |
| cidr_block | xsd:string | 0..1 | optional | IETF | CIDR notation (e.g., "10.0.1.0/24") |
| vlan_id | xsd:integer | 0..1 | optional | CIM | VLAN identifier (1-4094) |
| gateway_ip | xsd:string | 0..1 | optional | CIM | Gateway IP address |
| dhcp_enabled | xsd:boolean | 0..1 | optional | CIM | Whether DHCP is enabled |
| dns_servers | xsd:string | 0..* | optional | CIM | DNS server IP addresses |
| location | xsd:string | 1..1 | mandatory | CIM | Physical or cloud location |
| cloud_provider | xsd:string | 0..1 | enum | Cloud APIs | Cloud provider if cloud-based: aws, azure, gcp |
| vpc_id | xsd:string | 0..1 | optional | Cloud APIs | VPC/VNet identifier for cloud segments |
| availability_zone | xsd:string | 0..1 | optional | Cloud APIs | Availability zone for cloud segments |
| is_public | xsd:boolean | 0..1 | optional | Cloud APIs | Whether segment has public internet access |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Segment state: active, inactive, creating, deleting |

**Enumeration Values**:
- **segment_type**: `subnet`, `vlan`, `vpc`, `vnet`, `security_group`
- **cloud_provider**: `aws`, `azure`, `gcp`, `alibaba`, `oracle`
- **lifecycle_status**: `active`, `inactive`, `creating`, `deleting`, `failed`

**SHACL Validation Shape**:
```turtle
:NetworkSegmentShape
  a sh:NodeShape ;
  sh:targetClass :NetworkSegment ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :segment_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "subnet" "vlan" "vpc" "vnet" "security_group" ) ;
  ] ;
  sh:property [
    sh:path :location ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "inactive" "creating" "deleting" "failed" ) ;
  ] .
```

---

### 5. CommunicationPath

**Definition**: A logical communication path between two components.

**OWL Class Definition**:
```turtle
:CommunicationPath
  rdf:type owl:Class ;
  rdfs:subClassOf :NetworkLayer ;
  rdfs:label "Communication Path" ;
  rdfs:comment "A logical communication path between components" ;
  skos:definition "A communication path represents the network route and protocol used for communication between two components" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Path name or description |
| path_id | xsd:string | 0..1 | optional | CIM | Unique path identifier |
| protocol | xsd:string | 1..1 | enum | IETF | Communication protocol: http, https, tcp, udp, grpc, amqp, mqtt |
| source_port | xsd:integer | 0..1 | optional | IETF | Source port number |
| destination_port | xsd:integer | 0..1 | optional | IETF | Destination port number |
| source_ip | xsd:string | 0..1 | optional | IETF | Source IP address or range |
| destination_ip | xsd:string | 0..1 | optional | IETF | Destination IP address or range |
| bandwidth_mbps | xsd:decimal | 0..1 | optional | CIM | Allocated bandwidth in Mbps |
| latency_ms | xsd:decimal | 0..1 | optional | CIM | Average latency in milliseconds |
| encrypted | xsd:boolean | 0..1 | optional | CIM | Whether communication is encrypted |
| encryption_protocol | xsd:string | 0..1 | enum | IETF | Encryption protocol: tls, ipsec, ssh |
| qos_class | xsd:string | 0..1 | enum | CIM | Quality of Service class: high, medium, low, best_effort |
| path_type | xsd:string | 1..1 | enum | CIM | Path type: direct, routed, vpn, internet |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Path state: active, inactive, degraded, failed |

**Enumeration Values**:
- **protocol**: `http`, `https`, `tcp`, `udp`, `grpc`, `amqp`, `mqtt`, `kafka`, `redis`, `sql`
- **encryption_protocol**: `tls`, `ipsec`, `ssh`, `none`
- **qos_class**: `high`, `medium`, `low`, `best_effort`
- **path_type**: `direct`, `routed`, `vpn`, `internet`, `private_link`
- **lifecycle_status**: `active`, `inactive`, `degraded`, `failed`, `establishing`

**SHACL Validation Shape**:
```turtle
:CommunicationPathShape
  a sh:NodeShape ;
  sh:targetClass :CommunicationPath ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :protocol ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "http" "https" "tcp" "udp" "grpc" "amqp" "mqtt" "kafka" "redis" "sql" ) ;
  ] ;
  sh:property [
    sh:path :path_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "direct" "routed" "vpn" "internet" "private_link" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "inactive" "degraded" "failed" "establishing" ) ;
  ] .
```

---

### 6. NetworkRoute

**Definition**: A routing rule or path configuration.

**OWL Class Definition**:
```turtle
:NetworkRoute
  rdf:type owl:Class ;
  rdfs:subClassOf :NetworkLayer ;
  rdfs:label "Network Route" ;
  rdfs:comment "A routing rule or path configuration" ;
  skos:definition "A network route defines how traffic is directed from source to destination" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Route name or description |
| route_id | xsd:string | 0..1 | optional | CIM | Unique route identifier |
| destination_cidr | xsd:string | 1..1 | mandatory | IETF | Destination CIDR block |
| next_hop | xsd:string | 0..1 | optional | IETF | Next hop IP address or gateway |
| next_hop_type | xsd:string | 0..1 | enum | Cloud APIs | Next hop type: gateway, instance, nat, vpn, peering |
| metric | xsd:integer | 0..1 | optional | IETF | Route metric or priority |
| route_type | xsd:string | 1..1 | enum | IETF | Route type: static, dynamic, default |
| protocol | xsd:string | 0..1 | enum | IETF | Routing protocol: bgp, ospf, static, rip |
| administrative_distance | xsd:integer | 0..1 | optional | IETF | Administrative distance |
| is_active | xsd:boolean | 0..1 | optional | CIM | Whether route is currently active |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Route state: active, inactive, blackhole, propagating |

**Enumeration Values**:
- **next_hop_type**: `gateway`, `instance`, `nat`, `vpn`, `peering`, `internet_gateway`, `local`
- **route_type**: `static`, `dynamic`, `default`, `propagated`
- **protocol**: `bgp`, `ospf`, `static`, `rip`, `eigrp`, `isis`
- **lifecycle_status**: `active`, `inactive`, `blackhole`, `propagating`, `failed`

**SHACL Validation Shape**:
```turtle
:NetworkRouteShape
  a sh:NodeShape ;
  sh:targetClass :NetworkRoute ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :destination_cidr ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:pattern "^([0-9]{1,3}\\.){3}[0-9]{1,3}/[0-9]{1,2}$" ;
  ] ;
  sh:property [
    sh:path :route_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "static" "dynamic" "default" "propagated" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "inactive" "blackhole" "propagating" "failed" ) ;
  ] .
```

---

## Relationship Specifications

### Intra-Layer Relationships

These relationships connect entities within Layer 5 (Network).

#### 1. connected_to

**Definition**: Physical or logical connection between network devices.

**Domain**: NetworkDevice
**Range**: NetworkDevice
**Cardinality**: many-to-many (*..*)
**Inver
se**: connected_to (symmetric relationship)
**Properties**:
- connection_type (enum): physical, logical, virtual
- bandwidth_gbps (decimal): Connection bandwidth
- link_status (enum): up, down, degraded

**OWL Definition**:
```turtle
:connected_to
  rdf:type owl:ObjectProperty ;
  rdf:type owl:SymmetricProperty ;
  rdfs:domain :NetworkDevice ;
  rdfs:range :NetworkDevice ;
  rdfs:label "connected to" ;
  rdfs:comment "Physical or logical connection between network devices" .
```

**Usage Example**:
```turtle
:Router_Core01 :connected_to :Switch_Access01 .
:Switch_Access01 :connected_to :Router_Core01 .
```

---

#### 2. connects_from

**Definition**: A communication path originates from a source network interface.

**Domain**: CommunicationPath
**Range**: NetworkInterface
**Cardinality**: many-to-one (*..1) - a path has one source interface

**Inverse**: source_of (NetworkInterface is source of CommunicationPath)
**Properties**:
- connection_established (dateTime): When connection was established
- source_port (integer): Source port number

**OWL Definition**:
```turtle
:connects_from
  rdf:type owl:ObjectProperty ;
  rdf:type owl:FunctionalProperty ;
  rdfs:domain :CommunicationPath ;
  rdfs:range :NetworkInterface ;
  rdfs:label "connects from" ;
  rdfs:comment "Communication path originates from source network interface" .

:source_of
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :connects_from ;
  rdfs:domain :NetworkInterface ;
  rdfs:range :CommunicationPath .
```

**Usage Example**:
```turtle
:Path_App1_to_DB1 :connects_from :eth0_app_vm01 .
:eth0_app_vm01 :source_of :Path_App1_to_DB1 .
```

---

#### 3. connects_to

**Definition**: A communication path terminates at a destination network interface.

**Domain**: CommunicationPath
**Range**: NetworkInterface
**Cardinality**: many-to-one (*..1) - a path has one destination interface

**Inverse**: destination_of (NetworkInterface is destination of CommunicationPath)
**Properties**:
- connection_established (dateTime): When connection was established
- destination_port (integer): Destination port number

**OWL Definition**:
```turtle
:connects_to
  rdf:type owl:ObjectProperty ;
  rdf:type owl:FunctionalProperty ;
  rdfs:domain :CommunicationPath ;
  rdfs:range :NetworkInterface ;
  rdfs:label "connects to" ;
  rdfs:comment "Communication path terminates at destination network interface" .

:destination_of
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :connects_to ;
  rdfs:domain :NetworkInterface ;
  rdfs:range :CommunicationPath .
```

**Usage Example**:
```turtle
:Path_App1_to_DB1 :connects_to :eth0_db_vm01 .
:eth0_db_vm01 :destination_of :Path_App1_to_DB1 .
```

---

#### 4. routes_through

**Definition**: A communication path routes through intermediate network devices.

**Domain**: CommunicationPath
**Range**: NetworkDevice
**Cardinality**: many-to-many (*..*) - a path can route through multiple devices

**Inverse**: routes (NetworkDevice routes CommunicationPath)
**Properties**:
- hop_number (integer): Sequence number in the path
- latency_contribution_ms (decimal): Latency added by this hop

**OWL Definition**:
```turtle
:routes_through
  rdf:type owl:ObjectProperty ;
  rdfs:domain :CommunicationPath ;
  rdfs:range :NetworkDevice ;
  rdfs:label "routes through" ;
  rdfs:comment "Communication path routes through intermediate network device" .

:routes
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :routes_through ;
  rdfs:domain :NetworkDevice ;
  rdfs:range :CommunicationPath .
```

**Usage Example**:
```turtle
:Path_App1_to_DB1 :connects_from :eth0_app_vm01 .
:Path_App1_to_DB1 :routes_through :Router_Core01 .
:Path_App1_to_DB1 :routes_through :Firewall_DMZ .
:Path_App1_to_DB1 :routes_through :Switch_DB .
:Path_App1_to_DB1 :connects_to :eth0_db_vm01 .
```

---

#### 5. attached_to

**Definition**: A network interface is attached to a compute resource.

**Domain**: NetworkInterface
**Range**: PhysicalServer | VirtualMachine | CloudInstance | Container | Pod
**Cardinality**: many-to-one (*..1) - interface attached to one resource

**Inverse**: has_interface (Compute resource has NetworkInterface)
**Properties**:
- attachment_type (enum): primary, secondary, management
- attachment_time (dateTime): When interface was attached

**OWL Definition**:
```turtle
:attached_to
  rdf:type owl:ObjectProperty ;
  rdf:type owl:FunctionalProperty ;
  rdfs:domain :NetworkInterface ;
  rdfs:range [ owl:unionOf ( :PhysicalServer :VirtualMachine :CloudInstance :Container :Pod ) ] ;
  rdfs:label "attached to" ;
  rdfs:comment "Network interface attached to compute resource" .

:has_interface
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :attached_to ;
  rdfs:domain [ owl:unionOf ( :PhysicalServer :VirtualMachine :CloudInstance :Container ) ] ;
  rdfs:range :NetworkInterface .
```

**Usage Example**:
```turtle
:eth0_vm01 :attached_to :VM_AppServer01 .
:VM_AppServer01 :has_interface :eth0_vm01 .
```

---

#### 6. connected_to_port

**Definition**: A network interface is physically or logically connected to a port on a network device.

**Domain**: NetworkInterface
**Range**: NetworkDevice
**Cardinality**: many-to-one (*..1) - interface connects to one device port

**Inverse**: has_connected_interface (NetworkDevice has connected interfaces)
**Properties**:
- port_number (string): Port identifier on the network device (e.g., "GigabitEthernet0/1", "eth0")
- connection_type (enum): physical, virtual, trunk, access
- port_speed_mbps (integer): Port speed in Mbps
- vlan_mode (enum): access, trunk, hybrid

**OWL Definition**:
```turtle
:connected_to_port
  rdf:type owl:ObjectProperty ;
  rdf:type owl:FunctionalProperty ;
  rdfs:domain :NetworkInterface ;
  rdfs:range :NetworkDevice ;
  rdfs:label "connected to port" ;
  rdfs:comment "Network interface is connected to a port on a network device" ;
  skos:definition "Represents the physical or logical connection between a network interface and a specific port on a network device (switch, router)" .

:has_connected_interface
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :connected_to_port ;
  rdfs:domain :NetworkDevice ;
  rdfs:range :NetworkInterface ;
  rdfs:label "has connected interface" ;
  rdfs:comment "Network device has network interface connected to its port" .
```

**Usage Example**:
```turtle
# VM's network interface connected to switch port
:eth0_vm01 :connected_to_port :Switch_Access01 .
:Switch_Access01 :has_connected_interface :eth0_vm01 .

# Physical server NIC connected to switch
:nic0_server01 :connected_to_port :Switch_Core01 .
:Switch_Core01 :has_connected_interface :nic0_server01 .
```

---

#### 7. part_of_segment

**Definition**: A network interface or device is part of a network segment.

**Domain**: NetworkInterface | NetworkDevice
**Range**: NetworkSegment
**Cardinality**: many-to-one (*..1) - interface/device in one segment

**Inverse**: contains (NetworkSegment contains interfaces/devices)
**Properties**:
- membership_type (enum): member, gateway, dhcp_server

**OWL Definition**:
```turtle
:part_of_segment
  rdf:type owl:ObjectProperty ;
  rdf:type owl:FunctionalProperty ;
  rdfs:domain [ owl:unionOf ( :NetworkInterface :NetworkDevice ) ] ;
  rdfs:range :NetworkSegment ;
  rdfs:label "part of segment" ;
  rdfs:comment "Network interface or device is part of network segment" .

:contains
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :part_of_segment ;
  rdfs:domain :NetworkSegment ;
  rdfs:range [ owl:unionOf ( :NetworkInterface :NetworkDevice ) ] .
```

**Usage Example**:
```turtle
:eth0_vm01 :part_of_segment :Subnet_AppTier .
:Subnet_AppTier :contains :eth0_vm01 .
```

---

#### 8. applies_to

**Definition**: A network route applies to a network segment.

**Domain**: NetworkRoute
**Range**: NetworkSegment
**Cardinality**: many-to-one (*..1) - route applies to one segment

**Inverse**: has_route (NetworkSegment has routes)

**OWL Definition**:
```turtle
:applies_to
  rdf:type owl:ObjectProperty ;
  rdf:type owl:FunctionalProperty ;
  rdfs:domain :NetworkRoute ;
  rdfs:range :NetworkSegment ;
  rdfs:label "applies to" ;
  rdfs:comment "Network route applies to network segment" .

:has_route
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :applies_to ;
  rdfs:domain :NetworkSegment ;
  rdfs:range :NetworkRoute .
```

**Usage Example**:
```turtle
:Route_Default_Gateway :applies_to :Subnet_AppTier .
:Subnet_AppTier :has_route :Route_Default_Gateway .
```

---

#### 9. balances_to

**Definition**: A load balancer distributes traffic to backend targets.

**Domain**: LoadBalancer
**Range**: PhysicalServer | VirtualMachine | CloudInstance | Container | Service
**Cardinality**: one-to-many (1..*) - load balancer to multiple targets

**Inverse**: balanced_by (Target is balanced by LoadBalancer)
**Properties**:
- weight (integer): Load balancing weight
- health_status (enum): healthy, unhealthy, draining
- enabled (boolean): Whether target is enabled

**OWL Definition**:
```turtle
:balances_to
  rdf:type owl:ObjectProperty ;
  rdfs:domain :LoadBalancer ;
  rdfs:range [ owl:unionOf ( :PhysicalServer :VirtualMachine :CloudInstance :Container :Service ) ] ;
  rdfs:label "balances to" ;
  rdfs:comment "Load balancer distributes traffic to backend targets" .

:balanced_by
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :balances_to ;
  rdfs:domain [ owl:unionOf ( :PhysicalServer :VirtualMachine :CloudInstance :Container :Service ) ] ;
  rdfs:range :LoadBalancer .
```

**Usage Example**:
```turtle
:LB_WebTier :balances_to :VM_Web01 .
:LB_WebTier :balances_to :VM_Web02 .
:LB_WebTier :balances_to :VM_Web03 .
```

---

### Cross-Layer Relationships

These relationships connect Layer 5 (Network) to other layers.

#### 10. communicates_via (Application → Network)

**Definition**: An application communicates via a communication path.

**Domain**: Application | Service | Database | MessageQueue
**Range**: CommunicationPath
**Cardinality**: many-to-many (*..*) - application can use multiple paths

**Inverse**: used_by (CommunicationPath used by Application)
**Properties**:
- criticality (enum): critical, high, medium, low
- traffic_volume_mbps (decimal): Average traffic volume

**OWL Definition**:
```turtle
:communicates_via
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Application :Service :Database :MessageQueue ) ] ;
  rdfs:range :CommunicationPath ;
  rdfs:label "communicates via" ;
  rdfs:comment "Application communicates via communication path" .

:used_by
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :communicates_via ;
  rdfs:domain :CommunicationPath ;
  rdfs:range [ owl:unionOf ( :Application :Service :Database :MessageQueue ) ] .
```

**Usage Example**:
```turtle
:App_OrderService :communicates_via :Path_OrderService_to_DB .
:Path_OrderService_to_DB :used_by :App_OrderService .
```

---

#### 11. exposes_via (Application → LoadBalancer)

**Definition**: An application or service is exposed via a load balancer.

**Domain**: Application | Service | Container
**Range**: LoadBalancer
**Cardinality**: many-to-many (*..*) - application can be exposed via multiple load balancers

**Inverse**: exposes (LoadBalancer exposes Application)
**Properties**:
- exposure_type (enum): public, private, internal
- port_mapping (string): Port mapping configuration

**OWL Definition**:
```turtle
:exposes_via
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Application :Service :Container ) ] ;
  rdfs:range :LoadBalancer ;
  rdfs:label "exposes via" ;
  rdfs:comment "Application is exposed via load balancer" .

:exposes
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :exposes_via ;
  rdfs:domain :LoadBalancer ;
  rdfs:range [ owl:unionOf ( :Application :Service :Container ) ] .
```

**Usage Example**:
```turtle
:App_WebPortal :exposes_via :LB_PublicWeb .
:LB_PublicWeb :exposes :App_WebPortal .
```

---

## Relationship Summary Table

| Relationship | Domain | Range | Cardinality | Type |
|--------------|--------|-------|-------------|------|
| connected_to | NetworkDevice | NetworkDevice | *..*  | Intra-layer |
| connects_from | CommunicationPath | NetworkInterface | *..1 | Intra-layer |
| connects_to | CommunicationPath | NetworkInterface | *..1 | Intra-layer |
| routes_through | CommunicationPath | NetworkDevice | *..* | Intra-layer |
| attached_to | NetworkInterface | Compute | *..1 | Cross-layer |
| connected_to_port | NetworkInterface | NetworkDevice | *..1 | Intra-layer |
| part_of_segment | NetworkInterface/Device | NetworkSegment | *..1 | Intra-layer |
| applies_to | NetworkRoute | NetworkSegment | *..1 | Intra-layer |
| balances_to | LoadBalancer | Compute/Service | 1..* | Cross-layer |
| communicates_via | Application/Service | CommunicationPath | *..* | Cross-layer |
| exposes_via | Application/Service | LoadBalancer | *..* | Cross-layer |

---

## Validation Rules

### Layer Assignment Rules

1. All network entity types belong exclusively to Layer 5
2. Network entities cannot have attributes from other layers
3. Cross-layer relationships must connect to entities in Layers 2, 3, or 4
4. Intra-layer relationships must connect entities within Layer 5

### Network-Specific Validation Rules

1. **NetworkInterface IP Validation**:
   - If ip_address is specified, subnet_mask must be specified
   - IP address must be valid IPv4 or IPv6 format
   - MAC address must be valid format (XX:XX:XX:XX:XX:XX)

2. **NetworkSegment CIDR Validation**:
   - CIDR block must be valid format (e.g., "10.0.1.0/24")
   - VLAN ID must be between 1 and 4094
   - Gateway IP must be within CIDR block

3. **CommunicationPath Port Validation**:
   - Port numbers must be between 1 and 65535
   - If encrypted is true, encryption_protocol must be specified
   - Protocol must match port number conventions (e.g., http on 80, https on 443)

4. **NetworkRoute CIDR Validation**:
   - Destination CIDR must be valid format
   - Metric must be positive integer
   - Administrative distance must be between 0 and 255

5. **LoadBalancer Configuration Validation**:
   - If health_check_enabled is true, health_check_interval must be specified
   - Frontend and backend ports must be valid (1-65535)
   - At least one backend target must be configured (balances_to relationship)

6. **Connectivity Validation**:
   - NetworkInterface must be attached_to exactly one compute resource
   - CommunicationPath must have exactly one connects_from relationship (source interface)
   - CommunicationPath must have exactly one connects_to relationship (destination interface)
   - CommunicationPath may have zero or more routes_through relationships (intermediate devices)
   - LoadBalancer must have at least one balances_to relationship

### SHACL Validation Examples

```turtle
# Validate NetworkInterface has valid IP and subnet
:NetworkInterfaceIPValidation
  a sh:NodeShape ;
  sh:targetClass :NetworkInterface ;
  sh:sparql [
    sh:message "If ip_address is specified, subnet_mask must also be specified" ;
    sh:select """
      SELECT $this
      WHERE {
        $this :ip_address ?ip .
        FILTER NOT EXISTS { $this :subnet_mask ?mask }
      }
    """ ;
  ] .

# Validate CommunicationPath has source and destination
:CommunicationPathEndpointValidation
  a sh:NodeShape ;
  sh:targetClass :CommunicationPath ;
  sh:property [
    sh:path :connects_from ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "Communication path must have exactly one source interface (connects_from)" ;
  ] ;
  sh:property [
    sh:path :connects_to ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "Communication path must have exactly one destination interface (connects_to)" ;
  ] .

# Validate LoadBalancer has targets
:LoadBalancerTargetValidation
  a sh:NodeShape ;
  sh:targetClass :LoadBalancer ;
  sh:property [
    sh:path :balances_to ;
    sh:minCount 1 ;
    sh:message "Load balancer must have at least one backend target" ;
  ] .
```

---

## Usage Patterns and Examples

### Pattern 1: On-Premises Network Topology

**Scenario**: Traditional three-tier application with physical network infrastructure.

**Components**:
- Core router connecting to internet
- Firewall protecting DMZ
- Load balancer in DMZ
- Access switches for web, app, and database tiers
- VLANs for network segmentation

**Entity Instances**:

```turtle
# Network Devices
:Router_Core01
  rdf:type :NetworkDevice ;
  :name "Core-Router-01" ;
  :device_type "router" ;
  :manufacturer "Cisco" ;
  :model "ASR 1001-X" ;
  :location "DC1-NetRoom-Rack01" ;
  :management_ip "10.0.0.1" ;
  :lifecycle_status "active" .

:Firewall_DMZ
  rdf:type :NetworkDevice ;
  :name "Firewall-DMZ-01" ;
  :device_type "firewall" ;
  :manufacturer "Palo Alto" ;
  :model "PA-5220" ;
  :location "DC1-NetRoom-Rack01" ;
  :management_ip "10.0.0.2" ;
  :lifecycle_status "active" .

:LB_WebTier
  rdf:type :LoadBalancer ;
  :name "LB-Web-01" ;
  :lb_type "hardware" ;
  :algorithm "round_robin" ;
  :protocol "https" ;
  :frontend_ip "203.0.113.10" ;
  :frontend_port 443 ;
  :backend_port 8080 ;
  :ssl_termination true ;
  :location "DC1-NetRoom-Rack02" ;
  :lifecycle_status "active" .

:Switch_WebTier
  rdf:type :NetworkDevice ;
  :name "Switch-Web-01" ;
  :device_type "switch" ;
  :manufacturer "Cisco" ;
  :model "Catalyst 9300" ;
  :location "DC1-NetRoom-Rack03" ;
  :port_count 48 ;
  :lifecycle_status "active" .

# Network Segments
:VLAN_DMZ
  rdf:type :NetworkSegment ;
  :name "VLAN-DMZ" ;
  :segment_type "vlan" ;
  :vlan_id 10 ;
  :cidr_block "10.10.0.0/24" ;
  :gateway_ip "10.10.0.1" ;
  :location "DC1" ;
  :lifecycle_status "active" .

:VLAN_WebTier
  rdf:type :NetworkSegment ;
  :name "VLAN-Web" ;
  :segment_type "vlan" ;
  :vlan_id 20 ;
  :cidr_block "10.20.0.0/24" ;
  :gateway_ip "10.20.0.1" ;
  :location "DC1" ;
  :lifecycle_status "active" .

# Network Interfaces
:eth0_web01
  rdf:type :NetworkInterface ;
  :name "eth0" ;
  :interface_type "virtual" ;
  :mac_address "00:50:56:01:23:45" ;
  :ip_address "10.20.0.10" ;
  :subnet_mask "255.255.255.0" ;
  :gateway "10.20.0.1" ;
  :vlan_id 20 ;
  :lifecycle_status "up" .

# Relationships
:Router_Core01 :connected_to :Firewall_DMZ .
:Firewall_DMZ :connected_to :LB_WebTier .
:LB_WebTier :connected_to :Switch_WebTier .

:eth0_web01 :attached_to :VM_Web01 .
:eth0_web01 :part_of_segment :VLAN_WebTier .

:LB_WebTier :balances_to :VM_Web01 .
:LB_WebTier :balances_to :VM_Web02 .
:LB_WebTier :balances_to :VM_Web03 .
```

---

### Pattern 2: Cloud Network Architecture (AWS VPC)

**Scenario**: Microservices application in AWS with VPC, subnets, and load balancers.

**Components**:
- VPC with public and private subnets
- Application Load Balancer (ALB)
- NAT Gateway for outbound traffic
- Internet Gateway for inbound traffic
- Route tables for traffic routing

**Entity Instances**:

```turtle
# Network Segments (VPC and Subnets)
:VPC_Production
  rdf:type :NetworkSegment ;
  :name "VPC-Production" ;
  :segment_type "vpc" ;
  :cidr_block "10.0.0.0/16" ;
  :cloud_provider "aws" ;
  :vpc_id "vpc-0123456789abcdef0" ;
  :location "us-east-1" ;
  :lifecycle_status "active" .

:Subnet_Public_1a
  rdf:type :NetworkSegment ;
  :name "Subnet-Public-1a" ;
  :segment_type "subnet" ;
  :cidr_block "10.0.1.0/24" ;
  :cloud_provider "aws" ;
  :vpc_id "vpc-0123456789abcdef0" ;
  :availability_zone "us-east-1a" ;
  :is_public true ;
  :location "us-east-1" ;
  :lifecycle_status "active" .

:Subnet_Private_1a
  rdf:type :NetworkSegment ;
  :name "Subnet-Private-1a" ;
  :segment_type "subnet" ;
  :cidr_block "10.0.10.0/24" ;
  :cloud_provider "aws" ;
  :vpc_id "vpc-0123456789abcdef0" ;
  :availability_zone "us-east-1a" ;
  :is_public false ;
  :location "us-east-1" ;
  :lifecycle_status "active" .

# Load Balancer
:ALB_API
  rdf:type :LoadBalancer ;
  :name "ALB-API-Gateway" ;
  :lb_id "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/api-gateway/50dc6c495c0c9188" ;
  :lb_type "cloud" ;
  :algorithm "least_connections" ;
  :protocol "https" ;
  :frontend_port 443 ;
  :backend_port 8080 ;
  :health_check_enabled true ;
  :health_check_interval 30 ;
  :ssl_termination true ;
  :cloud_provider "aws" ;
  :location "us-east-1" ;
  :lifecycle_status "active" .

# Network Devices (Gateways)
:IGW_Production
  rdf:type :NetworkDevice ;
  :name "IGW-Production" ;
  :device_id "igw-0123456789abcdef0" ;
  :device_type "gateway" ;
  :is_virtual true ;
  :location "us-east-1" ;
  :lifecycle_status "active" .

:NAT_Gateway_1a
  rdf:type :NetworkDevice ;
  :name "NAT-Gateway-1a" ;
  :device_id "nat-0123456789abcdef0" ;
  :device_type "gateway" ;
  :is_virtual true ;
  :location "us-east-1a" ;
  :lifecycle_status "active" .

# Routes
:Route_Public_Default
  rdf:type :NetworkRoute ;
  :name "Public-Default-Route" ;
  :destination_cidr "0.0.0.0/0" ;
  :next_hop "igw-0123456789abcdef0" ;
  :next_hop_type "internet_gateway" ;
  :route_type "static" ;
  :lifecycle_status "active" .

:Route_Private_Default
  rdf:type :NetworkRoute ;
  :name "Private-Default-Route" ;
  :destination_cidr "0.0.0.0/0" ;
  :next_hop "nat-0123456789abcdef0" ;
  :next_hop_type "nat" ;
  :route_type "static" ;
  :lifecycle_status "active" .

# Relationships
:Route_Public_Default :applies_to :Subnet_Public_1a .
:Route_Private_Default :applies_to :Subnet_Private_1a .

:ALB_API :balances_to :Container_API_Pod1 .
:ALB_API :balances_to :Container_API_Pod2 .
:ALB_API :balances_to :Container_API_Pod3 .
```

---

### Pattern 3: Communication Path Analysis

**Scenario**: Tracing network communication between microservices.

**Components**:
- Order Service communicating with Inventory Service
- Communication path routing through load balancer and firewall
- HTTPS protocol with TLS encryption

**Entity Instances**:

```turtle
# Communication Path
:Path_Order_to_Inventory
  rdf:type :CommunicationPath ;
  :name "Order-to-Inventory-Path" ;
  :protocol "https" ;
  :destination_port 443 ;
  :encrypted true ;
  :encryption_protocol "tls" ;
  :qos_class "high" ;
  :path_type "routed" ;
  :lifecycle_status "active" .

# Relationships
:Service_OrderAPI :communicates_via :Path_Order_to_Inventory .
:Path_Order_to_Inventory :routes_through :LB_Internal .
:Path_Order_to_Inventory :routes_through :Firewall_Internal .
:Path_Order_to_Inventory :routes_through :Switch_AppTier .
:Path_Order_to_Inventory :used_by :Service_InventoryAPI .
```

---

### Pattern 4: Hybrid Cloud Connectivity

**Scenario**: On-premises datacenter connected to AWS via VPN.

**Components**:
- On-premises VPN gateway
- AWS VPN gateway
- VPN tunnel for encrypted communication
- Route propagation between environments

**Entity Instances**:

```turtle
# VPN Gateways
:VPN_OnPrem
  rdf:type :NetworkDevice ;
  :name "VPN-Gateway-OnPrem" ;
  :device_type "vpn_gateway" ;
  :manufacturer "Cisco" ;
  :model "ASA 5516-X" ;
  :location "DC1-NetRoom" ;
  :management_ip "192.168.1.1" ;
  :lifecycle_status "active" .

:VPN_AWS
  rdf:type :NetworkDevice ;
  :name "VPN-Gateway-AWS" ;
  :device_id "vgw-0123456789abcdef0" ;
  :device_type "vpn_gateway" ;
  :is_virtual true ;
  :location "us-east-1" ;
  :lifecycle_status "active" .

# VPN Communication Path
:Path_VPN_Tunnel
  rdf:type :CommunicationPath ;
  :name "VPN-Tunnel-OnPrem-to-AWS" ;
  :protocol "ipsec" ;
  :encrypted true ;
  :encryption_protocol "ipsec" ;
  :bandwidth_mbps 1000 ;
  :path_type "vpn" ;
  :lifecycle_status "active" .

# Relationships
:VPN_OnPrem :connected_to :VPN_AWS .
:Path_VPN_Tunnel :routes_through :VPN_OnPrem .
:Path_VPN_Tunnel :routes_through :VPN_AWS .
```

---

### Pattern 5: Kubernetes Service Networking

**Scenario**: Kubernetes service exposing pods via load balancer.

**Components**:
- Kubernetes Service (ClusterIP)
- Ingress Controller
- External Load Balancer
- Pod network interfaces

**Entity Instances**:

```turtle
# Load Balancer (External)
:LB_K8s_Ingress
  rdf:type :LoadBalancer ;
  :name "K8s-Ingress-LB" ;
  :lb_type "cloud" ;
  :algorithm "round_robin" ;
  :protocol "https" ;
  :frontend_port 443 ;
  :backend_port 80 ;
  :health_check_enabled true ;
  :cloud_provider "aws" ;
  :location "us-west-2" ;
  :lifecycle_status "active" .

# Network Interfaces (Pod NICs)
:veth_pod1
  rdf:type :NetworkInterface ;
  :name "veth0" ;
  :interface_type "virtual" ;
  :ip_address "10.244.1.5" ;
  :subnet_mask "255.255.255.0" ;
  :lifecycle_status "up" .

# Communication Path
:Path_Ingress_to_Service
  rdf:type :CommunicationPath ;
  :name "Ingress-to-Service-Path" ;
  :protocol "http" ;
  :destination_port 8080 ;
  :path_type "direct" ;
  :lifecycle_status "active" .

# Relationships
:veth_pod1 :attached_to :Pod_API_1 .
:LB_K8s_Ingress :balances_to :Pod_API_1 .
:LB_K8s_Ingress :balances_to :Pod_API_2 .
:LB_K8s_Ingress :balances_to :Pod_API_3 .
:Service_API :exposes_via :LB_K8s_Ingress .
:Service_API :communicates_via :Path_Ingress_to_Service .
```

---

## Query Patterns

### Query 1: Find Network Path Between Two Applications

**Scenario**: Trace the complete network path from Application A to Application B.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?device ?device_type ?hop_number
WHERE {
  :App_OrderService :communicates_via ?path .
  ?path :routes_through ?device .
  ?device :device_type ?device_type .
  ?path :used_by :App_InventoryService .
}
ORDER BY ?hop_number
```

**Cypher Query** (Neo4j):
```cypher
MATCH (app1:Application {name: 'OrderService'})-[:COMMUNICATES_VIA]->(path:CommunicationPath)
      -[:ROUTES_THROUGH]->(device:NetworkDevice)
WHERE (path)-[:USED_BY]->(:Application {name: 'InventoryService'})
RETURN device.name AS device, 
       device.device_type AS device_type
ORDER BY device.name
```

---

### Query 2: Find All Applications Behind a Load Balancer

**Scenario**: Identify all applications exposed via a specific load balancer.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?application ?app_type ?health_status
WHERE {
  :LB_WebTier :balances_to ?target .
  ?application :runs_on ?target .
  ?application rdf:type ?app_type .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (lb:LoadBalancer {name: 'LB-WebTier'})-[:BALANCES_TO]->(target)
      <-[:RUNS_ON]-(app:Application)
RETURN app.name AS application,
       labels(app)[0] AS app_type,
       target.name AS target
```

---

### Query 3: Network Impact Analysis - Failed Router

**Scenario**: Find all communication paths affected by a failed router.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?path ?source_app ?dest_app ?protocol
WHERE {
  :Router_Core01 :lifecycle_status "failed" .
  ?path :routes_through :Router_Core01 .
  ?source_app :communicates_via ?path .
  ?path :used_by ?dest_app .
  ?path :protocol ?protocol .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (router:NetworkDevice {name: 'Router-Core01', lifecycle_status: 'failed'})
      <-[:ROUTES_THROUGH]-(path:CommunicationPath)
      <-[:COMMUNICATES_VIA]-(source_app:Application)
WHERE (path)-[:USED_BY]->(dest_app:Application)
RETURN path.name AS path,
       source_app.name AS source_app,
       dest_app.name AS dest_app,
       path.protocol AS protocol
```

---

### Query 4: Find All Network Interfaces in a Subnet

**Scenario**: List all network interfaces and their attached compute resources in a specific subnet.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?interface ?ip_address ?compute_resource ?resource_type
WHERE {
  ?interface :part_of_segment :Subnet_AppTier .
  ?interface :ip_address ?ip_address .
  ?interface :attached_to ?compute_resource .
  ?compute_resource rdf:type ?resource_type .
}
ORDER BY ?ip_address
```

**Cypher Query** (Neo4j):
```cypher
MATCH (interface:NetworkInterface)-[:PART_OF_SEGMENT]->(subnet:NetworkSegment {name: 'Subnet-AppTier'})
MATCH (interface)-[:ATTACHED_TO]->(compute)
RETURN interface.name AS interface,
       interface.ip_address AS ip_address,
       compute.name AS compute_resource,
       labels(compute)[0] AS resource_type
ORDER BY interface.ip_address
```

---

### Query 5: Load Balancer Health Check

**Scenario**: Find all load balancers with unhealthy backend targets.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?lb ?target ?health_status
WHERE {
  ?lb rdf:type :LoadBalancer .
  ?lb :balances_to ?target .
  ?target :lifecycle_status ?health_status .
  FILTER(?health_status IN ("failed", "degraded", "stopped"))
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (lb:LoadBalancer)-[r:BALANCES_TO]->(target)
WHERE target.lifecycle_status IN ['failed', 'degraded', 'stopped']
RETURN lb.name AS load_balancer,
       target.name AS target,
       target.lifecycle_status AS health_status
```

---

### Query 6: Network Bandwidth Utilization

**Scenario**: Find communication paths with high bandwidth usage.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?path ?source ?destination ?bandwidth_mbps ?protocol
WHERE {
  ?path rdf:type :CommunicationPath .
  ?path :bandwidth_mbps ?bandwidth_mbps .
  ?source :communicates_via ?path .
  ?path :used_by ?destination .
  ?path :protocol ?protocol .
  FILTER(?bandwidth_mbps > 1000)
}
ORDER BY DESC(?bandwidth_mbps)
```

**Cypher Query** (Neo4j):
```cypher
MATCH (source)-[:COMMUNICATES_VIA]->(path:CommunicationPath)-[:USED_BY]->(destination)
WHERE path.bandwidth_mbps > 1000
RETURN path.name AS path,
       source.name AS source,
       destination.name AS destination,
       path.bandwidth_mbps AS bandwidth_mbps,
       path.protocol AS protocol
ORDER BY path.bandwidth_mbps DESC
```

---

### Query 7: VPN Connectivity Status

**Scenario**: Check status of all VPN connections.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?vpn_gateway ?location ?status ?connected_to
WHERE {
  ?vpn_gateway :device_type "vpn_gateway" .
  ?vpn_gateway :location ?location .
  ?vpn_gateway :lifecycle_status ?status .
  OPTIONAL { ?vpn_gateway :connected_to ?connected_to }
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (vpn:NetworkDevice {device_type: 'vpn_gateway'})
OPTIONAL MATCH (vpn)-[:CONNECTED_TO]->(connected)
RETURN vpn.name AS vpn_gateway,
       vpn.location AS location,
       vpn.lifecycle_status AS status,
       connected.name AS connected_to
```

---

### Query 8: Find Unencrypted Communication Paths

**Scenario**: Identify communication paths that are not encrypted (security audit).

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?path ?source ?destination ?protocol
WHERE {
  ?path rdf:type :CommunicationPath .
  ?path :encrypted false .
  ?source :communicates_via ?path .
  ?path :used_by ?destination .
  ?path :protocol ?protocol .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (source)-[:COMMUNICATES_VIA]->(path:CommunicationPath {encrypted: false})-[:USED_BY]->(destination)
RETURN path.name AS path,
       source.name AS source,
       destination.name AS destination,
       path.protocol AS protocol
```

---

### Query 9: Network Device Inventory by Type

**Scenario**: Count network devices by type and location.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?device_type ?location (COUNT(?device) AS ?count)
WHERE {
  ?device rdf:type :NetworkDevice .
  ?device :device_type ?device_type .
  ?device :location ?location .
}
GROUP BY ?device_type ?location
ORDER BY ?location ?device_type
```

**Cypher Query** (Neo4j):
```cypher
MATCH (device:NetworkDevice)
RETURN device.device_type AS device_type,
       device.location AS location,
       COUNT(device) AS count
ORDER BY location, device_type
```

---

### Query 10: Full Stack Network Decomposition

**Scenario**: Trace from business process through application to network infrastructure.

**SPARQL Query**:
```sparql
PREFIX : <http://example.org/ontology#>

SELECT ?business_process ?application ?path ?device ?segment
WHERE {
  ?business_process :fulfills ?application .
  ?application :communicates_via ?path .
  ?path :routes_through ?device .
  ?device :part_of_segment ?segment .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (bp:BusinessProcess)-[:FULFILLS]->(app:Application)
      -[:COMMUNICATES_VIA]->(path:CommunicationPath)
      -[:ROUTES_THROUGH]->(device:NetworkDevice)
      -[:PART_OF_SEGMENT]->(segment:NetworkSegment)
RETURN bp.name AS business_process,
       app.name AS application,
       path.name AS path,
       device.name AS device,
       segment.name AS segment
```

---

## Framework Mappings

### CIM Network Model Mapping

| Ontology Entity Type | CIM Class | CIM Namespace |
|----------------------|-----------|---------------|
| NetworkDevice | CIM_NetworkDevice | CIM_Network |
| LoadBalancer | CIM_LoadBalancer | CIM_Network |
| NetworkInterface | CIM_NetworkPort | CIM_Network |
| NetworkSegment | CIM_NetworkSegment | CIM_Network |
| CommunicationPath | CIM_NetworkPipe | CIM_Network |
| NetworkRoute | CIM_RouteCalculationService | CIM_Network |

### TOGAF Communication Infrastructure Mapping

| Ontology Layer | TOGAF Layer | TOGAF Elements |
|----------------|-------------|----------------|
| Network Topology | Technology Architecture | Communication Infrastructure, Network Services |

### Cloud Provider Network Mapping

| Ontology Entity Type | AWS | Azure | GCP |
|----------------------|-----|-------|-----|
| NetworkSegment (VPC) | VPC | Virtual Network | VPC Network |
| NetworkSegment (Subnet) | Subnet | Subnet | Subnet |
| LoadBalancer | ELB/ALB/NLB | Load Balancer | Cloud Load Balancing |
| NetworkDevice (Gateway) | Internet Gateway, NAT Gateway | Virtual Network Gateway | Cloud Router |
| NetworkRoute | Route Table | Route Table | Routes |
| NetworkInterface | ENI (Elastic Network Interface) | NIC | Network Interface |

---

## Integration with Other Layers

### Layer 2 (Application Layer)
- **communicates_via**: Applications use communication paths for inter-service communication
- **exposes_via**: Applications exposed via load balancers for external access
- Enables application-to-network dependency tracking

### Layer 3 (Container & Orchestration)
- **attached_to**: Container network interfaces attached to pods
- **exposes_via**: Kubernetes services exposed via load balancers
- Enables container networking and service mesh modeling

### Layer 4 (Physical Infrastructure)
- **attached_to**: Network interfaces attached to VMs and physical servers
- **part_of_segment**: Infrastructure resources grouped in network segments
- Enables infrastructure-to-network connectivity modeling

### Layer 6 (Security Infrastructure)
- Network devices (firewalls) also modeled in Security layer
- Communication paths protected by security policies
- Network segments define security boundaries

---

## Statistics

| Metric | Count |
|--------|-------|
| Entity Types | 6 |
| Attributes | 90+ |
| Intra-Layer Relationships | 6 |
| Cross-Layer Relationships | 2 |
| SHACL Validation Shapes | 6 |
| Validation Rules | 6 |
| Usage Patterns | 5 |
| Query Patterns | 10 |

---

## Next Steps

1. ✅ Layer 5 entity types specified (6 entity types)
2. ✅ Layer 5 relationships defined (8 relationships)
3. ⏳ Define Layer 6: Security Infrastructure (Task 7)
4. ⏳ Create formal OWL ontology with Layer 5 definitions (Task 8)
5. ⏳ Document deployment patterns with Layer 5 examples (Task 9)
6. ⏳ Validate with sample network data (Task 12)

---

**Document Version**: 1.0
**Completion Date**: 2025-11-10
**Status**: ✅ Complete
