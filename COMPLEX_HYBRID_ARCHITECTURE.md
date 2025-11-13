# Complex Hybrid Architecture - Documentation

## Overview

This document describes a comprehensive hybrid architecture modeled using the IT Infrastructure and Application Dependency Ontology. The architecture represents a real-world enterprise scenario with legacy on-premises systems integrated with modern cloud-native microservices across multiple cloud providers.

## Architecture Summary

### Applications (5 Total)

1. **Legacy ERP System** (On-Premises)
   - SOA-based architecture
   - WebLogic cluster
   - Oracle RAC database
   - Nginx web server
   - SOAP/XML APIs (synchronous and asynchronous)

2. **Customer Service Application** (Azure)
   - Microservices architecture
   - Node.js/Express
   - MongoDB Atlas (SaaS)
   - Kubernetes (AKS)

3. **Order Management Application** (Azure)
   - Microservices architecture
   - Java Spring Boot
   - PostgreSQL on Azure VM
   - Kubernetes (AKS)

4. **Inventory Service Application** (Azure)
   - Microservices architecture
   - Python FastAPI
   - Azure SQL Database (PaaS)
   - Kubernetes (AKS)

5. **Payment Service Application** (AWS)
   - Microservices architecture
   - Go/Gin Framework
   - AWS RDS PostgreSQL (PaaS)
   - Kubernetes (EKS)

### Common Microservices (Shared)

1. **Authentication Service** (Azure)
   - Centralized authentication/authorization
   - Used by all 5 applications
   - OAuth2-based

2. **Notification Service** (AWS)
   - Centralized notifications (email, SMS, push)
   - Used by all 5 applications
   - REST API

### Integration Architecture

- **MuleSoft Anypoint Platform** (SaaS)
  - Integration middleware between legacy and modern applications
  - SOAP to REST transformation
  - Message routing and transformation

- **Enterprise API Gateway**
  - Exposes microservices REST APIs to legacy application
  - OAuth2 authentication
  - Rate limiting and security

### Infrastructure Distribution

- **On-Premises**: Legacy ERP System
- **Azure**: 3 microservices applications + Authentication Service
- **AWS**: 1 microservices application + Notification Service
- **SaaS**: MuleSoft, MongoDB Atlas

## Detailed Component Breakdown

### Layer 1: Business Processes

| Business Process | Realized By Applications |
|------------------|-------------------------|
| Customer Management | Legacy ERP, Customer Service App |
| Order Processing | Legacy ERP, Order Management App |
| Inventory Management | Legacy ERP, Inventory Service App |
| Payment Processing | Payment Service App |
| Business Analytics | Customer, Order, Inventory Apps |

### Layer 2: Application Components

#### Legacy ERP System (On-Premises)

**Components**:
- ERP Customer Module (Web Service)
- ERP Order Module (Web Service)
- ERP Inventory Module (Web Service)

**Application Servers**:
- WebLogic Cluster (3 managed servers)
- Nginx Web Server (reverse proxy)

**APIs**:
- ERP Customer API (SOAP/XML - synchronous)
- ERP Order API (SOAP/XML - synchronous)
- ERP Inventory Queue (Oracle AQ - asynchronous)

**Database**:
- Oracle RAC 19c (2-node cluster)
- 500GB per instance

**Integration**:
- Calls MuleSoft for microservices integration
- Invokes microservices via Enterprise API Gateway
- Uses Authentication Service
- Uses Notification Service

#### Customer Service Application (Azure)

**Services**:
- Customer Profile Service (Node.js/Express)
- Customer Profile API (REST/OAuth2)

**Database**:
- MongoDB Atlas (SaaS)

**Cache**:
- Azure Redis Cache (shared)

**Deployment**:
- Kubernetes (AKS)
- 3 pod replicas
- Namespace: customer-service

#### Order Management Application (Azure)

**Services**:
- Order Processing Service (Java Spring Boot)
- Order Processing API (REST/OAuth2)

