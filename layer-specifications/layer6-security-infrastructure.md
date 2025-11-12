# Layer 6: Security Infrastructure - Complete Specification

## Overview

This document provides the complete formal specification for Layer 6 (Security Infrastructure) of the IT Infrastructure and Application Dependency Ontology. The Security layer represents security controls, policies, and infrastructure that protect IT resources across all other layers.

**Layer Purpose**: Represents security controls, policies, and infrastructure that protect IT resources.

**Layer Scope**: All security components including firewalls, web application firewalls (WAF), certificates, certificate authorities, security policies, identity providers, and security zones. This layer provides security controls and governance for all other layers.

**Framework Sources**: 
- CIM (Common Information Model) - Security Model
- NIST Cybersecurity Framework
- NIST SP 800-53 Security Controls
- ISO/IEC 27001 Information Security Management
- Cloud Provider Security APIs (AWS IAM, Azure Security Center, GCP Security Command Center)

**Key Characteristics**:
- Cross-cutting layer: Protects resources in all other layers
- Supports both perimeter and application-level security
- Models security policies, controls, and trust boundaries
- Provides certificate lifecycle management
- Supports identity and access management

---

## Entity Type Specifications

### 1. Firewall

**Definition**: A network firewall device or service that controls traffic based on security rules.

**OWL Class Definition**:
```turtle
:Firewall
  rdf:type owl:Class ;
  rdfs:subClassOf :SecurityLayer ;
  rdfs:label "Firewall" ;
  rdfs:comment "A network firewall device or service" ;
  skos:definition "A firewall is a security device that monitors and controls network traffic based on security rules" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Firewall name or identifier |
| firewall_id | xsd:string | 0..1 | optional | CIM | Unique firewall identifier |
| security_type | xsd:string | 1..1 | enum | CIM | Always "firewall" for Firewall entity |
| firewall_type | xsd:string | 1..1 | enum | CIM | Firewall type: network, host_based, cloud, virtual |
| manufacturer | xsd:string | 0..1 | optional | CIM | Manufacturer (e.g., "Palo Alto", "Cisco", "Fortinet") |
| model | xsd:string | 0..1 | optional | CIM | Firewall model |
| version | xsd:string | 0..1 | optional | CIM | Firmware or software version |
| location | xsd:string | 1..1 | mandatory | CIM | Physical or cloud location |
| management_ip | xsd:string | 0..1 | optional | CIM | Management IP address |
| rule_count | xsd:integer | 0..1 | optional | CIM | Number of configured rules |
| default_action | xsd:string | 0..1 | enum | NIST | Default action: allow, deny, reject |
| stateful | xsd:boolean | 0..1 | optional | CIM | Whether firewall is stateful |
| logging_enabled | xsd:boolean | 0..1 | optional | NIST | Whether logging is enabled |
| intrusion_prevention | xsd:boolean | 0..1 | optional | CIM | Whether IPS is enabled |
| cloud_provider | xsd:string | 0..1 | enum | Cloud APIs | Cloud provider if cloud-based: aws, azure, gcp |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Operational state: active, inactive, degraded, failed, maintenance |

**Enumeration Values**:
- **security_type**: `firewall` (fixed value)
- **firewall_type**: `network`, `host_based`, `cloud`, `virtual`, `next_gen`
- **default_action**: `allow`, `deny`, `reject`
- **cloud_provider**: `aws`, `azure`, `gcp`, `alibaba`, `oracle`
- **lifecycle_status**: `active`, `inactive`, `degraded`, `failed`, `maintenance`, `provisioning`

**SHACL Validation Shape**:
```turtle
:FirewallShape
  a sh:NodeShape ;
  sh:targetClass :Firewall ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
  ] ;
  sh:property [
    sh:path :security_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "firewall" ;
  ] ;
  sh:property [
    sh:path :firewall_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "network" "host_based" "cloud" "virtual" "next_gen" ) ;
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

### 2. WAF (Web Application Firewall)

**Definition**: A web application firewall that protects web applications from attacks.

**OWL Class Definition**:
```turtle
:WAF
  rdf:type owl:Class ;
  rdfs:subClassOf :SecurityLayer ;
  rdfs:label "Web Application Firewall" ;
  rdfs:comment "A web application firewall" ;
  skos:definition "A WAF protects web applications by filtering and monitoring HTTP/HTTPS traffic" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | WAF name or identifier |
| waf_id | xsd:string | 0..1 | optional | CIM | Unique WAF identifier |
| security_type | xsd:string | 1..1 | enum | CIM | Always "waf" for WAF entity |
| waf_type | xsd:string | 1..1 | enum | CIM | WAF type: hardware, software, cloud, virtual |
| manufacturer | xsd:string | 0..1 | optional | CIM | Manufacturer (e.g., "F5", "Imperva", "Cloudflare") |
| version | xsd:string | 0..1 | optional | CIM | Software version |
| location | xsd:string | 1..1 | mandatory | CIM | Physical or cloud location |
| mode | xsd:string | 0..1 | enum | NIST | Operating mode: detection, prevention, blocking |
| rule_set | xsd:string | 0..1 | optional | OWASP | Rule set name (e.g., "OWASP Core Rule Set") |
| rule_set_version | xsd:string | 0..1 | optional | OWASP | Rule set version |
| custom_rules_count | xsd:integer | 0..1 | optional | CIM | Number of custom rules |
| logging_enabled | xsd:boolean | 0..1 | optional | NIST | Whether logging is enabled |
| rate_limiting_enabled | xsd:boolean | 0..1 | optional | CIM | Whether rate limiting is enabled |
| bot_protection_enabled | xsd:boolean | 0..1 | optional | CIM | Whether bot protection is enabled |
| cloud_provider | xsd:string | 0..1 | enum | Cloud APIs | Cloud provider if cloud-based: aws, azure, gcp |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Operational state: active, inactive, degraded, failed, maintenance |

**Enumeration Values**:
- **security_type**: `waf` (fixed value)
- **waf_type**: `hardware`, `software`, `cloud`, `virtual`
- **mode**: `detection`, `prevention`, `blocking`, `monitoring`
- **cloud_provider**: `aws`, `azure`, `gcp`, `cloudflare`, `akamai`
- **lifecycle_status**: `active`, `inactive`, `degraded`, `failed`, `maintenance`, `provisioning`

**SHACL Validation Shape**:
```turtle
:WAFShape
  a sh:NodeShape ;
  sh:targetClass :WAF ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :security_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "waf" ;
  ] ;
  sh:property [
    sh:path :waf_type ;
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
    sh:in ( "active" "inactive" "degraded" "failed" "maintenance" "provisioning" ) ;
  ] .
