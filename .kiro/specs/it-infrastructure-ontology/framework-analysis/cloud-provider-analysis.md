# Cloud Provider API Analysis

## Overview

This document provides a comprehensive analysis of AWS, Azure, and GCP cloud provider APIs and services, extracting entity types, attributes, and relationships for cloud infrastructure representation in the IT Infrastructure and Application Dependency Ontology.

**Cloud Providers Analyzed**: AWS, Microsoft Azure, Google Cloud Platform (GCP)
**API Sources**: AWS API Reference, Azure REST API, GCP API Documentation
**Analysis Date**: 2025-11-09

---

## Part 1: AWS (Amazon Web Services) Analysis

### AWS Overview

AWS provides a comprehensive set of cloud services including compute, storage, networking, and managed services. AWS uses a service-oriented API model with resources defined per service.

---

### 1. EC2 (Elastic Compute Cloud) - Compute Instances

**AWS Definition**: Virtual servers in the cloud.

**API**: EC2 API
**Resource Type**: `Instance`

**Attributes**:
- `InstanceId` (string, mandatory): Unique instance identifier (e.g., "i-1234567890abcdef0")
- `InstanceType` (string, mandatory): Instance size (e.g., "t3.medium", "m5.large")
- `State.Name` (enum: pending, running, stopping, stopped, shutting-down, terminated, mandatory): Instance state
- `ImageId` (string, mandatory): AMI identifier
- `KeyName` (string, optional): SSH key pair name
- `LaunchTime` (timestamp, mandatory): Instance launch time
- `Placement.AvailabilityZone` (string, mandatory): Availability zone (e.g., "us-east-1a")
- `Placement.Region` (string, mandatory): AWS region (e.g., "us-east-1")
- `PrivateIpAddress` (string, optional): Private IP address
- `PublicIpAddress` (string, optional): Public IP address
- `VpcId` (string, optional): VPC identifier
- `SubnetId` (string, optional): Subnet identifier
- `Platform` (string, optional): Platform (e.g., "Linux/UNIX", "Windows")
- `Architecture` (string, optional): CPU architecture (e.g., "x86_64", "arm64")
- `CpuOptions.CoreCount` (integer, optional): Number of CPU cores
- `CpuOptions.ThreadsPerCore` (integer, optional): Threads per core
- `Tags` (array, optional): Resource tags for organization

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): CloudInstance
- Represents virtual compute resources in AWS

---

### 2. RDS (Relational Database Service) - Managed Databases

**AWS Definition**: Managed relational database service.

**API**: RDS API
**Resource Type**: `DBInstance`

**Attributes**:
- `DBInstanceIdentifier` (string, mandatory): Database instance identifier
- `DBInstanceClass` (string, mandatory): Instance size (e.g., "db.t3.medium")
- `Engine` (string, mandatory): Database engine (e.g., "mysql", "postgres", "oracle", "sqlserver")
- `EngineVersion` (string, mandatory): Database engine version
- `DBInstanceStatus` (string, mandatory): Instance status (e.g., "available", "backing-up", "creating")
- `MasterUsername` (string, mandatory): Master username
- `DBName` (string, optional): Database name
- `AllocatedStorage` (integer, mandatory): Storage size in GB
- `StorageType` (enum: gp2, gp3, io1, io2, standard, mandatory): Storage type
- `Iops` (integer, optional): Provisioned IOPS
- `AvailabilityZone` (string, optional): Availability zone
- `MultiAZ` (boolean, mandatory): Multi-AZ deployment flag
- `Endpoint.Address` (string, optional): Database endpoint hostname
- `Endpoint.Port` (integer, optional): Database port
- `VpcId` (string, optional): VPC identifier
- `PubliclyAccessible` (boolean, mandatory): Public accessibility flag
- `BackupRetentionPeriod` (integer, optional): Backup retention in days
- `PreferredBackupWindow` (string, optional): Backup window
- `PreferredMaintenanceWindow` (string, optional): Maintenance window

**Ontology Mapping**:
- Layer 2 (Application Layer): Database (logical)
- Layer 4 (Physical Infrastructure): CloudStorageService (physical)
- Represents managed database services