**Database**:
- PostgreSQL 14.5 on Azure VM

**Cache**:
- Azure Redis Cache (shared)

**Deployment**:
- Kubernetes (AKS)
- 3 pod replicas
- Namespace: order-service

#### Inventory Service Application (Azure)

**Services**:
- Inventory Tracking Service (Python FastAPI)
- Inventory Tracking API (REST/API Key)

**Database**:
- Azure SQL Database (PaaS)

**Deployment**:
- Kubernetes (AKS)
- 2 pod replicas
- Namespace: inventory-service

#### Payment Service Application (AWS)

**Services**:
- Payment Processing Service (Go/Gin)
- Payment Processing API (REST/OAuth2)

**Database**:
- AWS RDS PostgreSQL 14.7 (PaaS)

**Deployment**:
- Kubernetes (EKS)
- 4 pod replicas
- Namespace: payment-service

#### Common Services

**Authentication Service** (Azure):
- Deployed in shared-services namespace
- 3 pod replicas
- Used by all applications
- Azure AD integration

**Notification Service** (AWS):
- Deployed in notification-service namespace
- 2 pod replicas
- Used by all applications
- Email, SMS, push notifications

### Layer 3: Container & Orchestration

#### Azure AKS Cluster

**Configuration**:
- Cluster: aks-prod-eastus
- Kubernetes version: 1.26.3
- Node count: 6
- Region: East US

**Namespaces**:
1. customer-service (16 CPU, 32Gi RAM)
2. order-service (16 CPU, 32Gi RAM)
3. inventory-service (8 CPU, 16Gi RAM)
4. shared-services (8 CPU, 16Gi RAM)

**Pods**:
- Customer Profile Pod (3 replicas)
- Order Processing Pod (3 replicas)
- Inventory Tracking Pod (2 replicas)
- Authentication Pod (3 replicas)

**Services**:
- Load Balancer services for external access
- ClusterIP service for internal auth

#### AWS EKS Cluster

**Configuration**:
- Cluster: eks-prod-us-east-1
- Kubernetes version: 1.26.2
- Node count: 4
- Region: us-east-1

**Namespaces**:
1. payment-service (16 CPU, 32Gi RAM)
2. notification-service (4 CPU, 8Gi RAM)

**Pods**:
- Payment Processing Pod (4 replicas)
- Notification Pod (2 replicas)

**Services**:
- Load Balancer service for payment API
- ClusterIP service for internal notifications

### Layer 4: Physical Infrastructure

#### On-Premises Infrastructure

**Physical Servers** (3x Dell PowerEdge R740):
- 2x CPU, 32 cores each
- 256GB RAM each
- Location: Datacenter-East-Rack-05

**Hypervisor**:
- VMware ESXi 7.0 U3
- Cluster across 3 physical servers

**Virtual Machines**:
- 3x WebLogic VMs (8 vCPU, 32GB RAM each)
- 1x Nginx VM (4 vCPU, 16GB RAM)
- 2x Oracle RAC VMs (16 vCPU, 128GB RAM each)

**Storage**:
- NetApp FAS8300 SAN
- 50TB capacity
- RAID 10 for Oracle RAC (2TB volume)

#### Azure Infrastructure

**AKS Nodes** (6x Standard_D8s_v3):
- 8 vCPU, 32GB RAM each
- Distributed across 2 availability zones
- Ubuntu 20.04 LTS

**Database VM** (1x Standard_E16s_v3):
- 16 vCPU, 128GB RAM
- PostgreSQL 14.5
- Ubuntu 22.04 LTS

**Managed Services**:
- Azure SQL Database (PaaS)
- Azure Cache for Redis (PaaS)
- MongoDB Atlas (SaaS)

#### AWS Infrastructure

**EKS Nodes** (4x m5.2xlarge):
- 8 vCPU, 32GB RAM each
- Distributed across 2 availability zones
- Amazon Linux 2

**Managed Services**:
- AWS RDS PostgreSQL (PaaS)

### Layer 5: Network Topology