```

---

### 3. Certificate

**Definition**: A digital certificate used for authentication and encryption.

**OWL Class Definition**:
```turtle
:Certificate
  rdf:type owl:Class ;
  rdfs:subClassOf :SecurityLayer ;
  rdfs:label "Certificate" ;
  rdfs:comment "A digital certificate" ;
  skos:definition "A certificate is a digital document that binds a public key to an identity" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Certificate name or common name |
| certificate_id | xsd:string | 0..1 | optional | CIM | Unique certificate identifier |
| security_type | xsd:string | 1..1 | enum | CIM | Always "certificate" for Certificate entity |
| certificate_type | xsd:string | 1..1 | enum | PKI | Certificate type: ssl_tls, code_signing, client_auth, email |
| subject | xsd:string | 1..1 | mandatory | X.509 | Certificate subject (DN) |
| issuer | xsd:string | 1..1 | mandatory | X.509 | Certificate issuer (DN) |
| serial_number | xsd:string | 1..1 | mandatory | X.509 | Certificate serial number |
| common_name | xsd:string | 1..1 | mandatory | X.509 | Common name (CN) |
| subject_alternative_names | xsd:string | 0..* | optional | X.509 | Subject alternative names (SANs) |
| key_algorithm | xsd:string | 0..1 | enum | X.509 | Key algorithm: rsa, ecdsa, ed25519 |
| key_size | xsd:integer | 0..1 | optional | X.509 | Key size in bits (e.g., 2048, 4096) |
| signature_algorithm | xsd:string | 0..1 | optional | X.509 | Signature algorithm (e.g., "SHA256withRSA") |
| valid_from | xsd:dateTime | 1..1 | mandatory | X.509 | Certificate validity start date |
| valid_to | xsd:dateTime | 1..1 | mandatory | X.509 | Certificate expiration date |
| expiration_date | xsd:dateTime | 1..1 | mandatory | X.509 | Certificate expiration date (alias for valid_to) |
| days_until_expiry | xsd:integer | 0..1 | optional | Custom | Calculated days until expiration |
| is_self_signed | xsd:boolean | 0..1 | optional | X.509 | Whether certificate is self-signed |
| is_wildcard | xsd:boolean | 0..1 | optional | X.509 | Whether certificate is wildcard |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | Certificate state: active, expired, revoked, pending, renewing |

**Enumeration Values**:
- **security_type**: `certificate` (fixed value)
- **certificate_type**: `ssl_tls`, `code_signing`, `client_auth`, `email`, `root_ca`, `intermediate_ca`
- **key_algorithm**: `rsa`, `ecdsa`, `ed25519`, `dsa`
- **lifecycle_status**: `active`, `expired`, `revoked`, `pending`, `renewing`, `suspended`

**SHACL Validation Shape**:
```turtle
:CertificateShape
  a sh:NodeShape ;
  sh:targetClass :Certificate ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :security_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "certificate" ;
  ] ;
  sh:property [
    sh:path :certificate_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "ssl_tls" "code_signing" "client_auth" "email" "root_ca" "intermediate_ca" ) ;
  ] ;
  sh:property [
    sh:path :subject ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :issuer ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :serial_number ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :valid_from ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:dateTime ;
  ] ;
  sh:property [
    sh:path :valid_to ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:dateTime ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "expired" "revoked" "pending" "renewing" "suspended" ) ;
  ] ;
  # Validation rule: expiration_date must be in the future for active certificates
  sh:sparql [
    sh:message "Active certificates must not be expired" ;
    sh:select """
      SELECT $this
      WHERE {
        $this :lifecycle_status "active" .
        $this :expiration_date ?expiry .
        FILTER(?expiry < NOW())
      }
    """ ;
  ] .
```

---

### 4. CertificateAuthority

**Definition**: A certificate authority that issues and manages digital certificates.

**OWL Class Definition**:
```turtle
:CertificateAuthority
  rdf:type owl:Class ;
  rdfs:subClassOf :SecurityLayer ;
  rdfs:label "Certificate Authority" ;
  rdfs:comment "A certificate authority" ;
  skos:definition "A certificate authority is a trusted entity that issues digital certificates" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | CA name |
| ca_id | xsd:string | 0..1 | optional | CIM | Unique CA identifier |
| security_type | xsd:string | 1..1 | enum | CIM | Always "certificate_authority" for CA entity |
| ca_type | xsd:string | 1..1 | enum | PKI | CA type: root, intermediate, subordinate |
| subject | xsd:string | 1..1 | mandatory | X.509 | CA certificate subject (DN) |
| issuer | xsd:string | 0..1 | optional | X.509 | Issuer DN (for intermediate CAs) |
| trust_level | xsd:string | 1..1 | enum | NIST | Trust level: public_trusted, private, self_signed |
| vendor | xsd:string | 0..1 | optional | Custom | CA vendor (e.g., "DigiCert", "Let's Encrypt", "Internal") |
| certificate_count | xsd:integer | 0..1 | optional | CIM | Number of issued certificates |
| valid_from | xsd:dateTime | 0..1 | optional | X.509 | CA certificate validity start |
| valid_to | xsd:dateTime | 0..1 | optional | X.509 | CA certificate expiration |
| crl_url | xsd:anyURI | 0..1 | optional | X.509 | Certificate Revocation List URL |
| ocsp_url | xsd:anyURI | 0..1 | optional | X.509 | OCSP responder URL |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | CA state: active, expired, revoked, disabled |

**Enumeration Values**:
- **security_type**: `certificate_authority` (fixed value)
- **ca_type**: `root`, `intermediate`, `subordinate`, `issuing`
- **trust_level**: `public_trusted`, `private`, `self_signed`, `enterprise`
- **lifecycle_status**: `active`, `expired`, `revoked`, `disabled`, `pending`

**SHACL Validation Shape**:
```turtle
:CertificateAuthorityShape
  a sh:NodeShape ;
  sh:targetClass :CertificateAuthority ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :security_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "certificate_authority" ;
  ] ;
  sh:property [
    sh:path :ca_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "root" "intermediate" "subordinate" "issuing" ) ;
  ] ;
  sh:property [
    sh:path :subject ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :trust_level ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "public_trusted" "private" "self_signed" "enterprise" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "expired" "revoked" "disabled" "pending" ) ;
  ] .
