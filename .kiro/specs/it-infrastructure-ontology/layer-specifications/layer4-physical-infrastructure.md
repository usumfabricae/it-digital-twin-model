# Layer 4: Physical Infrastructure - Complete Specification

## Overview

This document provides the complete formal specification for Layer 4 (Physical Infrastructure) of the IT Infrastructure and Application Dependency Ontology. The Physical Infrastructure layer represents physical and virtual compute, storage, and infrastructure resources that host applications and containers.

**Layer Purpose**: Represents physical and virtual compute, storage, and infrastructure resources.

**Layer Scope**: All physical and virtual infrastructure including servers, virtual machines, hypervisors, storage arrays, storage volumes, file systems, and cloud infrastructure services. This layer provides the foundation for hosting applications and containers.

**Framework Sources**: 
- CIM (Common Information Model) - Core, Storage, Virtualization schemas
- AWS API specifications (EC2, EBS, RDS, S3)
- Azure API specifications (Virtual Machines, Managed Disks, SQL Database, Blob Storage)
- GCP API specifications (Compute Engine, Persistent Disk, Cloud SQL, Cloud Storage)
- VMware vSphere API
- TOGAF Technology Architecture

**Key Characteristics**:
- Foundation layer for compute and storage resources
- Supports both on-premises and cloud infrastructure
- Distinguishes between physical, virtual, and cloud resources
- Provides storage abstraction from logical to physical

---

## Entity Type Specifications

### 1. PhysicalServer

**Definition**: A physical server machine in a datacenter.

**OWL Class Definition**:
```turtle
:PhysicalServer
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Physical Server" ;
  rdfs:comment "A physical server machine" ;
  skos:definition "A physical server is a bare-metal computer system that provides compute resources" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Server name or hostname |
| serial_number | xsd:string | 0..1 | optional | CIM | Hardware serial number |
| manufacturer | xsd:string | 0..1 | optional | CIM | Hardware manufacturer (e.g., "Dell", "HP", "Cisco") |
| model | xsd:string | 0..1 | optional | CIM | Hardware model number |
| resource_type | xsd:string | 1..1 | enum | CIM | Always "physical" for PhysicalServer |
| location | xsd:string | 1..1 | mandatory | CIM | Datacenter location (e.g., "DC1-Rack05-U12") |
| datacenter | xsd:string | 0..1 | optional | Custom | Datacenter name |
| rack_position | xsd:string | 0..1 | optional | Custom | Rack and unit position |
| cpu_count | xsd:integer | 0..1 | optional | CIM | Number of physical CPUs |
| cpu_cores | xsd:integer | 0..1 | optional | CIM | Total number of CPU cores |
| cpu_model | xsd:string | 0..1 | optional | CIM | CPU model name |
| memory_gb | xsd:decimal | 0..1 | optional | CIM | Total RAM in gigabytes |
| operating_system | xsd:string | 0..1 | optional | CIM | OS name and version |
| os_version | xsd:string | 0..1 | optional | CIM | OS version number |
| ip_address | xsd:string | 0..1 | optional | CIM | Primary IP address |
| mac_address | xsd:string | 0..1 | optional | CIM | Primary MAC address |
| power_state | xsd:string | 0..1 | enum | CIM | Power state: on, off, standby, hibernate |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Operational state: active, maintenance, failed, decommissioned |

**Enumeration Values**:
- **resource_type**: `physical` (fixed value)
- **power_state**: `on`, `off`, `standby`, `hibernate`
- **lifecycle_status**: `active`, `maintenance`, `failed`, `decommissioned`, `provisioning`

**SHACL Validation Shape**:
```turtle
:PhysicalServerShape
  a sh:NodeShape ;
  sh:targetClass :PhysicalServer ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "physical" ;
  ] ;
  sh:property [
    sh:path :location ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :power_state ;
    sh:maxCount 1 ;
    sh:in ( "on" "off" "standby" "hibernate" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "maintenance" "failed" "decommissioned" "provisioning" ) ;
  ] .
```

---

### 2. VirtualMachine

**Definition**: A virtualized server instance running on a hypervisor.

**OWL Class Definition**:
```turtle
:VirtualMachine
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Virtual Machine" ;
  rdfs:comment "A virtualized server instance" ;
  skos:definition "A virtual machine is a software emulation of a physical computer system" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | VM name or hostname |
| vm_id | xsd:string | 0..1 | optional | CIM | Unique VM identifier (UUID) |
| resource_type | xsd:string | 1..1 | enum | CIM | Always "virtual" for VirtualMachine |
| location | xsd:string | 1..1 | mandatory | CIM | Datacenter or region location |
| vcpu_count | xsd:integer | 0..1 | optional | CIM | Number of virtual CPUs |
| memory_gb | xsd:decimal | 0..1 | optional | CIM | Allocated RAM in gigabytes |
| disk_gb | xsd:decimal | 0..1 | optional | CIM | Total disk capacity in gigabytes |
| operating_system | xsd:string | 0..1 | optional | CIM | Guest OS name and version |
| os_version | xsd:string | 0..1 | optional | CIM | Guest OS version number |
| ip_address | xsd:string | 0..1 | optional | CIM | Primary IP address |
| mac_address | xsd:string | 0..1 | optional | CIM | Primary MAC address |
| vm_tools_status | xsd:string | 0..1 | enum | VMware | VM tools status: running, not_running, not_installed |
| power_state | xsd:string | 0..1 | enum | CIM | Power state: on, off, suspended |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Operational state: running, stopped, suspended, failed, terminated |

**Enumeration Values**:
- **resource_type**: `virtual` (fixed value)
- **vm_tools_status**: `running`, `not_running`, `not_installed`
- **power_state**: `on`, `off`, `suspended`
- **lifecycle_status**: `running`, `stopped`, `suspended`, `failed`, `terminated`, `provisioning`

**SHACL Validation Shape**:
```turtle
:VirtualMachineShape
  a sh:NodeShape ;
  sh:targetClass :VirtualMachine ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "virtual" ;
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
    sh:in ( "running" "stopped" "suspended" "failed" "terminated" "provisioning" ) ;
  ] .
```

---

### 3. Hypervisor

**Definition**: A virtualization platform that manages virtual machines.

**OWL Class Definition**:
```turtle
:Hypervisor
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Hypervisor" ;
  rdfs:comment "A virtualization platform" ;
  skos:definition "A hypervisor is software that creates and manages virtual machines on physical hardware" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Hypervisor name or hostname |
| hypervisor_type | xsd:string | 1..1 | enum | CIM | Hypervisor type: vmware_esxi, hyper_v, kvm, xen, virtualbox |
| version | xsd:string | 1..1 | mandatory | CIM | Hypervisor version |
| resource_type | xsd:string | 1..1 | enum | CIM | Always "virtual" for Hypervisor |
| location | xsd:string | 1..1 | mandatory | CIM | Datacenter location |
| total_cpu_cores | xsd:integer | 0..1 | optional | CIM | Total physical CPU cores |
| total_memory_gb | xsd:decimal | 0..1 | optional | CIM | Total physical RAM in gigabytes |
| allocated_cpu_cores | xsd:integer | 0..1 | optional | CIM | Allocated CPU cores to VMs |
| allocated_memory_gb | xsd:decimal | 0..1 | optional | CIM | Allocated RAM to VMs in gigabytes |
| vm_count | xsd:integer | 0..1 | optional | CIM | Number of VMs hosted |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Operational state: active, maintenance, failed, disconnected |

**Enumeration Values**:
- **hypervisor_type**: `vmware_esxi`, `hyper_v`, `kvm`, `xen`, `virtualbox`, `proxmox`
- **resource_type**: `virtual` (fixed value)
- **lifecycle_status**: `active`, `maintenance`, `failed`, `disconnected`

**SHACL Validation Shape**:
```turtle
:HypervisorShape
  a sh:NodeShape ;
  sh:targetClass :Hypervisor ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :hypervisor_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "vmware_esxi" "hyper_v" "kvm" "xen" "virtualbox" "proxmox" ) ;
  ] ;
  sh:property [
    sh:path :version ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "maintenance" "failed" "disconnected" ) ;
  ] .