---

### 3. S3 (Simple Storage Service) - Object Storage

**AWS Definition**: Scalable object storage service.

**API**: S3 API
**Resource Type**: `Bucket`

**Attributes**:
- `Name` (string, mandatory): Bucket name (globally unique)
- `CreationDate` (timestamp, mandatory): Bucket creation date
- `Region` (string, mandatory): AWS region
- `Versioning.Status` (enum: Enabled, Suspended, optional): Versioning status
- `Encryption.Rules` (array, optional): Server-side encryption rules
- `PublicAccessBlock` (object, optional): Public access block configuration
- `LifecycleConfiguration` (array, optional): Lifecycle rules
- `ReplicationConfiguration` (object, optional): Cross-region replication
- `Tags` (array, optional): Resource tags

**Ontology Mapping**:
- Layer 2 (Application Layer): ObjectStorageService (logical)
- Layer 4 (Physical Infrastructure): ObjectStorageBucket (physical)
- Represents object storage buckets

---

### 4. EBS (Elastic Block Store) - Block Storage

**AWS Definition**: Block-level storage volumes for EC2 instances.

**API**: EC2 API
**Resource Type**: `Volume`

**Attributes**:
- `VolumeId` (string, mandatory): Volume identifier (e.g., "vol-1234567890abcdef0")
- `Size` (integer, mandatory): Volume size in GB
- `VolumeType` (enum: gp2, gp3, io1, io2, st1, sc1, standard, mandatory): Volume type
- `Iops` (integer, optional): Provisioned IOPS
- `Throughput` (integer, optional): Throughput in MB/s (gp3 only)
- `State` (enum: creating, available, in-use, deleting, deleted, error, mandatory): Volume state
- `AvailabilityZone` (string, mandatory): Availability zone
- `Encrypted` (boolean, mandatory): Encryption flag
- `KmsKeyId` (string, optional): KMS key for encryption
- `SnapshotId` (string, optional): Source snapshot
- `Attachments` (array, optional): Attached instances
- `Tags` (array, optional): Resource tags

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): StorageVolume, CloudStorageService
- Represents block storage volumes

---

### 5. VPC (Virtual Private Cloud) - Networking

**AWS Definition**: Isolated virtual network in AWS.

**API**: EC2 API
**Resource Type**: `Vpc`

**Attributes**:
- `VpcId` (string, mandatory): VPC identifier
- `CidrBlock` (string, mandatory): IPv4 CIDR block (e.g., "10.0.0.0/16")
- `State` (enum: pending, available, mandatory): VPC state
- `DhcpOptionsId` (string, optional): DHCP options set
- `InstanceTenancy` (enum: default, dedicated, host, optional): Instance tenancy
- `IsDefault` (boolean, mandatory): Default VPC flag
- `Tags` (array, optional): Resource tags

**Ontology Mapping**:
- Layer 5 (Network): NetworkSegment
- Represents virtual networks

---

### 6. ELB (Elastic Load Balancing) - Load Balancers

**AWS Definition**: Distributes incoming traffic across multiple targets.

**API**: ELBv2 API
**Resource Type**: `LoadBalancer`

**Attributes**:
- `LoadBalancerArn` (string, mandatory): Load balancer ARN
- `LoadBalancerName` (string, mandatory): Load balancer name
- `DNSName` (string, mandatory): DNS name
- `Scheme` (enum: internet-facing, internal, mandatory): Load balancer scheme
- `Type` (enum: application, network, gateway, mandatory): Load balancer type
- `State.Code` (enum: provisioning, active, failed, mandatory): Load balancer state
- `VpcId` (string, mandatory): VPC identifier
- `AvailabilityZones` (array, mandatory): Availability zones
- `SecurityGroups` (array, optional): Security group IDs
- `IpAddressType` (enum: ipv4, dualstack, mandatory): IP address type

**Ontology Mapping**:
- Layer 5 (Network): LoadBalancer
- Represents load balancing services

---

## Part 2: Microsoft Azure Analysis

### Azure Overview