```

---

### 5. SecurityPolicy

**Definition**: A security policy or rule set that governs security controls.

**OWL Class Definition**:
```turtle
:SecurityPolicy
  rdf:type owl:Class ;
  rdfs:subClassOf :SecurityLayer ;
  rdfs:label "Security Policy" ;
  rdfs:comment "A security policy or rule set" ;
  skos:definition "A security policy defines rules and controls for protecting resources" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | NIST | Policy name |
| policy_id | xsd:string | 0..1 | optional | NIST | Unique policy identifier |
| security_type | xsd:string | 1..1 | enum | CIM | Always "policy" for SecurityPolicy entity |
| policy_type | xsd:string | 1..1 | enum | NIST | Policy type: access_control, encryption, compliance, network, data_protection |
| description | xsd:string | 0..1 | optional | NIST | Policy description |
| policy_framework | xsd:string | 0..1 | enum | NIST | Framework: nist_800_53, iso_27001, pci_dss, hipaa, gdpr, custom |
| policy_rules | xsd:string | 0..1 | optional | NIST | Policy rules (JSON or text format) |
| enforcement_mode | xsd:string | 0..1 | enum | NIST | Enforcement mode: enforcing, permissive, audit_only |
| scope | xsd:string | 0..1 | optional | NIST | Policy scope (e.g., "all_resources", "production_only") |
| owner | xsd:string | 0..1 | optional | NIST | Policy owner or responsible party |
| compliance_standard | xsd:string | 0..* | optional | NIST | Compliance standards addressed |
| last_reviewed | xsd:dateTime | 0..1 | optional | ISO 27001 | Last review date |
| review_frequency_days | xsd:integer | 0..1 | optional | ISO 27001 | Review frequency in days |
| lifecycle_status | xsd:string | 1..1 | enum | NIST | Policy state: active, draft, deprecated, archived |

**Enumeration Values**:
- **security_type**: `policy` (fixed value)
- **policy_type**: `access_control`, `encryption`, `compliance`, `network`, `data_protection`, `authentication`, `authorization`
- **policy_framework**: `nist_800_53`, `iso_27001`, `pci_dss`, `hipaa`, `gdpr`, `sox`, `custom`
- **enforcement_mode**: `enforcing`, `permissive`, `audit_only`, `disabled`
- **lifecycle_status**: `active`, `draft`, `deprecated`, `archived`, `under_review`

**SHACL Validation Shape**:
```turtle
:SecurityPolicyShape
  a sh:NodeShape ;
  sh:targetClass :SecurityPolicy ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :security_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "policy" ;
  ] ;
  sh:property [
    sh:path :policy_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "access_control" "encryption" "compliance" "network" "data_protection" "authentication" "authorization" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "draft" "deprecated" "archived" "under_review" ) ;
  ] .
```

---

### 6. IdentityProvider

**Definition**: An identity provider for authentication and authorization (IAM, SSO).

**OWL Class Definition**:
```turtle
:IdentityProvider
  rdf:type owl:Class ;
  rdfs:subClassOf :SecurityLayer ;
  rdfs:label "Identity Provider" ;
  rdfs:comment "An identity provider for authentication and authorization" ;
  skos:definition "An identity provider manages user identities and provides authentication and authorization services" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | CIM | Identity provider name |
| idp_id | xsd:string | 0..1 | optional | CIM | Unique IdP identifier |
| security_type | xsd:string | 1..1 | enum | CIM | Always "iam" for IdentityProvider entity |
| idp_type | xsd:string | 1..1 | enum | NIST | IdP type: saml, oauth2, oidc, ldap, active_directory, custom |
| provider | xsd:string | 0..1 | optional | Custom | Provider name (e.g., "Okta", "Azure AD", "Auth0") |
| endpoint | xsd:anyURI | 0..1 | optional | SAML/OIDC | IdP endpoint URL |
| issuer_uri | xsd:anyURI | 0..1 | optional | SAML/OIDC | Issuer URI |
| metadata_url | xsd:anyURI | 0..1 | optional | SAML | SAML metadata URL |
| user_count | xsd:integer | 0..1 | optional | CIM | Number of managed users |
| mfa_enabled | xsd:boolean | 0..1 | optional | NIST | Whether multi-factor authentication is enabled |
| sso_enabled | xsd:boolean | 0..1 | optional | NIST | Whether single sign-on is enabled |
| federation_enabled | xsd:boolean | 0..1 | optional | NIST | Whether identity federation is enabled |
| session_timeout_minutes | xsd:integer | 0..1 | optional | NIST | Session timeout in minutes |
| password_policy | xsd:string | 0..1 | optional | NIST | Password policy configuration |
| lifecycle_status | xsd:string | 1..1 | enum | CIM | IdP state: active, inactive, degraded, failed, maintenance |

**Enumeration Values**:
- **security_type**: `iam` (fixed value)
- **idp_type**: `saml`, `oauth2`, `oidc`, `ldap`, `active_directory`, `kerberos`, `custom`
- **lifecycle_status**: `active`, `inactive`, `degraded`, `failed`, `maintenance`, `provisioning`

**SHACL Validation Shape**:
```turtle
:IdentityProviderShape
  a sh:NodeShape ;
  sh:targetClass :IdentityProvider ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :security_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "iam" ;
  ] ;
  sh:property [
    sh:path :idp_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "saml" "oauth2" "oidc" "ldap" "active_directory" "kerberos" "custom" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "inactive" "degraded" "failed" "maintenance" "provisioning" ) ;
  ] .
