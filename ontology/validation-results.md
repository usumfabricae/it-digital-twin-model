# SHACL Validation Results

## Summary

Initial validation run identified **26 constraint violations** across 4 sample data scenarios.

### Validation Statistics

| Scenario | Status | Violations |
|----------|--------|------------|
| On-Premises Infrastructure | ❌ FAIL | 3 |
| Cloud Infrastructure (AWS) | ❌ FAIL | 6 |
| Containerized Applications (Kubernetes/OpenShift) | ❌ FAIL | 11 |
| Hybrid Infrastructure | ❌ FAIL | 6 |
| **Total** | **0/4 passed** | **26** |

## Violation Categories

### 1. Missing Mandatory Attributes

**Issue**: ApplicationServer and Service entities are missing required `application_type` and `deployment_model` attributes.

**Affected Entities**:
- `inst:WebSphereAppServer` (On-Premises)
- `inst:JBossAppServer` (Hybrid)
- `inst:CustomerAPIService` (Cloud)
- `inst:PaymentGatewayService`, `inst:OrderService` (Containerized)

**Root Cause**: The SHACL shapes define ApplicationShape with mandatory `application_type` and `deployment_model`, but these apply to both Application and Service classes (Service is a subclass of ApplicationLayer).

**Resolution**: Add the missing attributes to all Service and ApplicationServer instances.

### 2. Invalid Enumeration Values

**Issue**: Database `lifecycle_status` value "active" is not in the allowed enumeration list.

**Affected Entities**:
- `inst:PaymentDatabase` (Containerized)

**Allowed Values**: development, testing, staging, production, deprecated, retired

**Resolution**: Change `lifecycle_status` from "active" to "production" for database instances.

### 3. Missing Relationship Constraints

**Issue**: CommunicationPath entities must route through at least one network device.

**Affected Entities**:
- `inst:CommPath03`, `inst:CommPath04`, `inst:CommPath05` (Cloud)
- `inst:CommPath06`, `inst:CommPath07`, `inst:CommPath08` (Containerized)
- `inst:HybridCommPath02` (Hybrid)

**Resolution**: Add `:routes_through` relationships to network devices for all communication paths.

### 4. Certificate Expiration Validation

**Issue**: Active certificates have expiration dates in the past (2025-01-01 is before current date 2025-11-12).

**Affected Entities**:
- `inst:ERPCertificate` (On-Premises)
- `inst:ACMCertificate` (Cloud)
- `inst:PaymentCertificate` (Containerized)
- `inst:HybridCertificate` (Hybrid)

**Resolution**: Update certificate expiration dates to future dates (e.g., 2026-01-01).

## Detailed Violation Analysis

### On-Premises Infrastructure (3 violations)

1. **WebSphereAppServer missing application_type**
   - Entity: `inst:WebSphereAppServer`
   - Type: ApplicationServer
   - Missing: `:application_type` property
   - Fix: Add `:application_type "legacy"`

2. **WebSphereAppServer missing deployment_model**
   - Entity: `inst:WebSphereAppServer`
   - Type: ApplicationServer
   - Missing: `:deployment_model` property
   - Fix: Add `:deployment_model "vm_based"`

3. **ERPCertificate expired**
   - Entity: `inst:ERPCertificate`
   - Type: Certificate
   - Issue: Expiration date 2025-01-01 < NOW()
   - Fix: Update `:expiration_date` and `:valid_to` to "2026-01-01T00:00:00Z"

### Cloud Infrastructure (6 violations)

1-2. **CustomerAPIService missing application_type and deployment_model**
   - Entity: `inst:CustomerAPIService`
   - Type: Service
   - Fix: Add `:application_type "microservice"` and `:deployment_model "cloud_managed"`

3-5. **Communication paths missing routes_through**
   - Entities: `inst:CommPath03`, `inst:CommPath04`, `inst:CommPath05`
   - Type: CommunicationPath
   - Fix: Add `:routes_through` relationships to appropriate network devices

6. **ACMCertificate expired**
   - Entity: `inst:ACMCertificate`
   - Fix: Update expiration date to 2026-01-01

### Containerized Applications (11 violations)

1-6. **Services and Database missing application_type and deployment_model**
   - Entities: `inst:PaymentGatewayService`, `inst:OrderService`, `inst:PaymentDatabase`
   - Fix: Add required attributes

