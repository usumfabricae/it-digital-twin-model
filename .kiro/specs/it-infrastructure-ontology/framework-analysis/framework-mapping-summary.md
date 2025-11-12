# Framework Mapping Summary

## Overview

This document provides a consolidated summary of all framework analyses conducted for the IT Infrastructure and Application Dependency Ontology. It synthesizes findings from TOGAF, CIM, ITIL, ArchiMate, Kubernetes, OpenShift, AWS, Azure, and GCP.

**Analysis Date**: 2025-11-09
**Status**: Complete

---

## Framework Coverage

| Framework | Version | Focus Area | Analysis Document |
|-----------|---------|------------|-------------------|
| TOGAF | 9.2 | Enterprise Architecture | togaf-analysis.md |
| CIM | 2.x | Infrastructure Modeling | cim-analysis.md |
| ITIL | 4 (2019) | Service Management | itil-archimate-analysis.md |
| ArchiMate | 3.1 | Architecture Modeling | itil-archimate-analysis.md |
| Kubernetes | 1.28+ | Container Orchestration | kubernetes-openshift-analysis.md |
| OpenShift | 4.14+ | Container Platform | kubernetes-openshift-analysis.md |
| AWS | Current | Cloud Services | cloud-provider-analysis.md |
| Azure | Current | Cloud Services | cloud-provider-analysis.md |
| GCP | Current | Cloud Services | cloud-provider-analysis.md |

---

## Layer-by-Layer Framework Contributions

### Layer 1: Business Processes

**Primary Frameworks**: TOGAF, ArchiMate

**Entity Types**:
- BusinessProcess (TOGAF, ArchiMate)
- BusinessCapability (TOGAF)
- BusinessService (TOGAF, ITIL, ArchiMate)
- Product (ArchiMate)

**Key Attributes**:
- From TOGAF: `name`, `description`, `owner`, `criticality`, `lifecycle_status`
- From ITIL: `service_level`, `availability_target`, `cost_center`
- From ArchiMate: `process_type` (core, support, management)

---

### Layer 2: Application Layer

**Primary Frameworks**: TOGAF, CIM, ITIL, ArchiMate, Cloud Providers

**Entity Types**:
- Application (TOGAF, CIM, ITIL, ArchiMate)
- ApplicationComponent (TOGAF, ArchiMate)
- ApplicationServer (ArchiMate, ITIL)
- Service (TOGAF, ArchiMate)
- API (ArchiMate)
- Database (TOGAF, CIM, AWS RDS, Azure SQL, GCP Cloud SQL)
- DataObject (TOGAF, ArchiMate)
- MessageQueue (Enterprise patterns)
- CacheService (Enterprise patterns)
- FileStorageService (Cloud providers)
- ObjectStorageService (AWS S3, Azure Blob, GCP Cloud Storage)

**Key Attributes**:
- From TOGAF: `name`, `version`, `application_type`, `technology_stack`
- From ITIL: `vendor`, `license_type`, `support_contract`, `end_of_life_date`
- From ArchiMate: `component_type`, `interface_type`, `endpoint_url`, `authentication_method`
- From Cloud Providers: `cloud_provider`, `service_tier`, `engine_type`

---

### Layer 3: Container and Orchestration

**Primary Frameworks**: Kubernetes, OpenShift, CIM

**Entity Types**:
- Container (Kubernetes, CIM)
- Pod (Kubernetes)
- Deployment (Kubernetes)
- StatefulSet (Kubernetes)
- DaemonSet (Kubernetes)
- Service (Kubernetes)
- Route (OpenShift)
- Ingress (Kubernetes)
- Namespace (Kubernetes)
- Project (OpenShift)
- Cluster (Kubernetes, OpenShift)
- ContainerImage (Kubernetes, OpenShift)

**Key Attributes**:
- From Kubernetes: `replica_count`, `image_name`, `resource_limits`, `exposed_port`
- From OpenShift: `tls_termination`, `external_hostname`, `route_path`
- From ITIL: `ci_status`, `support_group`, `environment`

---

### Layer 4: Physical Infrastructure

**Primary Frameworks**: CIM, TOGAF, ITIL, ArchiMate, Cloud Providers