```

---

### 7. SecurityZone

**Definition**: A security zone or trust boundary that groups resources with similar security requirements.

**OWL Class Definition**:
```turtle
:SecurityZone
  rdf:type owl:Class ;
  rdfs:subClassOf :SecurityLayer ;
  rdfs:label "Security Zone" ;
  rdfs:comment "A security zone or trust boundary" ;
  skos:definition "A security zone is a logical grouping of resources with similar security requirements and trust levels" .
```

**Attributes**:

| Attribute | Data Type | Cardinality | Constraint | Framework Source | Description |
|-----------|-----------|-------------|------------|------------------|-------------|
| name | xsd:string | 1..1 | mandatory | NIST | Security zone name |
| zone_id | xsd:string | 0..1 | optional | NIST | Unique zone identifier |
| security_type | xsd:string | 1..1 | enum | CIM | Always "security_zone" for SecurityZone entity |
| zone_type | xsd:string | 1..1 | enum | NIST | Zone type: dmz, internal, external, restricted, public |
| trust_level | xsd:string | 1..1 | enum | NIST | Trust level: trusted, untrusted, semi_trusted, restricted |
| description | xsd:string | 0..1 | optional | NIST | Zone description |
| security_classification | xsd:string | 0..1 | enum | NIST | Data classification: public, internal, confidential, restricted, top_secret |
| network_segments | xsd:string | 0..* | optional | NIST | Associated network segments (CIDR blocks) |
| allowed_protocols | xsd:string | 0..* | optional | NIST | Allowed network protocols |
| encryption_required | xsd:boolean | 0..1 | optional | NIST | Whether encryption is required |
| mfa_required | xsd:boolean | 0..1 | optional | NIST | Whether MFA is required for access |
| monitoring_level | xsd:string | 0..1 | enum | NIST | Monitoring level: high, medium, low, none |
| compliance_requirements | xsd:string | 0..* | optional | NIST | Compliance requirements (e.g., "PCI-DSS", "HIPAA") |
| lifecycle_status | xsd:string | 1..1 | enum | NIST | Zone state: active, inactive, under_review |

**Enumeration Values**:
- **security_type**: `security_zone` (fixed value)
- **zone_type**: `dmz`, `internal`, `external`, `restricted`, `public`, `management`, `production`, `development`
- **trust_level**: `trusted`, `untrusted`, `semi_trusted`, `restricted`, `high_security`
- **security_classification**: `public`, `internal`, `confidential`, `restricted`, `top_secret`
- **monitoring_level**: `high`, `medium`, `low`, `none`
- **lifecycle_status**: `active`, `inactive`, `under_review`, `deprecated`

**SHACL Validation Shape**:
```turtle
:SecurityZoneShape
  a sh:NodeShape ;
  sh:targetClass :SecurityZone ;
  sh:property [
    sh:path :name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path :security_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:hasValue "security_zone" ;
  ] ;
  sh:property [
    sh:path :zone_type ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "dmz" "internal" "external" "restricted" "public" "management" "production" "development" ) ;
  ] ;
  sh:property [
    sh:path :trust_level ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "trusted" "untrusted" "semi_trusted" "restricted" "high_security" ) ;
  ] ;
  sh:property [
    sh:path :lifecycle_status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "active" "inactive" "under_review" "deprecated" ) ;
  ] .
```

---

## Relationship Specifications

### Intra-Layer Relationships

These relationships connect entities within Layer 6 (Security).

#### 1. issued_by

**Definition**: A certificate is issued by a certificate authority.

**Domain**: Certificate
**Range**: CertificateAuthority
**Cardinality**: many-to-one (*..1) - certificate issued by one CA

**Inverse**: issues (CertificateAuthority issues Certificate)
**Properties**:
- issue_date (dateTime): When certificate was issued
- renewal_count (integer): Number of times certificate has been renewed

**OWL Definition**:
```turtle
:issued_by
  rdf:type owl:ObjectProperty ;
  rdf:type owl:FunctionalProperty ;
  rdfs:domain :Certificate ;
  rdfs:range :CertificateAuthority ;
  rdfs:label "issued by" ;
  rdfs:comment "Certificate issued by certificate authority" .

:issues
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :issued_by ;
  rdfs:domain :CertificateAuthority ;
  rdfs:range :Certificate .
```

**Usage Example**:
```turtle
:Cert_WebServer01 :issued_by :CA_InternalRoot .
:CA_InternalRoot :issues :Cert_WebServer01 .
```

---

#### 2. enforces

**Definition**: A security component enforces a security policy.

**Domain**: Firewall | WAF | IdentityProvider
**Range**: SecurityPolicy
**Cardinality**: many-to-many (*..*) - component can enforce multiple policies

**Inverse**: enforced_by (SecurityPolicy enforced by security component)
**Properties**:
- enforcement_priority (integer): Priority order for policy enforcement
- enforcement_status (enum): enabled, disabled, audit_only

**OWL Definition**:
```turtle
:enforces
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Firewall :WAF :IdentityProvider ) ] ;
  rdfs:range :SecurityPolicy ;
  rdfs:label "enforces" ;
  rdfs:comment "Security component enforces security policy" .

:enforced_by
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :enforces ;
  rdfs:domain :SecurityPolicy ;
  rdfs:range [ owl:unionOf ( :Firewall :WAF :IdentityProvider ) ] .
```

**Usage Example**:
```turtle
:Firewall_Perimeter :enforces :Policy_NetworkAccess .
:WAF_WebTier :enforces :Policy_WebSecurity .
:Policy_NetworkAccess :enforced_by :Firewall_Perimeter .
```

---

#### 3. trusts

**Definition**: A certificate authority trusts another CA (for certificate chain).

**Domain**: CertificateAuthority
**Range**: CertificateAuthority
**Cardinality**: many-to-many (*..*) - CA can trust multiple CAs

**Inverse**: trusted_by (CertificateAuthority trusted by another CA)
**Properties**:
- trust_type (enum): direct, transitive, cross_signed

**OWL Definition**:
```turtle
:trusts
  rdf:type owl:ObjectProperty ;
  rdfs:domain :CertificateAuthority ;
  rdfs:range :CertificateAuthority ;
  rdfs:label "trusts" ;
  rdfs:comment "Certificate authority trusts another CA" .