Azure provides cloud services through a resource-based API model with resources organized into resource groups and subscriptions.

---

### 1. Virtual Machines - Compute Instances

**Azure Definition**: Virtual machines in Azure.

**API**: Compute API
**Resource Type**: `VirtualMachine`

**Attributes**:
- `id` (string, mandatory): Resource ID
- `name` (string, mandatory): VM name
- `location` (string, mandatory): Azure region (e.g., "eastus", "westeurope")
- `properties.vmId` (string, mandatory): Unique VM identifier
- `properties.hardwareProfile.vmSize` (string, mandatory): VM size (e.g., "Standard_D2s_v3")
- `properties.provisioningState` (string, mandatory): Provisioning state
- `properties.instanceView.statuses` (array, optional): VM status
- `properties.osProfile.computerName` (string, mandatory): Computer name
- `properties.osProfile.adminUsername` (string, mandatory): Admin username
- `properties.storageProfile.imageReference` (object, mandatory): OS image reference
- `properties.storageProfile.osDisk` (object, mandatory): OS disk configuration
- `properties.networkProfile.networkInterfaces` (array, mandatory): Network interfaces
- `properties.availabilitySet` (object, optional): Availability set
- `properties.zones` (array, optional): Availability zones
- `tags` (object, optional): Resource tags

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): CloudInstance
- Represents virtual machines in Azure

---

### 2. Azure SQL Database - Managed Databases

**Azure Definition**: Managed relational database service.

**API**: SQL API
**Resource Type**: `Database`

**Attributes**:
- `id` (string, mandatory): Resource ID
- `name` (string, mandatory): Database name
- `location` (string, mandatory): Azure region
- `properties.status` (string, mandatory): Database status
- `properties.collation` (string, optional): Database collation
- `properties.edition` (string, optional): Service tier (e.g., "Basic", "Standard", "Premium")
- `properties.serviceLevelObjective` (string, optional): Performance level
- `properties.maxSizeBytes` (integer, optional): Maximum database size
- `properties.creationDate` (timestamp, mandatory): Creation date
- `properties.currentServiceObjectiveName` (string, optional): Current service objective
- `properties.requestedServiceObjectiveName` (string, optional): Requested service objective
- `properties.defaultSecondaryLocation` (string, optional): Geo-replication location
- `properties.elasticPoolName` (string, optional): Elastic pool name
- `tags` (object, optional): Resource tags

**Ontology Mapping**:
- Layer 2 (Application Layer): Database (logical)
- Layer 4 (Physical Infrastructure): CloudStorageService (physical)
- Represents managed SQL databases

---

### 3. Blob Storage - Object Storage

**Azure Definition**: Object storage service for unstructured data.

**API**: Storage API
**Resource Type**: `StorageAccount` / `Container`

**Storage Account Attributes**:
- `id` (string, mandatory): Resource ID
- `name` (string, mandatory): Storage account name
- `location` (string, mandatory): Azure region
- `properties.provisioningState` (string, mandatory): Provisioning state
- `sku.name` (string, mandatory): SKU (e.g., "Standard_LRS", "Premium_LRS")
- `sku.tier` (enum: Standard, Premium, mandatory): Performance tier
- `kind` (enum: Storage, StorageV2, BlobStorage, mandatory): Account kind
- `properties.primaryEndpoints` (object, optional): Primary endpoints
- `properties.encryption` (object, optional): Encryption settings
- `properties.networkAcls` (object, optional): Network rules
- `tags` (object, optional): Resource tags

**Container Attributes**:
- `name` (string, mandatory): Container name
- `properties.publicAccess` (enum: None, Blob, Container, optional): Public access level
- `properties.lastModifiedTime` (timestamp, optional): Last modified time
- `properties.leaseStatus` (string, optional): Lease status
- `properties.leaseState` (string, optional): Lease state

**Ontology Mapping**:
- Layer 2 (Application Layer): ObjectStorageService (logical)
- Layer 4 (Physical Infrastructure): ObjectStorageBucket (physical)
- Represents blob storage containers

---

### 4. Managed Disks - Block Storage