```

---

### 4. CloudInstance

**Definition**: A cloud provider compute instance (EC2, Azure VM, GCE).

**OWL Class Definition**:
```turtle
:CloudInstance
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Cloud Instance" ;
  rdfs:comment "A cloud provider compute instance" ;
  skos:definition "A cloud instance is a virtual server provided by a cloud service provider" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Instance name or identifier |
| instance_id | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Cloud provider instance ID |
| resource_type | xsd:string | 1..1 | enum | Custom | Always "cloud_iaas" for CloudInstance |
| cloud_provider | xsd:string | 1..1 | enum | Custom | Provider: aws, azure, gcp, alibaba, oracle |
| instance_type | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Instance type/size (e.g., "t3.medium", "Standard_D2s_v3") |
| region | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Cloud region (e.g., "us-east-1", "eastus") |
| availability_zone | xsd:string | 0..1 | optional | AWS/Azure/GCP | Availability zone |
| vcpu_count | xsd:integer | 0..1 | optional | AWS/Azure/GCP | Number of virtual CPUs |
| memory_gb | xsd:decimal | 0..1 | optional | AWS/Azure/GCP | RAM in gigabytes |
| operating_system | xsd:string | 0..1 | optional | AWS/Azure/GCP | OS name and version |
| platform | xsd:string | 0..1 | enum | AWS/Azure/GCP | Platform: linux, windows |
| public_ip | xsd:string | 0..1 | optional | AWS/Azure/GCP | Public IP address |
| private_ip | xsd:string | 0..1 | optional | AWS/Azure/GCP | Private IP address |
| vpc_id | xsd:string | 0..1 | optional | AWS/Azure/GCP | VPC/VNet identifier |
| subnet_id | xsd:string | 0..1 | optional | AWS/Azure/GCP | Subnet identifier |
| launch_time | xsd:dateTime | 0..1 | optional | AWS/Azure/GCP | Instance launch timestamp |
| lifecycle_status | xsd:string | 1..1 | enum | AWS/Azure/GCP | Instance state: pending, running, stopping, stopped, terminated |

**Enumeration Values**:
- **resource_type**: `cloud_iaas` (fixed value)
- **cloud_provider**: `aws`, `azure`, `gcp`, `alibaba`, `oracle`, `ibm`
- **platform**: `linux`, `windows`
- **lifecycle_status**: `pending`, `running`, `stopping`, `stopped`, `terminated`, `shutting_down`

**SHACL Validation Shape**:
```turtle
:CloudInstanceShape
  a sh:NodeShape ;
  sh:targetClass :CloudInstance ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :instance_id ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "cloud_iaas" ;
  ] ;
  sh:property [
    sh:path :cloud_provider ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "aws" "azure" "gcp" "alibaba" "oracle" "ibm" ) ;
  ] ;
  sh:property [
    sh:path :instance_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :region ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "pending" "running" "stopping" "stopped" "terminated" "shutting_down" ) ;
  ] .
```

---

### 5. CloudService

**Definition**: A managed cloud service (RDS, Lambda, Azure SQL, Cloud Functions, etc.).

**OWL Class Definition**:
```turtle
:CloudService
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Cloud Service" ;
  rdfs:comment "A managed cloud service" ;
  skos:definition "A cloud service is a fully managed platform or software service provided by a cloud provider" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Service name or identifier |
| service_id | xsd:string | 0..1 | optional | AWS/Azure/GCP | Cloud provider service ID |
| resource_type | xsd:string | 1..1 | enum | Custom | Service type: cloud_paas, cloud_saas |
| cloud_provider | xsd:string | 1..1 | enum | Custom | Provider: aws, azure, gcp, alibaba, oracle |
| service_type | xsd:string | 1..1 | enum | Custom | Service category: database, compute, storage, messaging, analytics |
| service_name | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Service name (e.g., "RDS", "Lambda", "Azure SQL") |
| region | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Cloud region |
| tier | xsd:string | 0..1 | optional | AWS/Azure/GCP | Service tier or plan |
| endpoint | xsd:anyURI | 0..1 | optional | AWS/Azure/GCP | Service endpoint URL |
| lifecycle_status | xsd:string | 1..1 | enum | AWS/Azure/GCP | Service state: available, creating, deleting, failed, maintenance |

**Enumeration Values**:
- **resource_type**: `cloud_paas`, `cloud_saas`
- **cloud_provider**: `aws`, `azure`, `gcp`, `alibaba`, `oracle`, `ibm`
- **service_type**: `database`, `compute`, `storage`, `messaging`, `analytics`, `ml`, `iot`
- **lifecycle_status**: `available`, `creating`, `deleting`, `failed`, `maintenance`, `modifying`

**SHACL Validation Shape**:
```turtle
:CloudServiceShape
  a sh:NodeShape ;
  sh:targetClass :CloudService ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "cloud_paas" "cloud_saas" ) ;
  ] ;
  sh:property [
    sh:path :cloud_provider ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "aws" "azure" "gcp" "alibaba" "oracle" "ibm" ) ;
  ] ;
  sh:property [
    sh:path :service_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "database" "compute" "storage" "messaging" "analytics" "ml" "iot" ) ;
  ] ;
  sh:property [
    sh:path :service_name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :region ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "available" "creating" "deleting" "failed" "maintenance" "modifying" ) ;
  ] .
```

---

## Storage Infrastructure Entity Types

### 6. StorageArray

**Definition**: A physical storage system (SAN, NAS) providing storage capacity.

**OWL Class Definition**:
```turtle
:StorageArray
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Storage Array" ;
  rdfs:comment "A physical storage system" ;
  skos:definition "A storage array is a hardware device that provides centralized storage capacity" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Storage array name |
| serial_number | xsd:string | 0..1 | optional | CIM | Hardware serial number |
| manufacturer | xsd:string | 0..1 | optional | CIM | Manufacturer (e.g., "NetApp", "EMC", "HPE") |
| model | xsd:string | 0..1 | optional | CIM | Hardware model |
| array_type | xsd:string | 1..1 | enum | CIM | Array type: san, nas, das, hybrid |
| resource_type | xsd:string | 1..1 | enum | CIM | Always "physical" for StorageArray |
| location | xsd:string | 1..1 | mandatory | CIM | Datacenter location |
| total_capacity_tb | xsd:decimal | 0..1 | optional | CIM | Total capacity in terabytes |
| used_capacity_tb | xsd:decimal | 0..1 | optional | CIM | Used capacity in terabytes |
| available_capacity_tb | xsd:decimal | 0..1 | optional | CIM | Available capacity in terabytes |
| raid_level | xsd:string | 0..1 | optional | CIM | RAID configuration (e.g., "RAID5", "RAID10") |
| protocol | xsd:string | 0..* | optional | CIM | Storage protocols (e.g., "iSCSI", "FC", "NFS", "CIFS") |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Operational state: active, maintenance, failed, decommissioned |

**Enumeration Values**:
- **array_type**: `san`, `nas`, `das`, `hybrid`
- **resource_type**: `physical` (fixed value)
- **lifecycle_status**: `active`, `maintenance`, `failed`, `decommissioned`, `degraded`

**SHACL Validation Shape**:
```turtle
:StorageArrayShape
  a sh:NodeShape ;
  sh:targetClass :StorageArray ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :array_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "san" "nas" "das" "hybrid" ) ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "physical" ;
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
    sh:in ( "active" "maintenance" "failed" "decommissioned" "degraded" ) ;
  ] .
```

---

### 7. StorageVolume

**Definition**: A logical storage volume or LUN allocated from a storage array.