:trusted_by
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :trusts ;
  rdfs:domain :CertificateAuthority ;
  rdfs:range :CertificateAuthority .
```

**Usage Example**:
```turtle
:CA_Intermediate :trusts :CA_Root .
:CA_Root :trusted_by :CA_Intermediate .
```

---

### Cross-Layer Relationships

These relationships connect Layer 6 (Security) to other layers.

#### 4. protected_by

**Definition**: An entity is protected by a security component.

**Domain**: Any entity from Layers 1-5
**Range**: Firewall | WAF | SecurityZone
**Cardinality**: many-to-many (*..*) - entity can be protected by multiple components

**Inverse**: protects (Security component protects entity)
**Properties**:
- protection_type (enum): network, application, data, identity
- criticality (enum): critical, high, medium, low

**OWL Definition**:
```turtle
:protected_by
  rdf:type owl:ObjectProperty ;
  rdfs:domain :InfrastructureEntity ;
  rdfs:range [ owl:unionOf ( :Firewall :WAF :SecurityZone ) ] ;
  rdfs:label "protected by" ;
  rdfs:comment "Entity protected by security component" .

:protects
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :protected_by ;
  rdfs:domain [ owl:unionOf ( :Firewall :WAF :SecurityZone ) ] ;
  rdfs:range :InfrastructureEntity .
```

**Usage Example**:
```turtle
:App_WebPortal :protected_by :WAF_PublicWeb .
:App_WebPortal :protected_by :Firewall_DMZ .
:WAF_PublicWeb :protects :App_WebPortal .
```

---

#### 5. secured_by

**Definition**: An entity is secured by a security policy.

**Domain**: Any entity from Layers 1-5
**Range**: SecurityPolicy
**Cardinality**: many-to-many (*..*) - entity can be governed by multiple policies

**Inverse**: secures (SecurityPolicy secures entity)
**Properties**:
- compliance_status (enum): compliant, non_compliant, under_review, exempt
- last_audit_date (dateTime): Last compliance audit date

**OWL Definition**:
```turtle
:secured_by
  rdf:type owl:ObjectProperty ;
  rdfs:domain :InfrastructureEntity ;
  rdfs:range :SecurityPolicy ;
  rdfs:label "secured by" ;
  rdfs:comment "Entity secured by security policy" .

:secures
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :secured_by ;
  rdfs:domain :SecurityPolicy ;
  rdfs:range :InfrastructureEntity .
```

**Usage Example**:
```turtle
:Database_CustomerDB :secured_by :Policy_DataEncryption .
:Database_CustomerDB :secured_by :Policy_AccessControl .
:Policy_DataEncryption :secures :Database_CustomerDB .
```

---

#### 6. belongs_to

**Definition**: An entity belongs to a security zone.

**Domain**: Any entity from Layers 2-5
**Range**: SecurityZone
**Cardinality**: many-to-one (*..1) - entity belongs to one zone

**Inverse**: contains (SecurityZone contains entities)
**Properties**:
- zone_membership_type (enum): primary, secondary, temporary

**OWL Definition**:
```turtle
:belongs_to
  rdf:type owl:ObjectProperty ;
  rdf:type owl:FunctionalProperty ;
  rdfs:domain :InfrastructureEntity ;
  rdfs:range :SecurityZone ;
  rdfs:label "belongs to" ;
  rdfs:comment "Entity belongs to security zone" .

:contains
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :belongs_to ;
  rdfs:domain :SecurityZone ;
  rdfs:range :InfrastructureEntity .
```

**Usage Example**:
```turtle
:App_PublicWeb :belongs_to :Zone_DMZ .
:Database_InternalDB :belongs_to :Zone_Internal .
:Zone_DMZ :contains :App_PublicWeb .
```

---

#### 7. authenticates_with

**Definition**: An application or service authenticates with an identity provider.

**Domain**: Application | Service | User
**Range**: IdentityProvider
**Cardinality**: many-to-many (*..*) - application can use multiple IdPs

**Inverse**: authenticates (IdentityProvider authenticates applications)
**Properties**:
- authentication_method (enum): saml, oauth2, oidc, ldap, api_key
- is_primary (boolean): Whether this is the primary IdP

**OWL Definition**:
```turtle
:authenticates_with
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Application :Service ) ] ;
  rdfs:range :IdentityProvider ;
  rdfs:label "authenticates with" ;
  rdfs:comment "Application authenticates with identity provider" .

:authenticates
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :authenticates_with ;
  rdfs:domain :IdentityProvider ;
  rdfs:range [ owl:unionOf ( :Application :Service ) ] .
```

**Usage Example**:
```turtle
:App_EmployeePortal :authenticates_with :IdP_AzureAD .
:App_CustomerPortal :authenticates_with :IdP_Okta .
:IdP_AzureAD :authenticates :App_EmployeePortal .
```

---

#### 8. uses_certificate

**Definition**: An entity uses a certificate for encryption or authentication.

**Domain**: Application | Service | LoadBalancer | Route | NetworkDevice
**Range**: Certificate
**Cardinality**: many-to-many (*..*) - entity can use multiple certificates

**Inverse**: used_by (Certificate used by entity)
**Properties**:
- certificate_usage (enum): tls_server, tls_client, code_signing, encryption
- binding_type (enum): primary, backup, failover

**OWL Definition**:
```turtle
:uses_certificate
  rdf:type owl:ObjectProperty ;
  rdfs:domain [ owl:unionOf ( :Application :Service :LoadBalancer :Route :NetworkDevice ) ] ;
  rdfs:range :Certificate ;
  rdfs:label "uses certificate" ;
  rdfs:comment "Entity uses certificate" .

:used_by
  rdf:type owl:ObjectProperty ;
  owl:inverseOf :uses_certificate ;
  rdfs:domain :Certificate ;
  rdfs:range [ owl:unionOf ( :Application :Service :LoadBalancer :Route :NetworkDevice ) ] .