**Azure Definition**: Persistent block storage for Azure VMs.

**API**: Compute API
**Resource Type**: `Disk`

**Attributes**:
- `id` (string, mandatory): Resource ID
- `name` (string, mandatory): Disk name
- `location` (string, mandatory): Azure region
- `properties.diskSizeGB` (integer, mandatory): Disk size in GB
- `properties.diskState` (enum: Unattached, Attached, Reserved, ActiveSAS, mandatory): Disk state
- `sku.name` (enum: Standard_LRS, Premium_LRS, StandardSSD_LRS, UltraSSD_LRS, mandatory): Disk SKU
- `properties.osType` (enum: Windows, Linux, optional): OS type for OS disks
- `properties.creationData.createOption` (enum: Empty, Attach, FromImage, Import, Copy, mandatory): Creation method
- `properties.encryption` (object, optional): Encryption settings
- `properties.diskIOPSReadWrite` (integer, optional): IOPS
- `properties.diskMBpsReadWrite` (integer, optional): Throughput in MB/s
- `zones` (array, optional): Availability zones
- `tags` (object, optional): Resource tags

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): StorageVolume, CloudStorageService
- Represents managed disks

---

### 5. Virtual Network - Networking

**Azure Definition**: Isolated network in Azure.

**API**: Network API
**Resource Type**: `VirtualNetwork`

**Attributes**:
- `id` (string, mandatory): Resource ID
- `name` (string, mandatory): Virtual network name
- `location` (string, mandatory): Azure region
- `properties.addressSpace.addressPrefixes` (array, mandatory): Address prefixes (CIDR)
- `properties.subnets` (array, optional): Subnets
- `properties.dhcpOptions` (object, optional): DHCP options
- `properties.provisioningState` (string, mandatory): Provisioning state
- `properties.enableDdosProtection` (boolean, optional): DDoS protection flag
- `properties.enableVmProtection` (boolean, optional): VM protection flag
- `tags` (object, optional): Resource tags

**Ontology Mapping**:
- Layer 5 (Network): NetworkSegment
- Represents virtual networks

---

### 6. Load Balancer - Load Balancing

**Azure Definition**: Distributes network traffic across multiple resources.

**API**: Network API
**Resource Type**: `LoadBalancer`

**Attributes**:
- `id` (string, mandatory): Resource ID
- `name` (string, mandatory): Load balancer name
- `location` (string, mandatory): Azure region
- `sku.name` (enum: Basic, Standard, Gateway, mandatory): Load balancer SKU
- `properties.frontendIPConfigurations` (array, mandatory): Frontend IP configurations
- `properties.backendAddressPools` (array, mandatory): Backend address pools
- `properties.loadBalancingRules` (array, optional): Load balancing rules
- `properties.probes` (array, optional): Health probes
- `properties.inboundNatRules` (array, optional): Inbound NAT rules
- `properties.provisioningState` (string, mandatory): Provisioning state
- `tags` (object, optional): Resource tags

**Ontology Mapping**:
- Layer 5 (Network): LoadBalancer
- Represents load balancers

---

## Part 3: Google Cloud Platform (GCP) Analysis

### GCP Overview

GCP provides cloud services through a project-based API model with resources organized by projects and regions/zones.

---

### 1. Compute Engine - Virtual Machines

**GCP Definition**: Virtual machines running in Google's data centers.

**API**: Compute Engine API
**Resource Type**: `Instance`

**Attributes**:
- `id` (string, mandatory): Unique instance ID
- `name` (string, mandatory): Instance name
- `zone` (string, mandatory): Zone URL (e.g., "us-central1-a")
- `machineType` (string, mandatory): Machine type URL (e.g., "n1-standard-1")
- `status` (enum: PROVISIONING, STAGING, RUNNING, STOPPING, TERMINATED, mandatory): Instance status
- `cpuPlatform` (string, optional): CPU platform
- `creationTimestamp` (timestamp, mandatory): Creation time
- `disks` (array, mandatory): Attached disks
- `networkInterfaces` (array, mandatory): Network interfaces
- `networkInterfaces[].networkIP` (string, optional): Internal IP
- `networkInterfaces[].accessConfigs[].natIP` (string, optional): External IP
- `metadata` (object, optional): Instance metadata
- `tags.items` (array, optional): Network tags
- `labels` (object, optional): Resource labels
- `scheduling.preemptible` (boolean, optional): Preemptible instance flag

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): CloudInstance
- Represents virtual machines in GCP