#### Load Balancers

1. **On-Premises F5 BIG-IP**
   - Hardware load balancer
   - Round-robin algorithm
   - HTTPS (port 443)
   - For legacy ERP

2. **Azure Load Balancer**
   - Cloud-managed
   - Least connections algorithm
   - HTTPS (port 443)
   - For AKS services

3. **AWS Application Load Balancer**
   - Cloud-managed
   - Round-robin algorithm
   - HTTPS (port 443)
   - For EKS services

#### Network Segments

1. **On-Premises Network**
   - VLAN 100
   - CIDR: 10.0.0.0/16
   - Gateway: 10.0.0.1

2. **Azure VNet**
   - CIDR: 172.16.0.0/16
   - Gateway: 172.16.0.1

3. **AWS VPC**
   - CIDR: 192.168.0.0/16
   - Gateway: 192.168.0.1

#### VPN Gateways

1. **On-Premises VPN Gateway**
   - Cisco ASA 5525-X
   - IP: 10.0.255.1

2. **Azure VPN Gateway**
   - Microsoft managed
   - IP: 172.16.255.1

3. **AWS VPN Gateway**
   - Amazon managed
   - IP: 192.168.255.1

#### Communication Paths

1. **Legacy to MuleSoft**
   - HTTPS
   - 1Gbps bandwidth
   - Routes through VPN gateways

2. **MuleSoft to Microservices**
   - HTTPS
   - 1Gbps bandwidth
   - Routes through Azure LB

3. **Legacy to API Gateway**
   - HTTPS
   - 500Mbps bandwidth
   - Routes through VPN gateways

### Layer 6: Security Infrastructure

#### Firewalls

1. **On-Premises Firewall**
   - Network firewall
   - 250 rules
   - Protects legacy ERP

2. **Azure Network Security Group**
   - Cloud-managed
   - 50 rules
   - Protects Azure microservices

3. **AWS Security Group**
   - Cloud-managed
   - 40 rules
   - Protects AWS microservices

#### Web Application Firewalls

1. **Azure WAF**
   - OWASP 3.2 ruleset
   - Protects Azure APIs

2. **AWS WAF**
   - OWASP 3.2 ruleset
   - Protects AWS APIs

#### SSL/TLS Certificates

1. **Legacy ERP Certificate**
   - CN: erp.example.com
   - Issuer: Internal CA
   - Valid: 2024-01-01 to 2025-01-01
   - 2048-bit RSA

2. **Azure Wildcard Certificate**
   - CN: *.azure.example.com
   - Issuer: DigiCert
   - Valid: 2024-01-01 to 2025-01-01
   - 2048-bit RSA

3. **AWS Wildcard Certificate**
   - CN: *.aws.example.com
   - Issuer: Amazon Trust Services
   - Valid: 2024-01-01 to 2025-01-01
   - 2048-bit RSA

#### Identity Providers

1. **Azure Active Directory**
   - OAuth2/OIDC
   - For Azure microservices

2. **AWS Cognito**
   - OAuth2/OIDC
   - For AWS microservices

#### Security Zones

1. **DMZ Zone**
   - Nginx web server
   - On-premises load balancer
   - External-facing services

2. **Internal Zone**
   - WebLogic cluster
   - Oracle RAC database
   - Backend services

## Integration Patterns

### Pattern 1: Legacy to Microservices via MuleSoft

```
Legacy ERP → MuleSoft ESB → Microservices
```

- Legacy calls MuleSoft with SOAP/XML
- MuleSoft transforms to REST/JSON
- MuleSoft routes to appropriate microservice
- Response transformed back to SOAP/XML

### Pattern 2: Legacy to Microservices via API Gateway

```
Legacy ERP → Enterprise API Gateway → Microservices
```

- Legacy calls API Gateway with REST
- API Gateway authenticates with OAuth2
- API Gateway routes to microservice
- Direct REST/JSON communication

### Pattern 3: Microservices to Microservices