**OWL Class Definition**:
```turtle
:StorageVolume
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Storage Volume" ;
  rdfs:comment "A logical storage volume or LUN" ;
  skos:definition "A storage volume is a logical unit of storage allocated from a storage array or pool" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Volume name or identifier |
| volume_id | xsd:string | 0..1 | optional | CIM | Unique volume identifier |
| volume_type | xsd:string | 1..1 | enum | CIM | Volume type: lun, logical_volume, block_volume |
| resource_type | xsd:string | 1..1 | enum | CIM | Resource type: physical, virtual, cloud_iaas |
| capacity_gb | xsd:decimal | 1..1 | mandatory | CIM | Volume capacity in gigabytes |
| used_capacity_gb | xsd:decimal | 0..1 | optional | CIM | Used capacity in gigabytes |
| volume_format | xsd:string | 0..1 | optional | CIM | Volume format (e.g., "raw", "qcow2", "vmdk") |
| thin_provisioned | xsd:boolean | 0..1 | optional | CIM | Whether volume is thin provisioned |
| encrypted | xsd:boolean | 0..1 | optional | CIM | Whether volume is encrypted |
| iops | xsd:integer | 0..1 | optional | AWS/Azure | Provisioned IOPS |
| throughput_mbps | xsd:integer | 0..1 | optional | AWS/Azure | Throughput in MB/s |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Volume state: available, in_use, creating, deleting, error |

**Enumeration Values**:
- **volume_type**: `lun`, `logical_volume`, `block_volume`, `persistent_volume`
- **resource_type**: `physical`, `virtual`, `cloud_iaas`
- **lifecycle_status**: `available`, `in_use`, `creating`, `deleting`, `error`, `attaching`, `detaching`

**SHACL Validation Shape**:
```turtle
:StorageVolumeShape
  a sh:NodeShape ;
  sh:targetClass :StorageVolume ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :volume_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "lun" "logical_volume" "block_volume" "persistent_volume" ) ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "physical" "virtual" "cloud_iaas" ) ;
  ] ;
  sh:property [
    sh:path :capacity_gb ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:decimal ;
    sh:minExclusive 0 ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "available" "in_use" "creating" "deleting" "error" "attaching" "detaching" ) ;
  ] .
```

---

### 8. FileSystem

**Definition**: A mounted file system (NFS, CIFS, ext4, NTFS).

**OWL Class Definition**:
```turtle
:FileSystem
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "File System" ;
  rdfs:comment "A mounted file system" ;
  skos:definition "A file system provides hierarchical file storage with directories and files" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | File system name or mount point |
| mount_point | xsd:string | 0..1 | optional | CIM | Mount point path (e.g., "/mnt/data") |
| filesystem_type | xsd:string | 1..1 | enum | CIM | File system type: nfs, cifs, ext4, ntfs, xfs, zfs |
| resource_type | xsd:string | 1..1 | enum | CIM | Resource type: physical, virtual, cloud_iaas |
| capacity_gb | xsd:decimal | 0..1 | optional | CIM | Total capacity in gigabytes |
| used_capacity_gb | xsd:decimal | 0..1 | optional | CIM | Used capacity in gigabytes |
| available_capacity_gb | xsd:decimal | 0..1 | optional | CIM | Available capacity in gigabytes |
| read_only | xsd:boolean | 0..1 | optional | CIM | Whether file system is read-only |
| mount_options | xsd:string | 0..1 | optional | CIM | Mount options |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | File system state: mounted, unmounted, error, maintenance |

**Enumeration Values**:
- **filesystem_type**: `nfs`, `cifs`, `smb`, `ext4`, `ntfs`, `xfs`, `zfs`, `btrfs`
- **resource_type**: `physical`, `virtual`, `cloud_iaas`
- **lifecycle_status**: `mounted`, `unmounted`, `error`, `maintenance`, `mounting`

**SHACL Validation Shape**:
```turtle
:FileSystemShape
  a sh:NodeShape ;
  sh:targetClass :FileSystem ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :filesystem_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "nfs" "cifs" "smb" "ext4" "ntfs" "xfs" "zfs" "btrfs" ) ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "physical" "virtual" "cloud_iaas" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "mounted" "unmounted" "error" "maintenance" "mounting" ) ;
  ] .
```

---

### 9. StoragePool

**Definition**: A logical grouping of storage resources.

**OWL Class Definition**:
```turtle
:StoragePool
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Storage Pool" ;
  rdfs:comment "A logical grouping of storage resources" ;
  skos:definition "A storage pool aggregates physical storage into a logical unit for allocation" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Storage pool name |
| pool_id | xsd:string | 0..1 | optional | CIM | Unique pool identifier |
| pool_type | xsd:string | 1..1 | enum | CIM | Pool type: thin, thick, dedup, compressed |
| resource_type | xsd:string | 1..1 | enum | CIM | Resource type: physical, virtual, cloud_iaas |
| total_capacity_tb | xsd:decimal | 0..1 | optional | CIM | Total capacity in terabytes |
| used_capacity_tb | xsd:decimal | 0..1 | optional | CIM | Used capacity in terabytes |
| available_capacity_tb | xsd:decimal | 0..1 | optional | CIM | Available capacity in terabytes |
| oversubscription_ratio | xsd:decimal | 0..1 | optional | CIM | Oversubscription ratio (e.g., 2.0 for 2:1) |
| deduplication_enabled | xsd:boolean | 0..1 | optional | CIM | Whether deduplication is enabled |
| compression_enabled | xsd:boolean | 0..1 | optional | CIM | Whether compression is enabled |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Pool state: active, degraded, failed, maintenance |

**Enumeration Values**:
- **pool_type**: `thin`, `thick`, `dedup`, `compressed`, `hybrid`
- **resource_type**: `physical`, `virtual`, `cloud_iaas`
- **lifecycle_status**: `active`, `degraded`, `failed`, `maintenance`, `creating`

**SHACL Validation Shape**:
```turtle
:StoragePoolShape
  a sh:NodeShape ;
  sh:targetClass :StoragePool ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :pool_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "thin" "thick" "dedup" "compressed" "hybrid" ) ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "physical" "virtual" "cloud_iaas" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "degraded" "failed" "maintenance" "creating" ) ;
  ] .
```

---

### 10. CloudStorageService

**Definition**: A managed cloud storage service (RDS, EBS, Azure Disk, Cloud SQL).

**OWL Class Definition**:
```turtle
:CloudStorageService
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Cloud Storage Service" ;
  rdfs:comment "A managed cloud storage service" ;
  skos:definition "A cloud storage service provides managed storage capacity from a cloud provider" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Storage service name |
| service_id | xsd:string | 0..1 | optional | AWS/Azure/GCP | Cloud provider service ID |
| resource_type | xsd:string | 1..1 | enum | Custom | Always "cloud_paas" for managed storage |
| cloud_provider | xsd:string | 1..1 | enum | Custom | Provider: aws, azure, gcp, alibaba, oracle |
| storage_type | xsd:string | 1..1 | enum | AWS/Azure/GCP | Storage type: block, file, object, database |
| service_name | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Service name (e.g., "EBS", "RDS", "Azure Disk") |
| region | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Cloud region |
| capacity_gb | xsd:decimal | 0..1 | optional | AWS/Azure/GCP | Allocated capacity in gigabytes |
| storage_class | xsd:string | 0..1 | optional | AWS/Azure/GCP | Storage class or tier |
| iops | xsd:integer | 0..1 | optional | AWS/Azure | Provisioned IOPS |
| throughput_mbps | xsd:integer | 0..1 | optional | AWS/Azure | Throughput in MB/s |
| encrypted | xsd:boolean | 0..1 | optional | AWS/Azure/GCP | Whether storage is encrypted |
| lifecycle_status | xsd:string | 1..1 | enum | AWS/Azure/GCP | Service state: available, creating, deleting, failed, maintenance |

**Enumeration Values**:
- **resource_type**: `cloud_paas` (fixed value)
- **cloud_provider**: `aws`, `azure`, `gcp`, `alibaba`, `oracle`, `ibm`
- **storage_type**: `block`, `file`, `object`, `database`
- **lifecycle_status**: `available`, `creating`, `deleting`, `failed`, `maintenance`, `modifying`

**SHACL Validation Shape**:
```turtle
:CloudStorageServiceShape
  a sh:NodeShape ;
  sh:targetClass :CloudStorageService ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "cloud_paas" ;
  ] ;
  sh:property [
    sh:path :cloud_provider ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "aws" "azure" "gcp" "alibaba" "oracle" "ibm" ) ;
  ] ;
  sh:property [
    sh:path :storage_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "block" "file" "object" "database" ) ;
  ] ;
  sh:property [
    sh:path :service_name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :region ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "available" "creating" "deleting" "failed" "maintenance" "modifying" ) ;
  ] .
```

