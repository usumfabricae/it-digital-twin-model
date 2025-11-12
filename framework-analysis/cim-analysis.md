# CIM (Common Information Model) Framework Analysis

## Overview

This document provides a comprehensive analysis of the DMTF Common Information Model (CIM) specifications, focusing on Core, Network, Storage, and Virtualization schemas. CIM provides standardized definitions for physical and virtual infrastructure components.

**CIM Version**: 2.49.0 (latest stable)
**Framework Source**: Distributed Management Task Force (DMTF)
**Analysis Date**: 2025-11-09

---

## CIM Core Schema

### Entity Types from CIM Core

#### 1. CIM_ComputerSystem

**CIM Definition**: A physical or virtual computer system representing a computing resource.

**Attributes**:
- `Name` (string, mandatory): System name or identifier
- `ElementName` (string, optional): User-friendly name
- `Description` (string, optional): System description
- `OperationalStatus` (uint16[], optional): Current operational status
- `HealthState` (uint16, optional): Health state of the system
- `EnabledState` (uint16, optional): Enabled/disabled state
- `Dedicated` (uint16[], optional): Purpose dedication (general, storage, router, etc.)
- `NameFormat` (string, optional): Format of the Name property
- `PrimaryOwnerName` (string, optional): System owner
- `PrimaryOwnerContact` (string, optional): Owner contact information

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_System
                  └─ CIM_ComputerSystem
```

**Mapped Ontology Entity**: PhysicalServer (Layer 4)

**Relationships**:
- `CIM_SystemComponent`: ComputerSystem contains components
- `CIM_HostedService`: ComputerSystem hosts services
- `CIM_RunningOS`: ComputerSystem runs operating system

---

#### 2. CIM_OperatingSystem

**CIM Definition**: An operating system running on a computer system.

**Attributes**:
- `Name` (string, mandatory): OS name
- `Version` (string, optional): OS version
- `OSType` (uint16, mandatory): Operating system type (Windows, Linux, etc.)
- `LastBootUpTime` (datetime, optional): Last boot timestamp
- `NumberOfProcesses` (uint32, optional): Current process count
- `NumberOfUsers` (uint32, optional): Current user count
- `MaxNumberOfProcesses` (uint32, optional): Maximum processes supported

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_OperatingSystem
```

**Mapped Ontology Attribute**: operating_system (Layer 4 - PhysicalServer, VirtualMachine)

---

## CIM Storage Schema

### Entity Types from CIM Storage

#### 1. CIM_StorageExtent

**CIM Definition**: A logical or physical storage extent representing allocatable storage capacity.

**Attributes**:
- `Name` (string, mandatory): Storage extent name
- `ElementName` (string, optional): User-friendly name
- `BlockSize` (uint64, optional): Block size in bytes
- `NumberOfBlocks` (uint64, optional): Total number of blocks
- `ConsumableBlocks` (uint64, optional): Available blocks
- `DataRedundancy` (uint16, optional): Redundancy level (RAID, mirroring)
- `PackageRedundancy` (uint16, optional): Package redundancy level
- `ExtentStatus` (uint16[], optional): Status of the extent
- `NoSinglePointOfFailure` (boolean, optional): SPOF indicator
- `Purpose` (string, optional): Intended purpose

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_StorageExtent
```

**Mapped Ontology Entity**: StorageVolume (Layer 4)

**Relationships**:
- `CIM_BasedOn`: StorageExtent based on other extents
- `CIM_AllocatedFromStoragePool`: Extent allocated from pool
- `CIM_RealizesDiskPartition`: Extent realizes partition

---

#### 2. CIM_StoragePool

**CIM Definition**: A logical grouping of storage capacity from which storage extents can be allocated.

**Attributes**:
- `PoolID` (string, mandatory): Unique pool identifier
- `ElementName` (string, optional): Pool name
- `TotalManagedSpace` (uint64, optional): Total capacity
- `RemainingManagedSpace` (uint64, optional): Available capacity
- `Usage` (uint16, optional): Pool usage type
- `LowSpaceWarningThreshold` (uint16, optional): Warning threshold percentage

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_ResourcePool
              └─ CIM_StoragePool
```