```
Order Service → Customer Service
Order Service → Inventory Service
Order Service → Payment Service
```

- Direct REST API calls
- Service discovery via Kubernetes DNS
- OAuth2 authentication
- Circuit breaker patterns

### Pattern 4: All Applications to Common Services

```
All Applications → Authentication Service
All Applications → Notification Service
```

- Centralized authentication
- Centralized notifications
- Shared across all applications

## Data Flow Examples

### Example 1: Order Creation

1. Customer creates order via Customer Service App
2. Order Service validates customer via Customer Service
3. Order Service checks inventory via Inventory Service
4. Order Service processes payment via Payment Service
5. Payment Service sends notification via Notification Service
6. Order Service updates legacy ERP via MuleSoft
7. Legacy ERP updates Oracle RAC database

### Example 2: Legacy ERP Queries Customer Data

1. Legacy ERP calls Enterprise API Gateway
2. API Gateway authenticates request
3. API Gateway routes to Customer Service
4. Customer Service queries MongoDB Atlas
5. Response returned through API Gateway
6. Legacy ERP receives customer data

## Query Examples

### Find All Applications and Their Databases

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>

SELECT ?app ?appName ?db ?dbName ?dbType
WHERE {
  ?app a :Application ;
       :name ?appName ;
       :uses ?db .
  ?db a :Database ;
      :name ?dbName ;
      :database_type ?dbType .
}
ORDER BY ?appName
```

### Find Full Stack for Payment Service

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>

SELECT ?layer ?component ?name
WHERE {
  {
    inst:PaymentProcessing :realized_by ?component .
    ?component :name ?name .
    BIND("Business Process" AS ?layer)
  } UNION {
    inst:PaymentServiceApp :name ?name .
    BIND("Application" AS ?layer)
    BIND(inst:PaymentServiceApp AS ?component)
  } UNION {
    inst:PaymentServiceApp :deployed_as ?component .
    ?component :name ?name .
    BIND("Container" AS ?layer)
  } UNION {
    inst:PaymentProcessingPod :runs_on ?component .
    ?component :name ?name .
    BIND("Infrastructure" AS ?layer)
  } UNION {
    inst:PaymentServiceApp :uses ?component .
    ?component a :Database ;
               :name ?name .
    BIND("Database" AS ?layer)
  }
}
```

### Find All Integration Points

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>

SELECT ?source ?target ?via
WHERE {
  {
    inst:LegacyERPSystem :calls ?via .
    ?via :calls ?target .
    BIND(inst:LegacyERPSystem AS ?source)
  } UNION {
    ?source :calls inst:AuthenticationService .
    BIND(inst:AuthenticationService AS ?target)
    BIND("Direct" AS ?via)
  }
}
```

### Impact Analysis: Azure AKS Node Failure

```sparql
PREFIX : <http://example.org/it-infrastructure-ontology#>
PREFIX inst: <http://example.org/instances#>

SELECT ?affected ?type ?name
WHERE {
  ?affected (:runs_on|:deployed_as)+ inst:AzureAKSNode1 ;
            a ?type ;
            :name ?name .
}
```

## File Location

The complete architecture is defined in:
```
ontology/sample-data-complex-hybrid.ttl
```

## Validation

To validate this architecture:

```bash
pyshacl -s ontology/shacl-shapes.ttl \
        -d ontology/sample-data-complex-hybrid.ttl \
        -f human
```

## Summary Statistics

- **Total Applications**: 5
- **Total Microservices**: 10+ (including common services)
- **Total Databases**: 5
- **Total Kubernetes Clusters**: 2 (AKS + EKS)
- **Total Pods**: 6 types
- **Total VMs**: 11 (6 on-prem + 5 cloud)
- **Total Physical Servers**: 3
- **Total Cloud Instances**: 10 (6 Azure + 4 AWS)
- **Integration Points**: MuleSoft + API Gateway
- **Cloud Providers**: 2 (Azure + AWS)
- **Deployment Models**: On-Premises + Multi-Cloud

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Status**: Complete