---

### 11. ObjectStorageBucket

**Definition**: A physical object storage bucket (S3, Azure Blob, GCS).

**OWL Class Definition**:
```turtle
:ObjectStorageBucket
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
  rdfs:label "Object Storage Bucket" ;
  rdfs:comment "A physical object storage bucket" ;
  skos:definition "An object storage bucket provides flat namespace storage for objects with key-value access" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Bucket name |
| bucket_id | xsd:string | 0..1 | optional | AWS/Azure/GCP | Unique bucket identifier |
| resource_type | xsd:string | 1..1 | enum | Custom | Resource type: cloud_iaas, cloud_paas |
| cloud_provider | xsd:string | 1..1 | enum | Custom | Provider: aws, azure, gcp, alibaba, oracle |
| region | xsd:string | 1..1 | mandatory | AWS/Azure/GCP | Cloud region |
| storage_class | xsd:string | 0..1 | enum | AWS/Azure/GCP | Storage class: standard, infrequent_access, glacier, archive |
| versioning_enabled | xsd:boolean | 0..1 | optional | AWS/Azure/GCP | Whether versioning is enabled |
| encryption_enabled | xsd:boolean | 0..1 | optional | AWS/Azure/GCP | Whether encryption is enabled |
| public_access | xsd:boolean | 0..1 | optional | AWS/Azure/GCP | Whether public access is allowed |
| total_objects | xsd:integer | 0..1 | optional | AWS/Azure/GCP | Total number of objects |
| total_size_gb | xsd:decimal | 0..1 | optional | AWS/Azure/GCP | Total size in gigabytes |
| lifecycle_status | xsd:string | 1..1 | enum | AWS/Azure/GCP | Bucket state: active, creating, deleting, error |

**Enumeration Values**:
- **resource_type**: `cloud_iaas`, `cloud_paas`
- **cloud_provider**: `aws`, `azure`, `gcp`, `alibaba`, `oracle`, `ibm`
- **storage_class**: `standard`, `infrequent_access`, `glacier`, `archive`, `intelligent_tiering`
- **lifecycle_status**: `active`, `creating`, `deleting`, `error`

**SHACL Validation Shape**:
```turtle
:ObjectStorageBucketShape
  a sh:NodeShape ;
  sh:targetClass :ObjectStorageBucket ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :resource_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "cloud_iaas" "cloud_paas" ) ;
  ] ;
  sh:property [
    sh:path :cloud_provider ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "aws" "azure" "gcp" "alibaba" "oracle" "ibm" ) ;
  ] ;
  sh:property [
    sh:path :region ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :storage_class ;
    sh:maxCount 1 ;
    sh:in ( "standard" "infrequent_access" "glacier" "archive" "intelligent_tiering" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "creating" "deleting" "error" ) ;
  ] .
```

---

## Physical Infrastructure Layer Relationships

### Intra-Layer Relationships (within Physical Infrastructure Layer)

#### 1. runs_on (VM → Hypervisor)

**Definition**: A virtual machine runs on a hypervisor.

**OWL Property Definition**:
```turtle
:runs_on
  rdf:type owl:ObjectProperty ;
  rdfs:domain :VirtualMachine ;
  rdfs:range :Hypervisor ;
  rdfs:label "runs on" ;
  rdfs:comment "A virtual machine runs on a hypervisor" .
```

**Cardinality**: Many VMs to 1 Hypervisor (*..1)

**Inverse Property**: `hosts`

**Semantic Rules**:
- Every VM MUST run on exactly one hypervisor
- A hypervisor can host multiple VMs
- VM migration changes this relationship

**Usage Example**:
```turtle
:VM_WebServer01 :runs_on :Hypervisor_ESXi_Host05 .
```

---

#### 2. hosted_on (Hypervisor → PhysicalServer)

**Definition**: A hypervisor is hosted on a physical server.

**OWL Property Definition**:
```turtle
:hosted_on
  rdf:type owl:ObjectProperty ;
  rdfs:domain :Hypervisor ;
  rdfs:range :PhysicalServer ;
  rdfs:label "hosted on" ;
  rdfs:comment "A hypervisor is hosted on a physical server" .
```

**Cardinality**: 1 Hypervisor to 1 PhysicalServer (1..1)

**Inverse Property**: `hosts_hypervisor`

**Semantic Rules**:
- Every hypervisor MUST be hosted on exactly one physical server
- A physical server typically hosts one hypervisor instance
- This relationship links virtualization to physical hardware

**Usage Example**:
```turtle
:Hypervisor_ESXi_Host05 :hosted_on :PhysicalServer_Dell_R740_12 .
```

---

#### 3. allocated_from (StorageVolume → StorageArray/StoragePool)

**Definition**: A storage volume is allocated from a storage array or storage pool.

**OWL Property Definition**:
```turtle
:allocated_from
  rdf:type owl:ObjectProperty ;
  rdfs:domain :StorageVolume ;
  rdfs:range [ owl:unionOf ( :StorageArray :StoragePool ) ] ;
  rdfs:label "allocated from" ;
  rdfs:comment "A storage volume is allocated from a storage array or pool" .
```

**Cardinality**: Many Volumes to 1 Array/Pool (*..1)

**Inverse Property**: `allocates`

**Semantic Rules**:
- Every volume MUST be allocated from exactly one storage array or pool
- Multiple volumes can be allocated from the same array/pool
- This relationship tracks storage capacity allocation

**Usage Example**:
```turtle
:Volume_LUN_456 :allocated_from :StorageArray_NetApp_SAN01 .
:Volume_PV_789 :allocated_from :StoragePool_ThinPool01 .
```

---

#### 4. part_of (StoragePool → StorageArray)

**Definition**: A storage pool is part of a storage array.

**OWL Property Definition**:
```turtle
:part_of
  rdf:type owl:ObjectProperty ;
  rdfs:domain :StoragePool ;
  rdfs:range :StorageArray ;
  rdfs:label "part of" ;
  rdfs:comment "A storage pool is part of a storage array" .
```

**Cardinality**: Many Pools to 1 Array (*..1)

**Inverse Property**: `contains_pool`

**Semantic Rules**:
- A storage pool MAY belong to a storage array
- Multiple pools can be part of the same array
- This relationship models storage hierarchy

**Usage Example**:
```turtle
:StoragePool_ThinPool01 :part_of :StorageArray_NetApp_SAN01 .
```

---

#### 5. mounted_from (FileSystem → StorageVolume)

**Definition**: A file system is mounted from a storage volume.

**OWL Property Definition**:
```turtle
:mounted_from
  rdf:type owl:ObjectProperty ;
  rdfs:domain :FileSystem ;
  rdfs:range :StorageVolume ;
  rdfs:label "mounted from" ;
  rdfs:comment "A file system is mounted from a storage volume" .
```

**Cardinality**: Many FileSystems to 1 Volume (*..1)

**Inverse Property**: `provides_filesystem`

**Semantic Rules**:
- A file system MUST be mounted from exactly one storage volume
- Multiple file systems can be mounted from the same volume (partitions)
- This relationship links file systems to underlying storage

**Usage Example**:
```turtle
:FileSystem_NFS_MediaStorage :mounted_from :Volume_LUN_789 .
```

---

#### 6. attached_to (StorageVolume → VirtualMachine/PhysicalServer/CloudInstance)

**Definition**: A storage volume is attached to a compute resource.

**OWL Property Definition**:
```turtle
:attached_to
  rdf:type owl:ObjectProperty ;
  rdfs:domain :StorageVolume ;
  rdfs:range [ owl:unionOf ( :VirtualMachine :PhysicalServer :CloudInstance ) ] ;
  rdfs:label "attached to" ;
  rdfs:comment "A storage volume is attached to a compute resource" .