**Mapped Ontology Entity**: StoragePool (Layer 4)

---

#### 3. CIM_StorageVolume

**CIM Definition**: A storage volume representing a unit of storage presented to a host.

**Attributes**:
- `DeviceID` (string, mandatory): Volume device identifier
- `Name` (string, optional): Volume name
- `BlockSize` (uint64, optional): Block size
- `NumberOfBlocks` (uint64, optional): Total blocks
- `Access` (uint16, optional): Access permissions (read-only, read-write)
- `NameFormat` (uint16, optional): Format of the Name property
- `NameNamespace` (uint16, optional): Namespace for the Name

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_StorageExtent
              └─ CIM_StorageVolume
```

**Mapped Ontology Entity**: StorageVolume (Layer 4)

---

#### 4. CIM_FileSystem

**CIM Definition**: A file system providing hierarchical storage organization.

**Attributes**:
- `Name` (string, mandatory): File system name
- `Root` (string, optional): Root directory path
- `FileSystemType` (string, optional): FS type (NTFS, ext4, XFS, etc.)
- `BlockSize` (uint64, optional): Block size
- `FileSystemSize` (uint64, optional): Total size
- `AvailableSpace` (uint64, optional): Available space
- `ReadOnly` (boolean, optional): Read-only flag
- `CaseSensitive` (boolean, optional): Case sensitivity
- `CasePreserved` (boolean, optional): Case preservation

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_FileSystem
```

**Mapped Ontology Entity**: FileSystem (Layer 4)

---

## CIM Network Schema

### Entity Types from CIM Network

#### 1. CIM_NetworkDevice

**CIM Definition**: A network device such as a switch, router, or gateway.

**Attributes**:
- `SystemName` (string, mandatory): Device system name
- `ElementName` (string, optional): User-friendly name
- `Description` (string, optional): Device description
- `OperationalStatus` (uint16[], optional): Operational status
- `EnabledState` (uint16, optional): Enabled state
- `Dedicated` (uint16[], optional): Device dedication (router, switch, gateway)

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_System
                  └─ CIM_ComputerSystem
                      └─ CIM_NetworkDevice
```

**Mapped Ontology Entity**: NetworkDevice (Layer 5)

---

#### 2. CIM_NetworkPort

**CIM Definition**: A network port on a device providing network connectivity.

**Attributes**:
- `DeviceID` (string, mandatory): Port identifier
- `PortNumber` (uint16, optional): Physical port number
- `LinkTechnology` (uint16, optional): Link technology (Ethernet, Fibre Channel, etc.)
- `Speed` (uint64, optional): Port speed in bits per second
- `MaxSpeed` (uint64, optional): Maximum supported speed
- `FullDuplex` (boolean, optional): Full duplex capability
- `AutoSense` (boolean, optional): Auto-sensing capability
- `PortType` (uint16, optional): Port type

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_LogicalDevice
                  └─ CIM_LogicalPort
                      └─ CIM_NetworkPort
```

**Mapped Ontology Entity**: NetworkInterface (Layer 5)

---

#### 3. CIM_IPProtocolEndpoint

**CIM Definition**: An IP protocol endpoint representing an IP address on a network interface.

**Attributes**:
- `Name` (string, mandatory): Endpoint name
- `IPv4Address` (string, optional): IPv4 address
- `IPv6Address` (string, optional): IPv6 address
- `SubnetMask` (string, optional): Subnet mask
- `PrefixLength` (uint8, optional): IPv6 prefix length
- `AddressType` (uint16, optional): Address type (IPv4, IPv6)
- `IPVersionSupport` (uint16, optional): Supported IP versions
- `ProtocolIFType` (uint16, optional): Interface type

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_ServiceAccessPoint
              └─ CIM_ProtocolEndpoint
                  └─ CIM_IPProtocolEndpoint