7. **PaymentDatabase invalid lifecycle_status**
   - Entity: `inst:PaymentDatabase`
   - Current: "active"
   - Fix: Change to "production"

8-10. **Communication paths missing routes_through**
   - Entities: `inst:CommPath06`, `inst:CommPath07`, `inst:CommPath08`
   - Fix: Add network device relationships

11. **PaymentCertificate expired**
   - Entity: `inst:PaymentCertificate`
   - Fix: Update expiration date to 2026-04-01

### Hybrid Infrastructure (6 violations)

1-4. **JBossAppServer and InventoryAnalyticsService missing attributes**
   - Entities: `inst:JBossAppServer`, `inst:InventoryAnalyticsService`
   - Fix: Add `application_type` and `deployment_model`

5. **HybridCommPath02 missing routes_through**
   - Entity: `inst:HybridCommPath02`
   - Fix: Add network device relationship

6. **HybridCertificate expired**
   - Entity: `inst:HybridCertificate`
   - Fix: Update expiration date to 2026-01-01

## Recommendations

### 1. Schema Refinement

The SHACL shapes may be too strict for certain entity types:
- **ApplicationServer**: Consider whether ApplicationServer should have `application_type` and `deployment_model`, or if these should only apply to Application entities
- **Service vs Application**: Clarify whether Service entities need the same attributes as Application entities

### 2. Data Quality Improvements

- Implement automated date validation to ensure certificates don't have past expiration dates
- Add validation for network topology completeness (all communication paths must have routing information)
- Consider adding warnings for entities missing optional but recommended attributes

### 3. Documentation Updates

- Update sample data creation guidelines to include all mandatory attributes
- Provide templates for each entity type with required and optional attributes
- Document common validation errors and their resolutions

## Next Steps

1. ✅ Fix all identified violations in sample data files
2. ✅ Re-run validation to confirm all issues resolved
3. ✅ Document validation process and results
4. ✅ Create validation report for stakeholders


## Final Validation Results

### Summary After Fixes

| Scenario | Status | Remaining Issues |
|----------|--------|------------------|
| On-Premises Infrastructure | ✅ PASS | 0 |
| Cloud Infrastructure (AWS) | ✅ PASS | 0 |
| Containerized Applications (Kubernetes/OpenShift) | ⚠️ PARTIAL | 1 (SHACL design issue) |
| Hybrid Infrastructure | ✅ PASS | 0 |
| **Total** | **3/4 fully passed** | **1 known issue** |

### Remaining Issue: SHACL Shape Conflict

**Issue**: Database entity has conflicting lifecycle_status validation rules

**Details**:
- ApplicationShape requires: development, testing, staging, production, deprecated, retired
- DatabaseShape requires: active, maintenance, failed, retired
- Since Database is a subclass of ApplicationLayer, both shapes are applied
- This creates an impossible validation scenario

**Root Cause**: SHACL shape design issue where:
1. ApplicationShape targets `:Application` class
2. Database is a subclass of ApplicationLayer
3. The SHACL validator applies ApplicationShape to all ApplicationLayer subclasses
4. DatabaseShape has different lifecycle_status values than ApplicationShape

**Recommended Solutions**:
1. **Option A**: Modify ApplicationShape to only target Application entities, not all ApplicationLayer entities
2. **Option B**: Align lifecycle_status enumerations across all ApplicationLayer entity types
3. **Option C**: Remove lifecycle_status from ApplicationShape and define it separately for each entity type

**Workaround**: For sample data validation purposes, this is documented as a known SHACL design issue. The sample data is otherwise valid and demonstrates all required ontology features.

### Validation Metrics

- **Total Violations Fixed**: 25 out of 26 (96% resolution rate)
- **Scenarios Fully Validated**: 3 out of 4 (75%)
- **Sample Data Quality**: High - all mandatory attributes present, relationships defined, cross-layer dependencies modeled

### Files Created

1. `sample-data-onpremises.ttl` - 290 triples, ✅ validated
2. `sample-data-cloud.ttl` - 306 triples, ✅ validated
3. `sample-data-containerized.ttl` - 410 triples, ⚠️ 1 SHACL design issue
4. `sample-data-hybrid.ttl` - 378 triples, ✅ validated
5. `validate_sample_data.py` - Python validation script
6. `validation-results.md` - This document

**Total Sample Data**: 1,384 triples across 4 comprehensive scenarios covering all 6 ontology layers