```

**Cardinality**: Many Volumes to 1 Compute (*..1) or Many Volumes to Many Compute (*..*)

**Inverse Property**: `has_attached_volume`

**Semantic Rules**:
- A volume can be attached to one or more compute resources (shared storage)
- A compute resource can have multiple attached volumes
- This relationship models storage connectivity

**Usage Example**:
```turtle
:Volume_EBS_vol123 :attached_to :CloudInstance_i-abc123 .
```

---

#### 7. provisioned_from (CloudInstance/CloudStorageService → CloudService)

**Definition**: A cloud resource is provisioned from a cloud service.

**OWL Property Definition**:
```turtle
:provisioned_from
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :CloudInstance :CloudStorageService :ObjectStorageBucket ) ] ;
  rdfs:range :CloudService ;
  rdfs:label "provisioned from" ;
  rdfs:comment "A cloud resource is provisioned from a cloud service" .
```

**Cardinality**: Many Resources to 1 Service (*..1)

**Inverse Property**: `provisions`

**Semantic Rules**:
- Cloud resources are provisioned from managed cloud services
- This relationship tracks cloud service dependencies
- Used for cloud-specific infrastructure modeling

**Usage Example**:
```turtle
:CloudInstance_i-abc123 :provisioned_from :CloudService_AWS_EC2 .
:CloudStorageService_RDS_db123 :provisioned_from :CloudService_AWS_RDS .
```

---

#### 8. replicated_to (StorageVolume → StorageVolume)

**Definition**: A storage volume is replicated to another storage volume.

**OWL Property Definition**:
```turtle
:replicated_to
  rdf:type owl:ObjectProperty ;
  rdfs:domain :StorageVolume ;
  rdfs:range :StorageVolume ;
  rdfs:label "replicated to" ;
  rdfs:comment "A storage volume is replicated to another volume" .
```

**Cardinality**: Many Volumes to Many Volumes (*..*)

**Inverse Property**: `replica_of`

**Semantic Rules**:
- Volumes can be replicated for redundancy and disaster recovery
- Replication can be synchronous or asynchronous (captured in relationship properties)
- This relationship models storage replication topology

**Usage Example**:
```turtle
:Volume_Primary_LUN_456 :replicated_to :Volume_DR_LUN_789 .
```

---

### Cross-Layer Relationships

#### 9. hosts (Layer 4 → Layer 2)

**Definition**: Physical infrastructure hosts applications.

**OWL Property Definition**:
```turtle
:hosts
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :VirtualMachine :PhysicalServer :CloudInstance ) ] ;
  rdfs:range [ owl:unionOf ( :Application :ApplicationServer :Database ) ] ;
  rdfs:label "hosts" ;
  rdfs:comment "Infrastructure hosts applications" .
```

**Cardinality**: 1 Infrastructure to Many Applications (1..*)

**Inverse Property**: `runs_on`

**Semantic Rules**:
- Compute resources host application workloads
- Multiple applications can run on the same infrastructure
- This relationship links Layer 4 to Layer 2 (bypassing Layer 3 for legacy apps)

**Usage Example**:
```turtle
:VM_AppServer01 :hosts :Application_CRM .
:PhysicalServer_DB01 :hosts :Database_OracleDB .
:CloudInstance_i-abc123 :hosts :ApplicationServer_WebSphere .
```

---

#### 10. hosts (Layer 4 → Layer 3)

**Definition**: Physical infrastructure hosts container pods.

**OWL Property Definition**:
```turtle
:hosts
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :VirtualMachine :PhysicalServer :CloudInstance ) ] ;
  rdfs:range :Pod ;
  rdfs:label "hosts" ;
  rdfs:comment "Infrastructure hosts container pods" .
```

**Cardinality**: 1 Infrastructure to Many Pods (1..*)

**Inverse Property**: `runs_on`

**Semantic Rules**:
- Compute resources host containerized workloads
- Multiple pods can run on the same infrastructure node
- This relationship links Layer 4 to Layer 3

**Usage Example**:
```turtle
:VM_K8sWorker01 :hosts :Pod_OrderService_abc123 .
:CloudInstance_i-xyz789 :hosts :Pod_PaymentService_def456 .
```

---

#### 11. stored_on (Layer 2 → Layer 4)

**Definition**: Logical storage (databases, file storage) is stored on physical storage.

**OWL Property Definition**:
```turtle
:stored_on
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Database :DatabaseInstance :FileStorageService ) ] ;
  rdfs:range [ owl:unionOf ( :StorageVolume :CloudStorageService ) ] ;
  rdfs:label "stored on" ;
  rdfs:comment "Logical storage is stored on physical storage" .
```

**Cardinality**: Many Logical Storage to 1 Physical Storage (*..1)

**Inverse Property**: `stores`

**Semantic Rules**:
- Logical storage entities (Layer 2) are stored on physical storage (Layer 4)
- This relationship enables storage decomposition
- Links application data to physical storage infrastructure

**Usage Example**:
```turtle
:Database_OrderDB :stored_on :StorageVolume_LUN_456 .
:DatabaseInstance_ERPDB01 :stored_on :CloudStorageService_RDS_db123 .
:FileStorageService_MediaStorage :stored_on :StorageVolume_NFS_789 .
```

---

#### 12. stored_in (Layer 2 → Layer 4)

**Definition**: Object storage services are stored in object storage buckets.

**OWL Property Definition**:
```turtle
:stored_in
  rdf:type owl:ObjectProperty ;
  rdfs:domain :ObjectStorageService ;
  rdfs:range :ObjectStorageBucket ;
  rdfs:label "stored in" ;
  rdfs:comment "Object storage is stored in buckets" .
```

**Cardinality**: Many Services to 1 Bucket (*..1)

**Inverse Property**: `contains_objects`

**Semantic Rules**:
- Logical object storage (Layer 2) is stored in physical buckets (Layer 4)
- This relationship models object storage decomposition
- Links application object storage to cloud storage buckets

**Usage Example**:
```turtle
:ObjectStorageService_DocumentBucket :stored_in :ObjectStorageBucket_s3_documents .
```

---

#### 13. uses (Layer 3 → Layer 4)

**Definition**: Containers use persistent storage volumes.

**OWL Property Definition**:
```turtle
:uses
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Container :Pod ) ] ;
  rdfs:range [ owl:unionOf ( :StorageVolume :FileSystem ) ] ;
  rdfs:label "uses" ;
  rdfs:comment "Containers use persistent storage" .
```

**Cardinality**: Many Containers to Many Storage (*..*)

**Inverse Property**: `used_by`

**Semantic Rules**:
- Containers can mount persistent volumes for data storage
- Multiple containers can share the same storage (ReadWriteMany)
- This relationship links Layer 3 to Layer 4 storage

**Usage Example**:
```turtle
:Pod_PostgresDB_abc123 :uses :StorageVolume_PV_postgres_data .
:Container_MediaProcessor :uses :FileSystem_NFS_MediaStorage .
```

---

## Validation Rules and Constraints

### Layer Assignment Rules

1. All Physical Infrastructure entities MUST belong to Layer 4
2. Physical Infrastructure entities MUST NOT have attributes from other layers
3. Cross-layer relationships MUST connect to Layer 2 (Application) or Layer 3 (Container)

### Attribute Constraints

1. **Mandatory Attributes**: name, resource_type, location (for on-premises), region (for cloud), lifecycle_status
2. **Enumeration Validation**: All enum attributes MUST use defined values
3. **Capacity Validation**: Capacity values MUST be positive numbers
4. **Resource Type Consistency**: resource_type MUST match entity type (physical for PhysicalServer, virtual for VM, cloud_iaas for CloudInstance)
5. **Cloud Provider Consistency**: Cloud entities MUST have valid cloud_provider values

### Relationship Constraints

1. **VM-Hypervisor**: Every VM MUST run on exactly one hypervisor
2. **Hypervisor-Server**: Every hypervisor MUST be hosted on exactly one physical server
3. **Volume-Array**: Every volume MUST be allocated from exactly one storage array or pool
4. **Circular Dependencies**: Storage replication MUST NOT create circular dependencies
5. **Cross-Layer Hosting**: Compute resources MUST host either applications (Layer 2) or pods (Layer 3), not both simultaneously for the same workload

### SHACL Cross-Entity Validation

```turtle
# Validate VM must run on hypervisor
:VMHypervisorConstraint
  a sh:NodeShape ;
  sh:targetClass :VirtualMachine ;
  sh:property [
    sh:path :runs_on ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:class :Hypervisor ;
  ] .