```

**Mapped Ontology Attribute**: ip_address (Layer 5 - NetworkInterface, NetworkSegment)

---

#### 4. CIM_LANEndpoint

**CIM Definition**: A LAN endpoint representing a MAC address on a network interface.

**Attributes**:
- `Name` (string, mandatory): Endpoint name
- `MACAddress` (string, optional): MAC address
- `AliasAddresses` (string[], optional): Alias MAC addresses
- `GroupAddresses` (string[], optional): Multicast group addresses
- `MaxDataSize` (uint32, optional): Maximum frame size
- `LANType` (uint16, optional): LAN type (Ethernet, Token Ring, etc.)

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_ServiceAccessPoint
              └─ CIM_ProtocolEndpoint
                  └─ CIM_LANEndpoint
```

**Mapped Ontology Attribute**: mac_address (Layer 5 - NetworkInterface)

---

#### 5. CIM_NetworkPipe

**CIM Definition**: A logical network connection between two endpoints.

**Attributes**:
- `InstanceID` (string, mandatory): Unique instance identifier
- `ElementName` (string, optional): Pipe name
- `AggregationBehavior` (uint16, optional): Aggregation behavior
- `Directionality` (uint16, optional): Unidirectional or bidirectional
- `RequestedState` (uint16, optional): Requested operational state

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_NetworkPipe
```

**Mapped Ontology Entity**: CommunicationPath (Layer 5)

---

## CIM Virtualization Schema

### Entity Types from CIM Virtualization

#### 1. CIM_VirtualComputerSystem

**CIM Definition**: A virtual computer system representing a virtualized computing resource.

**Attributes**:
- `Name` (string, mandatory): VM name
- `ElementName` (string, optional): User-friendly name
- `VirtualSystemIdentifier` (string, optional): Unique VM identifier
- `VirtualSystemType` (string, optional): VM type (e.g., "DMTF:xen", "DMTF:vmware")
- `OperationalStatus` (uint16[], optional): VM operational status
- `EnabledState` (uint16, optional): VM power state
- `OnTimeInMilliseconds` (uint64, optional): Uptime in milliseconds

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_System
                  └─ CIM_ComputerSystem
                      └─ CIM_VirtualComputerSystem
```

**Mapped Ontology Entity**: VirtualMachine (Layer 4)

**Relationships**:
- `CIM_HostedDependency`: VM hosted on physical system
- `CIM_VirtualSystemSettingData`: VM configuration settings

---

#### 2. CIM_VirtualSystemSettingData

**CIM Definition**: Configuration settings for a virtual computer system.

**Attributes**:
- `InstanceID` (string, mandatory): Settings instance ID
- `ElementName` (string, optional): Settings name
- `VirtualSystemType` (string, optional): VM type
- `AutomaticStartupAction` (uint16, optional): Startup behavior
- `AutomaticShutdownAction` (uint16, optional): Shutdown behavior
- `AutomaticRecoveryAction` (uint16, optional): Recovery behavior

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_SettingData
      └─ CIM_VirtualSystemSettingData
```

**Mapped Ontology Attribute**: Configuration attributes for VirtualMachine (Layer 4)

---

#### 3. CIM_Container

**CIM Definition**: A container representing an isolated application environment.

**Attributes**:
- `Name` (string, mandatory): Container name
- `ElementName` (string, optional): User-friendly name
- `ContainerID` (string, optional): Unique container identifier
- `ImageID` (string, optional): Container image identifier
- `OperationalStatus` (uint16[], optional): Container status
- `EnabledState` (uint16, optional): Container state (running, stopped, paused)

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_System
                  └─ CIM_ComputerSystem
                      └─ CIM_Container
```

**Mapped Ontology Entity**: Container (Layer 3)

---

#### 4. CIM_ResourceAllocationSettingData

**CIM Definition**: Resource allocation settings for virtual systems (CPU, memory, storage, network).