---

### 2. Cloud SQL - Managed Databases

**GCP Definition**: Fully managed relational database service.

**API**: Cloud SQL Admin API
**Resource Type**: `DatabaseInstance`

**Attributes**:
- `name` (string, mandatory): Instance name
- `project` (string, mandatory): Project ID
- `region` (string, mandatory): GCP region
- `databaseVersion` (enum: MYSQL_5_7, MYSQL_8_0, POSTGRES_13, SQLSERVER_2019, mandatory): Database version
- `state` (enum: RUNNABLE, SUSPENDED, PENDING_DELETE, MAINTENANCE, mandatory): Instance state
- `settings.tier` (string, mandatory): Machine tier (e.g., "db-n1-standard-1")
- `settings.dataDiskSizeGb` (integer, optional): Data disk size
- `settings.dataDiskType` (enum: PD_SSD, PD_HDD, mandatory): Disk type
- `settings.ipConfiguration.ipv4Enabled` (boolean, optional): IPv4 enabled flag
- `settings.ipConfiguration.privateNetwork` (string, optional): VPC network
- `settings.backupConfiguration` (object, optional): Backup configuration
- `settings.maintenanceWindow` (object, optional): Maintenance window
- `connectionName` (string, mandatory): Connection name
- `ipAddresses` (array, optional): IP addresses
- `gceZone` (string, optional): Compute Engine zone

**Ontology Mapping**:
- Layer 2 (Application Layer): Database (logical)
- Layer 4 (Physical Infrastructure): CloudStorageService (physical)
- Represents managed databases

---

### 3. Cloud Storage - Object Storage

**GCP Definition**: Unified object storage service.

**API**: Cloud Storage API
**Resource Type**: `Bucket`

**Attributes**:
- `id` (string, mandatory): Bucket ID
- `name` (string, mandatory): Bucket name (globally unique)
- `location` (string, mandatory): Bucket location (region or multi-region)
- `locationType` (enum: region, multi-region, mandatory): Location type
- `storageClass` (enum: STANDARD, NEARLINE, COLDLINE, ARCHIVE, mandatory): Storage class
- `timeCreated` (timestamp, mandatory): Creation time
- `updated` (timestamp, mandatory): Last update time
- `versioning.enabled` (boolean, optional): Versioning enabled flag
- `encryption` (object, optional): Encryption configuration
- `lifecycle` (object, optional): Lifecycle management rules
- `iamConfiguration` (object, optional): IAM configuration
- `labels` (object, optional): Resource labels

**Ontology Mapping**:
- Layer 2 (Application Layer): ObjectStorageService (logical)
- Layer 4 (Physical Infrastructure): ObjectStorageBucket (physical)
- Represents storage buckets

---

### 4. Persistent Disks - Block Storage

**GCP Definition**: Durable block storage for Compute Engine instances.

**API**: Compute Engine API
**Resource Type**: `Disk`

**Attributes**:
- `id` (string, mandatory): Unique disk ID
- `name` (string, mandatory): Disk name
- `zone` (string, mandatory): Zone URL
- `sizeGb` (integer, mandatory): Disk size in GB
- `type` (string, mandatory): Disk type URL (pd-standard, pd-ssd, pd-balanced)
- `status` (enum: CREATING, READY, FAILED, DELETING, mandatory): Disk status
- `sourceImage` (string, optional): Source image URL
- `sourceSnapshot` (string, optional): Source snapshot URL
- `users` (array, optional): Attached instances
- `creationTimestamp` (timestamp, mandatory): Creation time
- `labels` (object, optional): Resource labels
- `physicalBlockSizeBytes` (integer, optional): Physical block size
- `provisionedIops` (integer, optional): Provisioned IOPS