**Entity Types**:
- PhysicalServer (CIM, ArchiMate)
- VirtualMachine (CIM, ArchiMate)
- Hypervisor (CIM, ArchiMate)
- CloudInstance (AWS EC2, Azure VM, GCP Compute Engine)
- StorageArray (CIM)
- StorageVolume (CIM, AWS EBS, Azure Disk, GCP Persistent Disk)
- FileSystem (CIM)
- CloudStorageService (AWS RDS, Azure SQL, GCP Cloud SQL)
- ObjectStorageBucket (AWS S3, Azure Blob, GCP Cloud Storage)

**Key Attributes**:
- From CIM: `name`, `capacity`, `operating_system`, `resource_type`
- From ITIL: `asset_tag`, `serial_number`, `warranty_expiry`, `maintenance_window`
- From ArchiMate: `device_type`, `node_type`
- From Cloud Providers: `cloud_provider`, `region`, `availability_zone`, `instance_size`, `pricing_model`

---

### Layer 5: Network Topology and Communication Path

**Primary Frameworks**: CIM, TOGAF, ArchiMate, Cloud Providers

**Entity Types**:
- NetworkDevice (CIM, ArchiMate)
- LoadBalancer (CIM, AWS ELB, Azure LB, GCP Cloud LB)
- NetworkInterface (CIM)
- NetworkSegment (CIM, ArchiMate, AWS VPC, Azure VNet, GCP VPC)
- CommunicationPath (ArchiMate)
- NetworkRoute (ArchiMate, Cloud Providers)

**Key Attributes**:
- From CIM: `device_type`, `ip_address`, `protocol`, `port`
- From ArchiMate: `network_type`, `latency`, `throughput`, `path_type`
- From Cloud Providers: `cidr_block`, `load_balancer_scheme`, `dns_name`

---

### Layer 6: Security Infrastructure

**Primary Frameworks**: CIM, TOGAF, ITIL, Kubernetes, Cloud Providers

**Entity Types**:
- Firewall (CIM, Cloud Providers)
- WAF (Cloud Providers)
- Certificate (CIM, Kubernetes Secret)
- CertificateAuthority (CIM)
- SecurityPolicy (TOGAF, ITIL)
- IdentityProvider (Enterprise patterns)
- SecurityZone (TOGAF)

**Key Attributes**:
- From CIM: `security_type`, `trust_level`
- From Kubernetes: `tls_certificate`, `tls_key`
- From ITIL: `expiration_date`, `policy_rules`
- From Cloud Providers: `encryption_enabled`, `public_access_block`

---

## Cross-Framework Attribute Mapping

### Operational Management Attributes (All Layers)

| Attribute | TOGAF | CIM | ITIL | ArchiMate | K8s/OpenShift | Cloud |
|-----------|-------|-----|------|-----------|---------------|-------|
| `name` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `description` | ✓ | ✓ | - | ✓ | - | - |
| `owner` | ✓ | - | ✓ | - | - | - |
| `support_group` | - | - | ✓ | - | - | - |
| `lifecycle_status` | ✓ | ✓ | ✓ | - | ✓ | ✓ |
| `environment` | - | - | ✓ | - | ✓ | - |
| `tags/labels` | - | - | - | - | ✓ | ✓ |

### Resource Attributes (Layer 4)

| Attribute | TOGAF | CIM | ITIL | Cloud |
|-----------|-------|-----|------|-------|
| `capacity` | ✓ | ✓ | - | ✓ |
| `location` | ✓ | ✓ | - | ✓ |
| `operating_system` | ✓ | ✓ | - | ✓ |
| `asset_tag` | - | - | ✓ | - |
| `serial_number` | - | ✓ | ✓ | - |
| `warranty_expiry` | - | - | ✓ | - |
| `region` | - | - | - | ✓ |
| `availability_zone` | - | - | - | ✓ |

### Application Attributes (Layer 2)

| Attribute | TOGAF | ITIL | ArchiMate | Cloud |
|-----------|-------|------|-----------|-------|
| `version` | ✓ | - | - | ✓ |
| `application_type` | ✓ | - | - | - |
| `vendor` | - | ✓ | - | - |
| `license_type` | - | ✓ | - | - |
| `component_type` | - | - | ✓ | - |
| `interface_type` | - | - | ✓ | - |
| `endpoint_url` | - | - | ✓ | ✓ |
| `service_tier` | - | - | - | ✓ |

---

## Relationship Type Mapping

### Cross-Layer Relationships