**Attributes**:
- `InstanceID` (string, mandatory): Allocation instance ID
- `ResourceType` (uint16, mandatory): Resource type (CPU, memory, disk, network)
- `VirtualQuantity` (uint64, optional): Allocated quantity
- `Reservation` (uint64, optional): Reserved quantity
- `Limit` (uint64, optional): Maximum limit
- `Weight` (uint32, optional): Relative weight for sharing
- `AllocationUnits` (string, optional): Units of measurement

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_SettingData
      └─ CIM_ResourceAllocationSettingData
```

**Mapped Ontology Attribute**: resource_limits (Layer 3 - Container, Layer 4 - VirtualMachine)

---

## CIM Application Schema

### Entity Types from CIM Application

#### 1. CIM_ApplicationSystem

**CIM Definition**: An application system representing a software application.

**Attributes**:
- `Name` (string, mandatory): Application name
- `ElementName` (string, optional): User-friendly name
- `Description` (string, optional): Application description
- `OperationalStatus` (uint16[], optional): Application status
- `EnabledState` (uint16, optional): Application state

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_System
                  └─ CIM_ApplicationSystem
```

**Mapped Ontology Entity**: Application (Layer 2)

---

#### 2. CIM_DatabaseSystem

**CIM Definition**: A database management system.

**Attributes**:
- `Name` (string, mandatory): Database system name
- `ElementName` (string, optional): User-friendly name
- `Description` (string, optional): Database description
- `OperationalStatus` (uint16[], optional): Database status

**CIM Class Hierarchy**:
```
CIM_ManagedElement
  └─ CIM_ManagedSystemElement
      └─ CIM_LogicalElement
          └─ CIM_EnabledLogicalElement
              └─ CIM_System
                  └─ CIM_ApplicationSystem
                      └─ CIM_DatabaseSystem
```

**Mapped Ontology Entity**: Database (Layer 2)

---

## CIM Relationship Types (Associations)

### Core Relationships

| CIM Association | Source Class | Target Class | Cardinality | Description |
|-----------------|--------------|--------------|-------------|-------------|
| CIM_SystemComponent | CIM_System | CIM_ManagedSystemElement | 1-to-many | System contains components |
| CIM_HostedService | CIM_System | CIM_Service | 1-to-many | System hosts services |
| CIM_RunningOS | CIM_ComputerSystem | CIM_OperatingSystem | 1-to-1 | System runs OS |
| CIM_HostedDependency | CIM_ComputerSystem | CIM_VirtualComputerSystem | 1-to-many | Physical hosts virtual |

### Storage Relationships

| CIM Association | Source Class | Target Class | Cardinality | Description |
|-----------------|--------------|--------------|-------------|-------------|
| CIM_BasedOn | CIM_StorageExtent | CIM_StorageExtent | many-to-many | Extent layering |
| CIM_AllocatedFromStoragePool | CIM_StorageExtent | CIM_StoragePool | many-to-1 | Extent from pool |
| CIM_HostedFileSystem | CIM_ComputerSystem | CIM_FileSystem | 1-to-many | System hosts filesystem |

### Network Relationships

| CIM Association | Source Class | Target Class | Cardinality | Description |
|-----------------|--------------|--------------|-------------|-------------|
| CIM_NetworkPortOnDevice | CIM_NetworkDevice | CIM_NetworkPort | 1-to-many | Device has ports |
| CIM_BindsTo | CIM_ProtocolEndpoint | CIM_ServiceAccessPoint | many-to-many | Protocol binding |
| CIM_DeviceSAPImplementation | CIM_LogicalDevice | CIM_ServiceAccessPoint | 1-to-many | Device implements SAP |

---

## CIM Data Types and Enumerations

### OperationalStatus (uint16[])
- `0`: Unknown
- `1`: Other
- `2`: OK
- `3`: Degraded
- `4`: Stressed
- `5`: Predictive Failure
- `6`: Error
- `7`: Non-Recoverable Error
- `8`: Starting
- `9`: Stopping
- `10`: Stopped
- `11`: In Service
- `12`: No Contact
- `13`: Lost Communication
- `14`: Aborted
- `15`: Dormant
- `16`: Supporting Entity in Error
- `17`: Completed
- `18`: Power Mode