**Ontology Mapping**:
- Layer 4 (Physical Infrastructure): StorageVolume, CloudStorageService
- Represents persistent disks

---

### 5. VPC Network - Networking

**GCP Definition**: Virtual private cloud network.

**API**: Compute Engine API
**Resource Type**: `Network`

**Attributes**:
- `id` (string, mandatory): Unique network ID
- `name` (string, mandatory): Network name
- `autoCreateSubnetworks` (boolean, mandatory): Auto-create subnets flag
- `subnetworks` (array, optional): Subnet URLs
- `routingConfig.routingMode` (enum: REGIONAL, GLOBAL, mandatory): Routing mode
- `creationTimestamp` (timestamp, mandatory): Creation time
- `mtu` (integer, optional): Maximum transmission unit

**Ontology Mapping**:
- Layer 5 (Network): NetworkSegment
- Represents VPC networks

---

### 6. Cloud Load Balancing - Load Balancers

**GCP Definition**: Scalable load balancing service.

**API**: Compute Engine API
**Resource Types**: `ForwardingRule`, `TargetHttpProxy`, `BackendService`

**ForwardingRule Attributes**:
- `id` (string, mandatory): Unique forwarding rule ID
- `name` (string, mandatory): Forwarding rule name
- `region` (string, optional): Region (for regional load balancers)
- `IPAddress` (string, optional): IP address
- `IPProtocol` (enum: TCP, UDP, ESP, AH, SCTP, ICMP, mandatory): IP protocol
- `portRange` (string, optional): Port range
- `target` (string, mandatory): Target resource URL
- `loadBalancingScheme` (enum: EXTERNAL, INTERNAL, INTERNAL_MANAGED, mandatory): Load balancing scheme
- `networkTier` (enum: PREMIUM, STANDARD, optional): Network tier

**Ontology Mapping**:
- Layer 5 (Network): LoadBalancer
- Represents load balancing services

---

## Part 4: Cloud Deployment Model Attributes

### Common Cloud Attributes Across Providers

**Cloud Instance Attributes** (Layer 4):
- `cloud_provider` (enum: aws, azure, gcp, alibaba, oracle, mandatory): Cloud provider
- `resource_id` (string, mandatory): Provider-specific resource identifier
- `resource_type` (enum: cloud_iaas, cloud_paas, cloud_saas, mandatory): Service model
- `region` (string, mandatory): Cloud region
- `availability_zone` (string, optional): Availability zone
- `instance_size` (string, mandatory): Instance/VM size
- `pricing_model` (enum: on_demand, reserved, spot, savings_plan, optional): Pricing model
- `tenancy` (enum: shared, dedicated, host, optional): Instance tenancy
- `tags` (map[string]string, optional): Resource tags/labels

**Cloud Storage Attributes** (Layer 4):
- `cloud_provider` (enum: aws, azure, gcp, mandatory): Cloud provider
- `storage_type` (enum: block, object, file, managed_database, mandatory): Storage type
- `storage_class` (string, optional): Storage tier/class
- `capacity_gb` (integer, optional): Storage capacity
- `iops` (integer, optional): Provisioned IOPS
- `throughput_mbps` (integer, optional): Throughput
- `encryption_enabled` (boolean, mandatory): Encryption flag
- `replication_type` (string, optional): Replication configuration

**Cloud Network Attributes** (Layer 5):
- `cloud_provider` (enum: aws, azure, gcp, mandatory): Cloud provider
- `network_id` (string, mandatory): Network identifier
- `cidr_block` (string, mandatory): IP address range
- `is_default` (boolean, optional): Default network flag
- `dns_enabled` (boolean, optional): DNS resolution enabled

**Managed Service Attributes** (Layer 2 or Layer 4):
- `cloud_provider` (enum: aws, azure, gcp, mandatory): Cloud provider
- `service_type` (string, mandatory): Service type (e.g., "rds", "sql-database", "cloud-sql")
- `service_tier` (string, optional): Service tier/edition
- `engine_type` (string, optional): Database engine type
- `engine_version` (string, optional): Engine version
- `multi_az` (boolean, optional): Multi-AZ deployment
- `backup_retention_days` (integer, optional): Backup retention period
- `maintenance_window` (string, optional): Maintenance window