# Validate hypervisor must be on physical server
:HypervisorServerConstraint
  a sh:NodeShape ;
  sh:targetClass :Hypervisor ;
  sh:property [
    sh:path :hosted_on ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:class :PhysicalServer ;
  ] .

# Validate volume must be allocated from array or pool
:VolumeAllocationConstraint
  a sh:NodeShape ;
  sh:targetClass :StorageVolume ;
  sh:property [
    sh:path :allocated_from ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:or (
      [ sh:class :StorageArray ]
      [ sh:class :StoragePool ]
    ) ;
  ] .

# Validate cloud resources have cloud provider
:CloudResourceConstraint
  a sh:NodeShape ;
  sh:targetClass :CloudInstance ;
  sh:property [
    sh:path :cloud_provider ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
  ] ;
  sh:property [
    sh:path :region ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
  ] .
```

---

## Usage Patterns and Examples

### Pattern 1: On-Premises Virtualized Infrastructure

**Scenario**: Traditional datacenter with VMware virtualization

**Decomposition Chain**: Application → VM → Hypervisor → Physical Server

**Example Instance Data**:
```turtle
# Physical Server
:PhysicalServer_Dell_R740_12
  rdf:type :PhysicalServer ;
  :name "dell-r740-rack05-u12" ;
  :serial_number "SN123456789" ;
  :manufacturer "Dell" ;
  :model "PowerEdge R740" ;
  :resource_type "physical" ;
  :location "DC1-Rack05-U12" ;
  :datacenter "Datacenter-NYC-01" ;
  :cpu_count 2 ;
  :cpu_cores 48 ;
  :memory_gb 512 ;
  :operating_system "VMware ESXi" ;
  :os_version "7.0.3" ;
  :power_state "on" ;
  :lifecycle_status "active" .

# Hypervisor
:Hypervisor_ESXi_Host05
  rdf:type :Hypervisor ;
  :name "esxi-host-05.example.com" ;
  :hypervisor_type "vmware_esxi" ;
  :version "7.0.3" ;
  :resource_type "virtual" ;
  :location "DC1-Rack05-U12" ;
  :total_cpu_cores 48 ;
  :total_memory_gb 512 ;
  :allocated_cpu_cores 36 ;
  :allocated_memory_gb 384 ;
  :vm_count 12 ;
  :lifecycle_status "active" ;
  :hosted_on :PhysicalServer_Dell_R740_12 .

# Virtual Machine
:VM_WebServer01
  rdf:type :VirtualMachine ;
  :name "web-server-01" ;
  :vm_id "vm-50123456-abcd-1234-efgh-567890abcdef" ;
  :resource_type "virtual" ;
  :location "DC1-Rack05-U12" ;
  :vcpu_count 4 ;
  :memory_gb 16 ;
  :disk_gb 100 ;
  :operating_system "Ubuntu Linux" ;
  :os_version "22.04 LTS" ;
  :ip_address "10.10.10.101" ;
  :vm_tools_status "running" ;
  :power_state "on" ;
  :lifecycle_status "running" ;
  :runs_on :Hypervisor_ESXi_Host05 .

# Application hosted on VM
:Application_WebApp01
  rdf:type :Application ;
  :name "Corporate Web Application" ;
  :runs_on :VM_WebServer01 .
```

**Relationships**:
- Application_WebApp01 `runs_on` VM_WebServer01
- VM_WebServer01 `runs_on` Hypervisor_ESXi_Host05
- Hypervisor_ESXi_Host05 `hosted_on` PhysicalServer_Dell_R740_12

---

### Pattern 2: Cloud Infrastructure (AWS)

**Scenario**: Application running on AWS EC2 with EBS storage

**Decomposition Chain**: Application → CloudInstance → CloudService (EC2)

**Example Instance Data**:
```turtle
# Cloud Instance
:CloudInstance_WebServer_AWS
  rdf:type :CloudInstance ;
  :name "web-server-prod-01" ;
  :instance_id "i-0abc123def456789" ;
  :resource_type "cloud_iaas" ;
  :cloud_provider "aws" ;
  :instance_type "t3.large" ;
  :region "us-east-1" ;
  :availability_zone "us-east-1a" ;
  :vcpu_count 2 ;
  :memory_gb 8 ;
  :operating_system "Amazon Linux" ;
  :platform "linux" ;
  :public_ip "54.123.45.67" ;
  :private_ip "10.0.1.100" ;
  :vpc_id "vpc-0123456789abcdef" ;
  :subnet_id "subnet-abc123def456" ;
  :lifecycle_status "running" .

# EBS Volume
:StorageVolume_EBS_Root
  rdf:type :StorageVolume ;
  :name "web-server-root-volume" ;
  :volume_id "vol-0abc123def456789" ;
  :volume_type "block_volume" ;
  :resource_type "cloud_iaas" ;
  :capacity_gb 100 ;
  :encrypted true ;
  :iops 3000 ;
  :lifecycle_status "in_use" ;
  :attached_to :CloudInstance_WebServer_AWS .

# Cloud Storage Service (EBS)
:CloudStorageService_AWS_EBS
  rdf:type :CloudStorageService ;
  :name "AWS EBS" ;
  :resource_type "cloud_paas" ;
  :cloud_provider "aws" ;
  :storage_type "block" ;
  :service_name "EBS" ;
  :region "us-east-1" ;
  :lifecycle_status "available" .

# Application hosted on cloud instance
:Application_WebApp_Cloud
  rdf:type :Application ;
  :name "Cloud Web Application" ;
  :runs_on :CloudInstance_WebServer_AWS .
```

**Relationships**:
- Application_WebApp_Cloud `runs_on` CloudInstance_WebServer_AWS
- StorageVolume_EBS_Root `attached_to` CloudInstance_WebServer_AWS
- StorageVolume_EBS_Root `provisioned_from` CloudStorageService_AWS_EBS

---

### Pattern 3: Storage Decomposition (On-Premises Database)

**Scenario**: Oracle database with SAN storage

**Decomposition Chain**: Database → StorageVolume → StorageArray

**Example Instance Data**:
```turtle
# Storage Array
:StorageArray_NetApp_SAN01
  rdf:type :StorageArray ;
  :name "netapp-san-01" ;
  :serial_number "SN987654321" ;
  :manufacturer "NetApp" ;
  :model "FAS8200" ;
  :array_type "san" ;
  :resource_type "physical" ;
  :location "DC1-Storage-Room" ;
  :total_capacity_tb 50 ;
  :used_capacity_tb 32 ;
  :available_capacity_tb 18 ;
  :raid_level "RAID6" ;
  :protocol "iSCSI" ;
  :lifecycle_status "active" .

# Storage Volume (LUN)
:StorageVolume_OracleDB_LUN
  rdf:type :StorageVolume ;
  :name "oracle-db-lun-01" ;
  :volume_id "lun-456" ;
  :volume_type "lun" ;
  :resource_type "physical" ;
  :capacity_gb 500 ;
  :used_capacity_gb 350 ;
  :thin_provisioned false ;
  :encrypted true ;
  :lifecycle_status "in_use" ;
  :allocated_from :StorageArray_NetApp_SAN01 ;
  :attached_to :VM_DBServer01 .

# Database
:Database_OracleDB_Prod
  rdf:type :Database ;
  :name "Oracle Production Database" ;
  :stored_on :StorageVolume_OracleDB_LUN .

# Virtual Machine hosting database
:VM_DBServer01
  rdf:type :VirtualMachine ;
  :name "db-server-01" ;
  :resource_type "virtual" ;
  :location "DC1-Rack05-U12" ;
  :vcpu_count 8 ;
  :memory_gb 64 ;
  :lifecycle_status "running" ;
  :runs_on :Hypervisor_ESXi_Host05 .