### EnabledState (uint16)
- `0`: Unknown
- `1`: Other
- `2`: Enabled
- `3`: Disabled
- `4`: Shutting Down
- `5`: Not Applicable
- `6`: Enabled but Offline
- `7`: In Test
- `8`: Deferred
- `9`: Quiesce
- `10`: Starting

### HealthState (uint16)
- `0`: Unknown
- `5`: OK
- `10`: Degraded/Warning
- `15`: Minor failure
- `20`: Major failure
- `25`: Critical failure
- `30`: Non-recoverable error

---

## Mapping to Ontology Layers

### Layer 2: Application Layer

| Ontology Entity | CIM Class | Attribute Mapping |
|-----------------|-----------|-------------------|
| Application | CIM_ApplicationSystem | name, description, lifecycle_status |
| Database | CIM_DatabaseSystem | name, description, lifecycle_status |

### Layer 3: Container and Orchestration

| Ontology Entity | CIM Class | Attribute Mapping |
|-----------------|-----------|-------------------|
| Container | CIM_Container | name, image_name, lifecycle_status |

### Layer 4: Physical Infrastructure

| Ontology Entity | CIM Class | Attribute Mapping |
|-----------------|-----------|-------------------|
| PhysicalServer | CIM_ComputerSystem | name, operating_system, capacity, lifecycle_status |
| VirtualMachine | CIM_VirtualComputerSystem | name, operating_system, capacity, lifecycle_status |
| StorageArray | CIM_StorageExtent (physical) | name, capacity |
| StorageVolume | CIM_StorageVolume | name, capacity |
| FileSystem | CIM_FileSystem | name, filesystem type |
| StoragePool | CIM_StoragePool | name, capacity |

### Layer 5: Network Topology

| Ontology Entity | CIM Class | Attribute Mapping |
|-----------------|-----------|-------------------|
| NetworkDevice | CIM_NetworkDevice | name, device_type, lifecycle_status |
| NetworkInterface | CIM_NetworkPort | name, port, bandwidth |
| CommunicationPath | CIM_NetworkPipe | name, protocol |

---

## Key Insights for Ontology Design

### 1. Comprehensive Infrastructure Coverage
CIM provides detailed models for physical infrastructure, storage, network, and virtualization - ideal for Layer 4 and Layer 5.

### 2. Standardized Attributes
CIM defines standard attributes like OperationalStatus, EnabledState, and HealthState that map well to lifecycle_status in the ontology.

### 3. Class Hierarchy
CIM's class hierarchy (ManagedElement → ManagedSystemElement → LogicalElement) provides inheritance patterns for the ontology.

### 4. Resource Allocation
CIM_ResourceAllocationSettingData provides detailed resource allocation attributes for containers and VMs.

### 5. Association Patterns
CIM associations (HostedDependency, BasedOn, AllocatedFrom) provide relationship patterns for cross-layer dependencies.

---

## References

- DMTF, "Common Information Model (CIM) Standards"
- DMTF, "CIM Schema Version 2.49.0"
- DMTF, "CIM Core Model White Paper"
- DMTF, "CIM Network Model White Paper"
- DMTF, "CIM Storage Model White Paper"

---

## Conclusion

CIM provides a comprehensive, standardized model for IT infrastructure components, particularly for physical infrastructure (Layer 4) and network topology (Layer 5). The framework's detailed attribute definitions, class hierarchies, and association patterns make it an ideal foundation for the ontology's infrastructure layers.

**Key Contributions to Ontology**:
- Physical infrastructure entity types: PhysicalServer, VirtualMachine, StorageArray, StorageVolume, FileSystem
- Network entity types: NetworkDevice, NetworkPort, IPProtocolEndpoint
- Container entity types: Container
- Core attributes: name, operational_status, enabled_state, health_state, capacity
- Relationship patterns: hosted_on, allocated_from, based_on
- Enumeration values for operational status and health state