---

## Part 5: Cloud Provider Mapping Summary

### Compute Resources Mapping

| AWS | Azure | GCP | Ontology Entity | Layer |
|-----|-------|-----|-----------------|-------|
| EC2 Instance | Virtual Machine | Compute Engine Instance | CloudInstance | Layer 4 |
| Lambda | Azure Functions | Cloud Functions | CloudService (serverless) | Layer 4 |
| ECS/EKS | AKS | GKE | Cluster | Layer 3 |

### Storage Resources Mapping

| AWS | Azure | GCP | Ontology Entity | Layer |
|-----|-------|-----|-----------------|-------|
| RDS | Azure SQL Database | Cloud SQL | Database (logical) / CloudStorageService (physical) | Layer 2 / Layer 4 |
| S3 Bucket | Blob Container | Cloud Storage Bucket | ObjectStorageService (logical) / ObjectStorageBucket (physical) | Layer 2 / Layer 4 |
| EBS Volume | Managed Disk | Persistent Disk | StorageVolume / CloudStorageService | Layer 4 |
| EFS | Azure Files | Filestore | FileStorageService | Layer 2 / Layer 4 |

### Network Resources Mapping

| AWS | Azure | GCP | Ontology Entity | Layer |
|-----|-------|-----|-----------------|-------|
| VPC | Virtual Network | VPC Network | NetworkSegment | Layer 5 |
| Subnet | Subnet | Subnet | NetworkSegment | Layer 5 |
| ELB/ALB/NLB | Load Balancer | Cloud Load Balancing | LoadBalancer | Layer 5 |
| Security Group | Network Security Group | Firewall Rules | Firewall | Layer 6 |
| Route Table | Route Table | Routes | NetworkRoute | Layer 5 |

---

## Part 6: Cloud-Specific Relationship Types

### Cloud Relationships

**Compute Relationships**:
- `provisioned_in`: CloudInstance → Region/AvailabilityZone
- `attached_to`: StorageVolume → CloudInstance
- `member_of`: CloudInstance → VPC/VirtualNetwork

**Storage Relationships**:
- `hosted_in`: ManagedDatabase → Region/AvailabilityZone
- `backed_by`: ManagedDatabase → StorageVolume
- `replicated_to`: StorageVolume → Region (for cross-region replication)

**Network Relationships**:
- `routes_through`: CommunicationPath → LoadBalancer
- `protected_by`: CloudInstance → SecurityGroup/NetworkSecurityGroup
- `connected_to`: VPC → VPC (VPC peering)

---

## Conclusion

This analysis of AWS, Azure, and GCP cloud provider APIs has identified comprehensive attributes and relationships for cloud infrastructure representation:

**AWS Contributions**:
- EC2 instances with detailed compute attributes
- RDS managed databases with backup and maintenance configurations
- S3 object storage with versioning and lifecycle management
- EBS block storage with IOPS and throughput specifications
- VPC networking with CIDR blocks and routing
- ELB load balancing with multiple types (ALB, NLB, GLB)

**Azure Contributions**:
- Virtual machines with availability sets and zones
- Azure SQL Database with service tiers and elastic pools
- Blob storage with storage account SKUs and access tiers
- Managed disks with multiple performance tiers
- Virtual networks with DDoS protection
- Load balancers with SKU-based capabilities

**GCP Contributions**:
- Compute Engine instances with preemptible options
- Cloud SQL with connection names and private networking
- Cloud Storage with multi-region and storage classes
- Persistent disks with balanced and SSD options
- VPC networks with global routing
- Cloud Load Balancing with multiple schemes

These cloud provider APIs enable the ontology to represent hybrid and multi-cloud environments, supporting both on-premises and cloud infrastructure with consistent abstractions while preserving cloud-specific attributes.

---

**Analysis Complete**: 2025-11-09
**Next Steps**: Integrate cloud provider attributes into the ontology design document and update entity type specifications for cloud resources.
