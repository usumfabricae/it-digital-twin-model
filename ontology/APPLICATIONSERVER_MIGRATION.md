# ApplicationServer Migration: Layer 2 → Layer 4

## Summary

**Date**: 2024-01-01  
**Change Type**: Architectural Refactoring  
**Impact**: Medium - Affects class hierarchy, relationships, and documentation

## Rationale

ApplicationServer has been moved from Layer 2 (Application Layer) to Layer 4 (Physical Infrastructure Layer) to better align with its role as runtime infrastructure that manages applications, similar to how:
- Hypervisors manage virtual machines
- Container orchestrators (Kubernetes) manage containers

## Changes Made

### 1. Ontology Class Definition
**File**: `ontology/it-infrastructure-ontology.ttl`

**Before**:
```turtle
:ApplicationServer
  rdf:type owl:Class ;
  rdfs:subClassOf :ApplicationLayer ;
```

**After**:
```turtle
:ApplicationServer
  rdf:type owl:Class ;
  rdfs:subClassOf :PhysicalInfrastructureLayer ;
```

**Updated Definition**:
- Changed comment from "A runtime environment for hosting applications" to "Runtime infrastructure that hosts and manages applications"
- Enhanced definition to explicitly compare with hypervisors and container orchestrators
- Added examples: Nginx, Apache (in addition to WebSphere, WebLogic, JBoss, Tomcat, IIS)

### 2. SHACL Validation Shapes
**File**: `ontology/shacl-shapes.ttl`

**Added**: ApplicationServerShape in Layer 4 section with validation rule requiring `runs_on` relationship:
```turtle
:ApplicationServerShape
  a sh:NodeShape ;
  sh:targetClass :ApplicationServer ;
  sh:property [
    sh:path :runs_on ;
    sh:minCount 1 ;
    sh:message "ApplicationServer must run on infrastructure (VM, PhysicalServer, or CloudInstance)" ;
  ] .
```

### 3. Documentation Updates

#### README.md
- Removed ApplicationServer from Layer 2 entity list
- Added ApplicationServer to Layer 4 entity list with note: "(runtime infrastructure for hosting applications)"

#### Layer 2 Specification (layer2-application-specification.md)
- Removed entire ApplicationServer section (was section 3)
- Renumbered subsequent sections:
  - Service: 4 → 3
  - API: 5 → 4
  - Database: 6 → 5
  - DatabaseInstance: 7 → 6
  - DataObject: 8 → 7
  - FileStorageService: 9 → 8
  - ObjectStorageService: 10 → 9
  - CacheService: 11 → 10
  - MessageQueue: 12 → 11

#### Layer 4 Specification (layer4-physical-infrastructure.md)
- Added ApplicationServer as section 6 (after CloudService, before Storage Infrastructure)
- Included comprehensive definition with design rationale
- Documented relationships to other layers
- Renumbered storage sections:
  - StorageArray: 6 → 7
  - StorageVolume: 7 → 8
  - FileSystem: 8 → 9
  - StoragePool: 9 → 10
  - CloudStorageService: 10 → 11
  - ObjectStorageBucket: 11 → 12

### 4. Relationships

**Preserved Relationships**:
- `deployed_on` / `hosts_component` - ApplicationComponent to ApplicationServer (unchanged)
- `runs_on` / `hosts` - ApplicationServer to infrastructure (already supported in domain/range)

**Relationship Semantics**:
```turtle
# Cross-layer: Application to Infrastructure
:Application :hosted_on :ApplicationServer .
:ApplicationComponent :deployed_on :ApplicationServer .

# Intra-layer: ApplicationServer to compute infrastructure
:ApplicationServer :runs_on :VirtualMachine .
:ApplicationServer :runs_on :PhysicalServer .
:ApplicationServer :runs_on :CloudInstance .
```

## Design Rationale

### Why Layer 4 (Infrastructure)?