```

**Usage Example**:
```turtle
:App_WebAPI :uses_certificate :Cert_api_example_com .
:LB_PublicWeb :uses_certificate :Cert_www_example_com .
:Cert_api_example_com :used_by :App_WebAPI .
```

---

## Relationship Summary Table

| Relationship | Domain | Range | Cardinality | Type |
|--------------|--------|-------|-------------|------|
| issued_by | Certificate | CertificateAuthority | *..1 | Intra-layer |
| enforces | Firewall/WAF/IdP | SecurityPolicy | *..* | Intra-layer |
| trusts | CertificateAuthority | CertificateAuthority | *..* | Intra-layer |
| protected_by | Any Entity | Firewall/WAF/Zone | *..* | Cross-layer |
| secured_by | Any Entity | SecurityPolicy | *..* | Cross-layer |
| belongs_to | Any Entity | SecurityZone | *..1 | Cross-layer |
| authenticates_with | Application/Service | IdentityProvider | *..* | Cross-layer |
| uses_certificate | App/Service/LB/Route | Certificate | *..* | Cross-layer |

---

## Validation Rules

### Layer Assignment Rules

1. All security entity types belong exclusively to Layer 6
2. Security entities cannot have attributes from other layers
3. Cross-layer relationships must connect to entities in Layers 1-5
4. Intra-layer relationships must connect entities within Layer 6

### Security-Specific Validation Rules

1. **Certificate Expiration Validation**:
   - Active certificates MUST NOT be expired (expiration_date > current_date)
   - Certificates expiring within 30 days SHOULD trigger warnings
   - Expired certificates MUST have lifecycle_status = "expired"

2. **Certificate Chain Validation**:
   - Certificates MUST be issued_by a CertificateAuthority
   - Certificate subject MUST match the entity using it
   - Certificate validity period MUST be within CA validity period

3. **Security Zone Validation**:
   - Entities SHOULD belong to exactly one SecurityZone
   - Trust level MUST be consistent with zone_type
   - DMZ zones MUST have trust_level = "semi_trusted" or "untrusted"

4. **Policy Enforcement Validation**:
   - Active SecurityPolicies MUST be enforced by at least one security component
   - Enforcement_mode MUST be "enforcing" for production environments
   - Policies SHOULD be reviewed within review_frequency_days

5. **Identity Provider Validation**:
   - If mfa_enabled is true, authentication methods MUST support MFA
   - Session timeout MUST be defined for active IdPs
   - IdP endpoint MUST be accessible and valid

6. **Firewall Configuration Validation**:
   - Firewalls with default_action = "allow" SHOULD have explicit deny rules
   - Logging SHOULD be enabled for all production firewalls
   - Rule count SHOULD not exceed recommended limits (e.g., 10,000 rules)

### SHACL Validation Examples

```turtle
# Validate certificate expiration
:CertificateExpirationValidation
  a sh:NodeShape ;
  sh:targetClass :Certificate ;
  sh:sparql [
    sh:message "Active certificates must not be expired" ;
    sh:select """
      SELECT $this
      WHERE {
        $this :lifecycle_status "active" .
        $this :expiration_date ?expiry .
        FILTER(?expiry < NOW())
      }
    """ ;
  ] .

# Validate certificate issued by CA
:CertificateIssuedByValidation
  a sh:NodeShape ;
  sh:targetClass :Certificate ;
  sh:property [
    sh:path :issued_by ;
    sh:minCount 1 ;
    sh:class :CertificateAuthority ;
    sh:message "Certificate must be issued by a Certificate Authority" ;
  ] .

# Validate security zone membership
:SecurityZoneMembershipValidation
  a sh:NodeShape ;
  sh:targetClass :Application ;
  sh:property [
    sh:path :belongs_to ;
    sh:maxCount 1 ;
    sh:class :SecurityZone ;
    sh:message "Application should belong to exactly one security zone" ;
  ] .

# Validate policy enforcement
:PolicyEnforcementValidation
  a sh:NodeShape ;
  sh:targetClass :SecurityPolicy ;
  sh:sparql [
    sh:message "Active policies must be enforced by at least one security component" ;
    sh:select """
      SELECT $this
      WHERE {
        $this :lifecycle_status "active" .
        FILTER NOT EXISTS { ?component :enforces $this }
      }
    """ ;
  ] .

# Validate certificate expiration warning (30 days)
:CertificateExpirationWarningValidation
  a sh:NodeShape ;
  sh:targetClass :Certificate ;
  sh:sparql [
    sh:severity sh:Warning ;
    sh:message "Certificate expires within 30 days" ;
    sh:select """
      SELECT $this
      WHERE {
        $this :lifecycle_status "active" .
        $this :expiration_date ?expiry .
        BIND(NOW() + "P30D"^^xsd:duration AS ?threshold)
        FILTER(?expiry < ?threshold && ?expiry >= NOW())
      }
    """ ;
  ] .