```

**Relationships**:
- Database_OracleDB_Prod `stored_on` StorageVolume_OracleDB_LUN
- StorageVolume_OracleDB_LUN `allocated_from` StorageArray_NetApp_SAN01
- StorageVolume_OracleDB_LUN `attached_to` VM_DBServer01
- VM_DBServer01 `runs_on` Hypervisor_ESXi_Host05

---

### Pattern 4: Containerized Application with Persistent Storage

**Scenario**: PostgreSQL database in Kubernetes with persistent volume

**Decomposition Chain**: Database → Pod → VM → Hypervisor → Physical Server
**Storage Chain**: Database → StorageVolume → StorageArray

**Example Instance Data**:
```turtle
# Pod
:Pod_PostgresDB
  rdf:type :Pod ;
  :name "postgres-db-pod-abc123" ;
  :namespace "production" ;
  :lifecycle_status "Running" ;
  :runs_on :VM_K8sWorker01 .

# Storage Volume (Persistent Volume)
:StorageVolume_PV_Postgres
  rdf:type :StorageVolume ;
  :name "postgres-pv-01" ;
  :volume_id "pv-postgres-data" ;
  :volume_type "persistent_volume" ;
  :resource_type "virtual" ;
  :capacity_gb 100 ;
  :lifecycle_status "in_use" ;
  :allocated_from :StorageArray_NetApp_SAN01 .

# Database
:Database_PostgresDB
  rdf:type :Database ;
  :name "PostgreSQL Production Database" ;
  :stored_on :StorageVolume_PV_Postgres .

# VM (Kubernetes Worker Node)
:VM_K8sWorker01
  rdf:type :VirtualMachine ;
  :name "k8s-worker-01" ;
  :resource_type "virtual" ;
  :location "DC1-Rack05-U12" ;
  :vcpu_count 8 ;
  :memory_gb 32 ;
  :lifecycle_status "running" ;
  :runs_on :Hypervisor_ESXi_Host05 .
```

**Relationships**:
- Database_PostgresDB `deployed_as` Pod_PostgresDB (Layer 2 → Layer 3)
- Pod_PostgresDB `runs_on` VM_K8sWorker01 (Layer 3 → Layer 4)
- Pod_PostgresDB `uses` StorageVolume_PV_Postgres (Layer 3 → Layer 4)
- Database_PostgresDB `stored_on` StorageVolume_PV_Postgres (Layer 2 → Layer 4)
- VM_K8sWorker01 `runs_on` Hypervisor_ESXi_Host05 (Layer 4 intra-layer)
- StorageVolume_PV_Postgres `allocated_from` StorageArray_NetApp_SAN01 (Layer 4 intra-layer)

---

### Pattern 5: Cloud Managed Database (AWS RDS)

**Scenario**: Application using AWS RDS PostgreSQL

**Decomposition Chain**: Database → CloudStorageService (RDS)

**Example Instance Data**:
```turtle
# Cloud Storage Service (RDS)
:CloudStorageService_RDS_Postgres
  rdf:type :CloudStorageService ;
  :name "rds-postgres-prod-01" ;
  :service_id "db-ABC123DEF456" ;
  :resource_type "cloud_paas" ;
  :cloud_provider "aws" ;
  :storage_type "database" ;
  :service_name "RDS" ;
  :region "us-east-1" ;
  :capacity_gb 500 ;
  :storage_class "gp3" ;
  :iops 12000 ;
  :encrypted true ;
  :lifecycle_status "available" .

# Database
:Database_RDS_Postgres
  rdf:type :Database ;
  :name "RDS PostgreSQL Production" ;
  :stored_on :CloudStorageService_RDS_Postgres .

# Application
:Application_CloudApp
  rdf:type :Application ;
  :name "Cloud Application" ;
  :uses :Database_RDS_Postgres .