1. **Functional Similarity to Orchestrators**:
   - **Lifecycle Management**: Start, stop, restart applications
   - **Resource Allocation**: CPU, memory, thread pools
   - **Health Monitoring**: Application health checks and recovery
   - **Service Discovery**: Networking and load balancing
   - **Deployment Orchestration**: Application deployment and updates

2. **Consistency with Existing Model**:
   - Hypervisor (Layer 4) manages VMs
   - Cluster/Kubernetes (Layer 3) manages Containers
   - ApplicationServer (Layer 4) manages Applications

3. **Clearer Decomposition Chain**:
   ```
   BusinessProcess → Application → ApplicationServer → VM → PhysicalServer
   ```
   vs previous ambiguous:
   ```
   BusinessProcess → Application → ApplicationServer (same layer?) → VM → PhysicalServer
   ```

4. **Infrastructure Characteristics**:
   - Provides platform services (not business logic)
   - Manages resources and runtime environment
   - Acts as hosting infrastructure for applications
   - Configured and managed by operations teams

### Why Not Layer 2 (Application)?

Layer 2 should contain:
- **Business Logic**: Applications, Services, APIs
- **Data Services**: Databases, Caches, Message Queues
- **Logical Components**: ApplicationComponents, DataObjects

ApplicationServer doesn't fit these categories - it's infrastructure that *hosts* these components.

### Why Not Layer 3 (Container)?

Layer 3 is specifically for containerization and orchestration technologies. ApplicationServer predates containers and serves a different (though analogous) purpose. Keeping it in Layer 4 maintains:
- Clear separation between container-based and traditional deployment models
- Flexibility for hybrid architectures
- Alignment with legacy infrastructure patterns

## Impact Analysis

### Breaking Changes
**None** - This is a semantic reorganization that doesn't break existing instance data or queries.

### Sample Data Updates Required
Instance data files that reference ApplicationServer should be reviewed to ensure:
1. ApplicationServer instances use `runs_on` to connect to infrastructure
2. Applications use `hosted_on` to connect to ApplicationServer
3. ApplicationComponents use `deployed_on` to connect to ApplicationServer

### Query Pattern Updates
Queries traversing from Application to Infrastructure should now include ApplicationServer:

**Before** (if ApplicationServer was bypassed):
```sparql
?app :hosted_on ?vm .
```

**After** (explicit ApplicationServer):
```sparql
?app :hosted_on ?appServer .
?appServer :runs_on ?vm .
```

## Validation

### SHACL Validation
All ApplicationServer instances must now:
- Have `rdfs:subClassOf :PhysicalInfrastructureLayer`
- Have at least one `runs_on` relationship to infrastructure
- Have valid `server_type` from enumeration
- Have valid `lifecycle_status` from enumeration

### Sample Data Validation
Run validation on all sample data files:
```bash
pyshacl -s ontology/shacl-shapes.ttl -d ontology/sample-data-*.ttl
```

## Migration Checklist

- [x] Update class definition in main ontology
- [x] Update SHACL shapes
- [x] Update README.md
- [x] Update Layer 2 specification
- [x] Update Layer 4 specification
- [x] Document design rationale
- [ ] Validate sample data files
- [ ] Update query pattern documentation
- [ ] Update deployment pattern examples
- [ ] Review and update any external documentation

## Benefits

1. **Conceptual Clarity**: ApplicationServer is now clearly positioned as infrastructure
2. **Consistency**: Aligns with how other runtime platforms (Hypervisor, Cluster) are modeled
3. **Better Queries**: Enables cleaner decomposition queries from business to infrastructure
4. **Modern Architecture**: Reflects cloud-native thinking where app servers are infrastructure components
5. **Extensibility**: Makes it easier to add new runtime platforms (e.g., serverless runtimes)

## References

- Original discussion: User feedback on ApplicationServer placement
- Related entities: Hypervisor (Layer 4), Cluster (Layer 3)
- Framework sources: CIM ApplicationSystem, TOGAF Technology Architecture