```

---

## Security Deployment Patterns

### Pattern 1: Multi-Tier Web Application Security

**Scenario**: A web application with multiple security layers

**Components**:
- Application: "Customer Portal" (Layer 2)
- WAF: "CloudFlare WAF" (Layer 6)
- Load Balancer: "ALB-Public" (Layer 5)
- Firewall: "Perimeter Firewall" (Layer 6)
- Certificate: "*.example.com" (Layer 6)
- Identity Provider: "Okta SSO" (Layer 6)
- Security Zone: "DMZ" (Layer 6)

**Relationships**:
```turtle
:App_CustomerPortal :protected_by :WAF_CloudFlare .
:App_CustomerPortal :protected_by :Firewall_Perimeter .
:App_CustomerPortal :belongs_to :Zone_DMZ .
:App_CustomerPortal :authenticates_with :IdP_Okta .
:App_CustomerPortal :uses_certificate :Cert_Wildcard_Example .
:LB_ALB_Public :uses_certificate :Cert_Wildcard_Example .
:Cert_Wildcard_Example :issued_by :CA_DigiCert .
```

---

### Pattern 2: Internal Application with Certificate Management

**Scenario**: Internal application with certificate lifecycle management

**Components**:
- Application: "HR System" (Layer 2)
- Certificate: "hr.internal.example.com" (Layer 6)
- Certificate Authority: "Internal CA" (Layer 6)
- Security Policy: "Internal TLS Policy" (Layer 6)
- Security Zone: "Internal" (Layer 6)

**Relationships**:
```turtle
:App_HRSystem :uses_certificate :Cert_HR_Internal .
:App_HRSystem :secured_by :Policy_InternalTLS .
:App_HRSystem :belongs_to :Zone_Internal .
:Cert_HR_Internal :issued_by :CA_Internal .
:CA_Internal :trusts :CA_Root .
:Policy_InternalTLS :enforced_by :Firewall_Internal .
```

---

### Pattern 3: Cloud Infrastructure with IAM

**Scenario**: Cloud application with identity and access management

**Components**:
- Application: "Cloud API" (Layer 2)
- Identity Provider: "AWS IAM" (Layer 6)
- Security Policy: "API Access Policy" (Layer 6)
- Security Zone: "Cloud Production" (Layer 6)
- Certificate: "api.cloud.example.com" (Layer 6)

**Relationships**:
```turtle
:App_CloudAPI :authenticates_with :IdP_AWS_IAM .
:App_CloudAPI :secured_by :Policy_APIAccess .
:App_CloudAPI :belongs_to :Zone_CloudProduction .
:App_CloudAPI :uses_certificate :Cert_API_Cloud .
:Policy_APIAccess :enforced_by :IdP_AWS_IAM .
:Cert_API_Cloud :issued_by :CA_LetsEncrypt .
```

---

### Pattern 4: Microservices with Service Mesh Security

**Scenario**: Microservices with mutual TLS and service mesh

**Components**:
- Services: "Order Service", "Payment Service", "Inventory Service" (Layer 2)
- Certificates: Individual service certificates (Layer 6)
- Certificate Authority: "Service Mesh CA" (Layer 6)
- Security Policy: "mTLS Policy" (Layer 6)
- Identity Provider: "Service Mesh Identity" (Layer 6)

**Relationships**:
```turtle
:Service_Order :uses_certificate :Cert_OrderService .
:Service_Payment :uses_certificate :Cert_PaymentService .
:Service_Inventory :uses_certificate :Cert_InventoryService .
:Cert_OrderService :issued_by :CA_ServiceMesh .
:Cert_PaymentService :issued_by :CA_ServiceMesh .
:Cert_InventoryService :issued_by :CA_ServiceMesh .
:Service_Order :secured_by :Policy_mTLS .
:Service_Payment :secured_by :Policy_mTLS .
:Service_Inventory :secured_by :Policy_mTLS .
:Service_Order :authenticates_with :IdP_ServiceMesh .
```

---

## Query Patterns

### Security Analysis Queries

#### Query 1: Find Expiring Certificates

**SPARQL**:
```sparql
SELECT ?cert ?entity ?expiry_date ?days_until_expiry
WHERE {
  ?cert rdf:type :Certificate ;
        :lifecycle_status "active" ;
        :expiration_date ?expiry_date .
  ?entity :uses_certificate ?cert .
  BIND((xsd:integer(?expiry_date - NOW()) / 86400) AS ?days_until_expiry)
  FILTER(?days_until_expiry <= 30 && ?days_until_expiry >= 0)
}
ORDER BY ?days_until_expiry
```

**Cypher** (Neo4j):
```cypher
MATCH (entity)-[:USES_CERTIFICATE]->(cert:Certificate)
WHERE cert.lifecycle_status = 'active'
  AND duration.between(datetime(), datetime(cert.expiration_date)).days <= 30
  AND duration.between(datetime(), datetime(cert.expiration_date)).days >= 0
RETURN entity.name AS entity,
       cert.name AS certificate,
       cert.expiration_date AS expiry_date,
       duration.between(datetime(), datetime(cert.expiration_date)).days AS days_until_expiry
ORDER BY days_until_expiry
```

---

#### Query 2: Find Unprotected Applications

**SPARQL**:
```sparql
SELECT ?app ?zone
WHERE {
  ?app rdf:type :Application .
  OPTIONAL { ?app :protected_by ?firewall }
  OPTIONAL { ?app :belongs_to ?zone }
  FILTER(!BOUND(?firewall))
}
```

**Cypher** (Neo4j):
```cypher
MATCH (app:Application)
WHERE NOT (app)-[:PROTECTED_BY]->(:Firewall)
  AND NOT (app)-[:PROTECTED_BY]->(:WAF)
OPTIONAL MATCH (app)-[:BELONGS_TO]->(zone:SecurityZone)
RETURN app.name AS application,
       zone.name AS security_zone
```

---

#### Query 3: Find Security Policy Violations

**SPARQL**:
```sparql
SELECT ?entity ?policy ?compliance_status
WHERE {
  ?entity :secured_by ?policy .
  ?policy :lifecycle_status "active" .
  ?entity :compliance_status ?compliance_status .
  FILTER(?compliance_status = "non_compliant")
}
```

**Cypher** (Neo4j):
```cypher
MATCH (entity)-[r:SECURED_BY]->(policy:SecurityPolicy)
WHERE policy.lifecycle_status = 'active'
  AND r.compliance_status = 'non_compliant'
RETURN entity.name AS entity,
       policy.name AS policy,
       r.compliance_status AS compliance_status
```

---

#### Query 4: Find Certificate Chain

**SPARQL**:
```sparql
SELECT ?cert ?issuer_ca ?root_ca
WHERE {
  ?cert rdf:type :Certificate ;
        :issued_by ?issuer_ca .
  OPTIONAL {
    ?issuer_ca :trusts+ ?root_ca .
    ?root_ca :ca_type "root" .
  }
}
```

**Cypher** (Neo4j):
```cypher
MATCH (cert:Certificate)-[:ISSUED_BY]->(issuer:CertificateAuthority)
OPTIONAL MATCH (issuer)-[:TRUSTS*]->(root:CertificateAuthority)
WHERE root.ca_type = 'root'
RETURN cert.name AS certificate,
       issuer.name AS issuer_ca,
       root.name AS root_ca