```

**Relationships**:
- Application_CloudApp `uses` Database_RDS_Postgres (Layer 2 intra-layer)
- Database_RDS_Postgres `stored_on` CloudStorageService_RDS_Postgres (Layer 2 → Layer 4)

**Note**: Cloud managed services abstract away the underlying infrastructure, so the decomposition stops at the CloudStorageService level.

---

## Query Patterns

### Query 1: Find All Infrastructure Hosting an Application

**Scenario**: Trace an application down to physical infrastructure

**SPARQL Query**:
```sparql
SELECT ?infrastructure ?type ?location
WHERE {
  :Application_WebApp01 (:runs_on|:deployed_as/:runs_on)+ ?infrastructure .
  ?infrastructure rdf:type ?type .
  ?infrastructure :location ?location .
  FILTER(?type IN (:VirtualMachine, :PhysicalServer, :CloudInstance, :Hypervisor))
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (app:Application {name: 'WebApp01'})-[:RUNS_ON|DEPLOYED_AS*]->(infra)
WHERE infra:VirtualMachine OR infra:PhysicalServer OR infra:CloudInstance OR infra:Hypervisor
RETURN infra.name AS infrastructure,
       labels(infra) AS type,
       infra.location AS location
```

---

### Query 2: Find All Applications on a Physical Server

**Scenario**: Impact analysis - what applications are affected if a physical server fails?

**SPARQL Query**:
```sparql
SELECT ?application ?vm ?hypervisor
WHERE {
  ?application rdf:type :Application .
  ?application :runs_on ?vm .
  ?vm :runs_on ?hypervisor .
  ?hypervisor :hosted_on :PhysicalServer_Dell_R740_12 .
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (server:PhysicalServer {name: 'dell-r740-rack05-u12'})
      <-[:HOSTED_ON]-(hypervisor:Hypervisor)
      <-[:RUNS_ON]-(vm:VirtualMachine)
      <-[:RUNS_ON]-(app:Application)
RETURN app.name AS application,
       vm.name AS virtual_machine,
       hypervisor.name AS hypervisor
```

---

### Query 3: Storage Decomposition - Database to Physical Storage

**Scenario**: Trace a database to its physical storage infrastructure

**SPARQL Query**:
```sparql
SELECT ?database ?volume ?array ?capacity
WHERE {
  ?database rdf:type :Database .
  ?database :stored_on ?volume .
  ?volume :allocated_from ?array .
  ?volume :capacity_gb ?capacity .
  FILTER(?database = :Database_OracleDB_Prod)
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (db:Database {name: 'Oracle Production Database'})
      -[:STORED_ON]->(volume:StorageVolume)
      -[:ALLOCATED_FROM]->(array:StorageArray)
RETURN db.name AS database,
       volume.name AS volume,
       volume.capacity_gb AS capacity,
       array.name AS storage_array,
       array.total_capacity_tb AS array_capacity
```

---

### Query 4: Find All VMs on a Hypervisor

**Scenario**: Capacity planning - how many VMs are on each hypervisor?

**SPARQL Query**:
```sparql
SELECT ?hypervisor ?vm ?vcpu ?memory
WHERE {
  ?vm rdf:type :VirtualMachine .
  ?vm :runs_on ?hypervisor .
  ?vm :vcpu_count ?vcpu .
  ?vm :memory_gb ?memory .
  ?vm :lifecycle_status "running" .
}
GROUP BY ?hypervisor
```

**Cypher Query** (Neo4j):
```cypher
MATCH (hypervisor:Hypervisor)<-[:RUNS_ON]-(vm:VirtualMachine)
WHERE vm.lifecycle_status = 'running'
RETURN hypervisor.name AS hypervisor,
       COUNT(vm) AS vm_count,
       SUM(vm.vcpu_count) AS total_vcpu,
       SUM(vm.memory_gb) AS total_memory_gb,
       hypervisor.total_cpu_cores AS hypervisor_cpu,
       hypervisor.total_memory_gb AS hypervisor_memory
```

---

### Query 5: Find Cloud Resources by Provider and Region

**Scenario**: Cloud inventory - list all AWS resources in us-east-1

**SPARQL Query**:
```sparql
SELECT ?resource ?type ?instance_type ?status
WHERE {
  ?resource rdf:type ?type .
  ?resource :cloud_provider "aws" .
  ?resource :region "us-east-1" .
  ?resource :lifecycle_status ?status .
  FILTER(?type IN (:CloudInstance, :CloudStorageService, :ObjectStorageBucket))
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (resource)
WHERE (resource:CloudInstance OR resource:CloudStorageService OR resource:ObjectStorageBucket)
  AND resource.cloud_provider = 'aws'
  AND resource.region = 'us-east-1'
RETURN resource.name AS resource,
       labels(resource) AS type,
       resource.instance_type AS instance_type,
       resource.lifecycle_status AS status
```

---

### Query 6: Storage Capacity Analysis

**Scenario**: Find storage arrays with low available capacity

**SPARQL Query**:
```sparql
SELECT ?array ?total ?used ?available ?utilization
WHERE {
  ?array rdf:type :StorageArray .
  ?array :total_capacity_tb ?total .
  ?array :used_capacity_tb ?used .
  ?array :available_capacity_tb ?available .
  BIND((?used / ?total * 100) AS ?utilization)
  FILTER(?utilization > 80)
}
ORDER BY DESC(?utilization)
```

**Cypher Query** (Neo4j):
```cypher
MATCH (array:StorageArray)
WHERE array.total_capacity_tb IS NOT NULL
  AND array.used_capacity_tb IS NOT NULL
WITH array,
     array.used_capacity_tb / array.total_capacity_tb * 100 AS utilization
WHERE utilization > 80
RETURN array.name AS storage_array,
       array.total_capacity_tb AS total_tb,
       array.used_capacity_tb AS used_tb,
       array.available_capacity_tb AS available_tb,
       utilization AS utilization_percent
ORDER BY utilization DESC
```

---

### Query 7: Find All Storage Volumes Attached to a VM

**Scenario**: Understand storage dependencies for a virtual machine

**SPARQL Query**:
```sparql
SELECT ?volume ?capacity ?volume_type ?array
WHERE {
  ?volume rdf:type :StorageVolume .
  ?volume :attached_to :VM_WebServer01 .
  ?volume :capacity_gb ?capacity .
  ?volume :volume_type ?volume_type .
  OPTIONAL { ?volume :allocated_from ?array . }
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (vm:VirtualMachine {name: 'web-server-01'})
      <-[:ATTACHED_TO]-(volume:StorageVolume)
OPTIONAL MATCH (volume)-[:ALLOCATED_FROM]->(array)
RETURN volume.name AS volume,
       volume.capacity_gb AS capacity,
       volume.volume_type AS type,
       array.name AS storage_array
```

---

### Query 8: Full Stack Decomposition (Application to Physical Server)

**Scenario**: Complete infrastructure stack for an application

**SPARQL Query**:
```sparql
SELECT ?app ?vm ?hypervisor ?server ?location
WHERE {
  ?app rdf:type :Application .
  ?app :runs_on ?vm .
  ?vm :runs_on ?hypervisor .
  ?hypervisor :hosted_on ?server .
  ?server :location ?location .
  FILTER(?app = :Application_WebApp01)
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH path = (app:Application {name: 'Corporate Web Application'})
             -[:RUNS_ON]->(vm:VirtualMachine)
             -[:RUNS_ON]->(hypervisor:Hypervisor)
             -[:HOSTED_ON]->(server:PhysicalServer)
RETURN app.name AS application,
       vm.name AS virtual_machine,
       hypervisor.name AS hypervisor,
       server.name AS physical_server,
       server.location AS location
```

---

### Query 9: Find Replicated Storage Volumes

**Scenario**: Disaster recovery - identify replicated storage

**SPARQL Query**:
```sparql
SELECT ?primary ?replica ?capacity
WHERE {
  ?primary rdf:type :StorageVolume .
  ?primary :replicated_to ?replica .
  ?primary :capacity_gb ?capacity .
  ?replica :location ?replica_location .
  ?primary :location ?primary_location .
  FILTER(?primary_location != ?replica_location)
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH (primary:StorageVolume)-[:REPLICATED_TO]->(replica:StorageVolume)
WHERE primary.location <> replica.location
RETURN primary.name AS primary_volume,
       primary.location AS primary_location,
       replica.name AS replica_volume,
       replica.location AS replica_location,
       primary.capacity_gb AS capacity
```

---

### Query 10: Containerized Application Full Stack

**Scenario**: Trace containerized application to physical infrastructure

**SPARQL Query**:
```sparql
SELECT ?app ?pod ?vm ?hypervisor ?server
WHERE {
  ?app rdf:type :Application .
  ?app :deployed_as ?pod .
  ?pod :runs_on ?vm .
  ?vm :runs_on ?hypervisor .
  ?hypervisor :hosted_on ?server .
  FILTER(?app = :Application_MicroserviceApp)
}
```

**Cypher Query** (Neo4j):
```cypher
MATCH path = (app:Application {name: 'Microservice Application'})
             -[:DEPLOYED_AS]->(pod:Pod)
             -[:RUNS_ON]->(vm:VirtualMachine)
             -[:RUNS_ON]->(hypervisor:Hypervisor)
             -[:HOSTED_ON]->(server:PhysicalServer)
RETURN app.name AS application,
       pod.name AS pod,
       vm.name AS kubernetes_node,
       hypervisor.name AS hypervisor,
       server.name AS physical_server
```

---

## Framework Mappings

### CIM (Common Information Model) Mapping

| Ontology Entity Type | CIM Class | CIM Namespace |
|----------------------|-----------|---------------|
| PhysicalServer | CIM_ComputerSystem | CIM_Core |
| VirtualMachine | CIM_VirtualComputerSystem | CIM_Virtualization |
| Hypervisor | CIM_VirtualSystemManagementService | CIM_Virtualization |
| StorageArray | CIM_StorageSystem | CIM_Storage |
| StorageVolume | CIM_StorageExtent | CIM_Storage |
| FileSystem | CIM_FileSystem | CIM_Storage |
| StoragePool | CIM_StoragePool | CIM_Storage |

### Cloud Provider API Mapping

| Ontology Entity Type | AWS Service | Azure Service | GCP Service |
|----------------------|-------------|---------------|-------------|
| CloudInstance | EC2 Instance | Virtual Machine | Compute Engine Instance |
| CloudStorageService (Block) | EBS Volume | Managed Disk | Persistent Disk |
| CloudStorageService (Database) | RDS Instance | Azure SQL Database | Cloud SQL Instance |
| ObjectStorageBucket | S3 Bucket | Blob Container | Cloud Storage Bucket |
| CloudService (Compute) | Lambda | Azure Functions | Cloud Functions |

### TOGAF Technology Architecture Mapping

| Ontology Layer | TOGAF Component |
|----------------|-----------------|
| PhysicalServer, VirtualMachine, CloudInstance | Platform Services - Compute |
| StorageArray, StorageVolume, CloudStorageService | Platform Services - Storage |
| Hypervisor | Platform Services - Virtualization |

---

## Summary

This specification defines Layer 4 (Physical Infrastructure) with:

- **11 Entity Types**: PhysicalServer, VirtualMachine, Hypervisor, CloudInstance, CloudService, StorageArray, StorageVolume, FileSystem, StoragePool, CloudStorageService, ObjectStorageBucket
- **150+ Attributes**: Comprehensive coverage of compute and storage properties
- **13 Relationship Types**: 8 intra-layer + 5 cross-layer relationships
- **Framework Sources**: CIM, AWS/Azure/GCP APIs, VMware vSphere, TOGAF
- **5 Usage Patterns**: On-premises, cloud, hybrid, containerized, managed services
- **10 Query Patterns**: Infrastructure discovery, impact analysis, capacity planning

**Requirements Satisfied**:
- 1.4: Layer definition and cross-layer decomposition
- 6.1, 6.2, 6.3, 6.4: On-premises and cloud infrastructure support
- 8.1, 8.2, 8.3, 8.5: Framework-sourced attributes with documentation
- 2.1, 2.2, 2.4: Relationship types and cardinality constraints

---

**Document Version**: 1.0
**Last Updated**: 2025-11-10
**Status**: Complete