| Relationship | Source Layer | Target Layer | Frameworks |
|--------------|--------------|--------------|------------|
| `fulfills` | Layer 1 | Layer 2 | TOGAF, ArchiMate |
| `uses` | Layer 2 | Layer 2 | TOGAF, ArchiMate |
| `deployed_as` | Layer 2 | Layer 3 | Kubernetes, OpenShift |
| `packaged_in` | Layer 2 | Layer 3 | Kubernetes |
| `runs_on` | Layer 3 | Layer 4 | CIM, Kubernetes |
| `hosted_on` | Layer 2 | Layer 4 | CIM, TOGAF |
| `communicates_via` | Layer 2 | Layer 5 | ArchiMate |
| `protected_by` | Any | Layer 6 | TOGAF, CIM |

### Intra-Layer Relationships

| Relationship | Layer | Frameworks |
|--------------|-------|------------|
| `part_of` | Layer 1 | TOGAF, ArchiMate |
| `depends_on` | Layer 2 | TOGAF, ArchiMate |
| `calls` | Layer 2 | ArchiMate |
| `exposes` | Layer 3 | Kubernetes |
| `routes_to` | Layer 3 | Kubernetes, OpenShift |
| `allocated_from` | Layer 4 | CIM |
| `connected_to` | Layer 5 | CIM, ArchiMate |
| `routes_through` | Layer 5 | ArchiMate |

---

## Deployment Pattern Support

### Containerized Applications

**Supported by**: Kubernetes, OpenShift, Cloud Providers (ECS, AKS, GKE)

**Decomposition Path**: Business Process → Application → Container → Pod → Node → Physical/Cloud Infrastructure

**Key Attributes**:
- Container orchestration: `replica_count`, `resource_limits`, `orchestration_platform`
- Networking: `service_type`, `exposed_port`, `external_hostname`
- Storage: `volume_mounts`, `persistent_volume_claim`

### Legacy Applications

**Supported by**: TOGAF, CIM, ITIL, ArchiMate

**Decomposition Path**: Business Process → Application → ApplicationServer → VM → Physical Server

**Key Attributes**:
- Application server: `runtime_environment`, `software_type`
- Infrastructure: `operating_system`, `capacity`, `location`
- Management: `support_group`, `maintenance_window`

### Cloud-Native Applications

**Supported by**: AWS, Azure, GCP, Kubernetes

**Decomposition Path**: Business Process → Application → Cloud Service

**Key Attributes**:
- Cloud: `cloud_provider`, `region`, `service_tier`
- Managed services: `engine_type`, `multi_az`, `backup_retention_days`
- Serverless: `pricing_model`, `resource_limits`

### Hybrid Deployments

**Supported by**: All frameworks

**Decomposition Path**: Multiple paths across on-premises and cloud

**Key Attributes**:
- Deployment model: `resource_type` (physical, virtual, cloud_iaas, cloud_paas)
- Location: `location`, `region`, `availability_zone`
- Integration: `endpoint_url`, `protocol`, `authentication_method`

---

## Framework Gaps and Recommendations

### Identified Gaps

1. **Container Storage**: Limited coverage in TOGAF/CIM for container-specific storage patterns
   - **Recommendation**: Adopt Kubernetes PersistentVolume model

2. **Serverless Computing**: Not well-represented in traditional frameworks
   - **Recommendation**: Use cloud provider attributes with `resource_type: cloud_paas`

3. **API Management**: Limited formal modeling in TOGAF/CIM
   - **Recommendation**: Adopt ArchiMate Application Interface model

4. **Multi-Cloud**: No standard for multi-cloud attribute mapping
   - **Recommendation**: Use `cloud_provider` attribute with provider-specific extensions

5. **DevOps Tooling**: CI/CD pipelines not covered
   - **Recommendation**: Extend Layer 3 with build/deployment entities (out of scope for initial ontology)

### Complementary Attributes

Each framework provides unique value:
- **TOGAF**: Enterprise architecture alignment, business context
- **CIM**: Technical precision, infrastructure modeling
- **ITIL**: Operational management, service lifecycle
- **ArchiMate**: Relationship semantics, interface specifications
- **Kubernetes/OpenShift**: Container orchestration, cloud-native patterns
- **Cloud Providers**: Cloud-specific attributes, managed services

---

## Next Steps

1. **Update Design Document**: Integrate framework attributes into entity type specifications
2. **Create Attribute Catalog**: Comprehensive list of all attributes with framework sources
3. **Define Validation Rules**: SHACL shapes for framework-sourced attributes
4. **Develop Mapping Tables**: Detailed mappings for CMDB integration
5. **Create Sample Data**: Instance examples using framework attributes

---

**Document Status**: Complete
**Last Updated**: 2025-11-09