```

---

#### Query 5: Find All Security Controls for Application

**SPARQL**:
```sparql
SELECT ?app ?firewall ?waf ?policy ?zone ?idp ?cert
WHERE {
  ?app rdf:type :Application .
  OPTIONAL { ?app :protected_by ?firewall . ?firewall rdf:type :Firewall }
  OPTIONAL { ?app :protected_by ?waf . ?waf rdf:type :WAF }
  OPTIONAL { ?app :secured_by ?policy }
  OPTIONAL { ?app :belongs_to ?zone }
  OPTIONAL { ?app :authenticates_with ?idp }
  OPTIONAL { ?app :uses_certificate ?cert }
  FILTER(?app = :App_CustomerPortal)
}
```

**Cypher** (Neo4j):
```cypher
MATCH (app:Application {name: 'Customer Portal'})
OPTIONAL MATCH (app)-[:PROTECTED_BY]->(firewall:Firewall)
OPTIONAL MATCH (app)-[:PROTECTED_BY]->(waf:WAF)
OPTIONAL MATCH (app)-[:SECURED_BY]->(policy:SecurityPolicy)
OPTIONAL MATCH (app)-[:BELONGS_TO]->(zone:SecurityZone)
OPTIONAL MATCH (app)-[:AUTHENTICATES_WITH]->(idp:IdentityProvider)
OPTIONAL MATCH (app)-[:USES_CERTIFICATE]->(cert:Certificate)
RETURN app.name AS application,
       collect(DISTINCT firewall.name) AS firewalls,
       collect(DISTINCT waf.name) AS wafs,
       collect(DISTINCT policy.name) AS policies,
       zone.name AS security_zone,
       collect(DISTINCT idp.name) AS identity_providers,
       collect(DISTINCT cert.name) AS certificates
```

---

## Framework Mappings

### CIM Security Model Mapping

| Ontology Entity Type | CIM Class | CIM Namespace |
|----------------------|-----------|---------------|
| Firewall | CIM_SecurityService | CIM_Security |
| WAF | CIM_SecurityService | CIM_Security |
| Certificate | CIM_Credential | CIM_Security |
| CertificateAuthority | CIM_CertificateAuthority | CIM_Security |
| SecurityPolicy | CIM_Policy | CIM_Policy |
| IdentityProvider | CIM_IdentityManagementService | CIM_Security |
| SecurityZone | CIM_SecurityZone | CIM_Security |

### NIST Framework Mapping

| Ontology Layer | NIST CSF Function | NIST SP 800-53 Controls |
|----------------|-------------------|-------------------------|
| Security Infrastructure | Protect (PR) | AC (Access Control), IA (Identification and Authentication), SC (System and Communications Protection) |
| Firewall | PR.AC, PR.PT | AC-4, SC-7 (Boundary Protection) |
| WAF | PR.PT | SI-10 (Information Input Validation) |
| Certificate | PR.DS | SC-12, SC-13 (Cryptographic Protection) |
| SecurityPolicy | PR.IP | PL-1, PL-2 (Security Planning) |
| IdentityProvider | PR.AC | IA-2, IA-3, IA-8 (Identification and Authentication) |
| SecurityZone | PR.AC | AC-4 (Information Flow Enforcement) |

### ISO 27001 Mapping

| Ontology Entity Type | ISO 27001 Control |
|----------------------|-------------------|
| Firewall | A.13.1.1 (Network controls) |
| WAF | A.14.1.2 (Securing application services) |
| Certificate | A.10.1.2 (Key management) |
| SecurityPolicy | A.5.1.1 (Policies for information security) |
| IdentityProvider | A.9.2.1 (User registration and de-registration) |
| SecurityZone | A.13.1.3 (Segregation in networks) |

---

## Implementation Notes

### Certificate Lifecycle Management

1. **Expiration Monitoring**: Implement automated monitoring for certificates expiring within 30, 60, and 90 days
2. **Renewal Workflow**: Define renewal processes for certificates before expiration
3. **Revocation Handling**: Track revoked certificates and update lifecycle_status
4. **Chain Validation**: Validate certificate chains up to trusted root CAs

### Security Zone Design

1. **Zone Segmentation**: Define clear boundaries between security zones
2. **Trust Boundaries**: Enforce trust levels at zone boundaries
3. **Access Control**: Implement access controls between zones
4. **Monitoring**: Enhanced monitoring for cross-zone traffic

### Policy Enforcement

1. **Policy Hierarchy**: Define policy precedence and inheritance
2. **Compliance Tracking**: Track compliance status for all secured entities
3. **Audit Logging**: Log all policy enforcement actions
4. **Review Cycles**: Implement regular policy review cycles

### Identity and Access Management

1. **Federation**: Support identity federation across multiple IdPs
2. **MFA Enforcement**: Enforce MFA for sensitive resources
3. **Session Management**: Implement session timeout and renewal
4. **Audit Trail**: Maintain audit logs for authentication events

---

## Extension Points

### Adding New Security Entity Types

1. Define entity type as subclass of :SecurityLayer
2. Specify security_type attribute value
3. Define relationships to existing security entities
4. Create SHACL validation shapes
5. Document framework mappings

### Custom Security Attributes

Organizations may need custom security attributes:
1. Custom attributes SHOULD be namespaced (e.g., `custom:security_attribute`)
2. Custom attributes SHOULD NOT conflict with framework attributes
3. Custom attributes SHOULD be documented with rationale
4. Custom attributes MAY be proposed for inclusion in future versions

---

## Summary

Layer 6 (Security Infrastructure) provides comprehensive security modeling across all IT infrastructure layers. The layer includes:

- **7 Entity Types**: Firewall, WAF, Certificate, CertificateAuthority, SecurityPolicy, IdentityProvider, SecurityZone
- **8 Relationship Types**: 3 intra-layer, 5 cross-layer
- **Framework Alignment**: CIM Security Model, NIST CSF, NIST SP 800-53, ISO 27001
- **Validation Rules**: Certificate expiration, policy enforcement, zone membership
- **Query Patterns**: Security analysis, compliance checking, certificate management

The Security layer is cross-cutting, protecting resources in all other layers through protection, policy enforcement, and trust boundaries.
