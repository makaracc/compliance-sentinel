# Admin Agent Architecture Plan

## Overview
The Admin Agent is a Python microservice powered by Dapr that orchestrates compliance management workflows using Dapr Agents and Dapr Workflows. It works with the existing compliance_sentinel database to manage company compliance requirements and detailed step-by-step compliance tracking.

## System Architecture

### Core Components

#### 1. Dapr Agents
- **Compliance Matcher Agent**: Matches companies to compliance requirements based on industry/location
- **Step Generator Agent**: Creates detailed compliance steps for assigned requirements
- **Progress Monitor Agent**: Tracks step completion and identifies bottlenecks
- **Evidence Validator Agent**: Validates evidence files and documentation
- **Notification Agent**: Sends alerts for due dates and missing steps

#### 2. Dapr Workflows
- **Company Onboarding Workflow**: Analyzes companies and assigns compliance requirements
- **Compliance Step Generation Workflow**: Creates detailed steps for company compliance
- **Step Completion Workflow**: Manages individual step execution and evidence validation
- **Compliance Reporting Workflow**: Generates comprehensive compliance status reports

#### 3. Existing Database Schema (compliance_sentinel)

##### Companies Table
```sql
-- EXISTING TABLE
CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    industry VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    address TEXT,
    contact_email VARCHAR,
    contact_phone VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Current Data:** 1 company record

##### Compliance Requirements Table
```sql
-- EXISTING TABLE
CREATE TABLE compliance_requirements (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    industry VARCHAR NOT NULL,
    location VARCHAR,
    regulatory_body VARCHAR,
    severity_level VARCHAR DEFAULT 'Medium',
    due_frequency VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Current Data:** 5 compliance requirements

##### Company Compliance Table
```sql
-- EXISTING TABLE
CREATE TABLE company_compliance (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    compliance_requirement_id INTEGER NOT NULL REFERENCES compliance_requirements(id),
    status VARCHAR DEFAULT 'Not Started',
    assigned_to VARCHAR,
    due_date DATE,
    completion_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, compliance_requirement_id)
);
```
**Current Data:** 5 company-compliance mappings

##### Compliance Steps Table
```sql
-- EXISTING TABLE
CREATE TABLE compliance_steps (
    id INTEGER PRIMARY KEY,
    compliance_requirement_id INTEGER NOT NULL REFERENCES compliance_requirements(id),
    step_number INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT,
    required_documentation TEXT,
    estimated_duration_hours INTEGER,
    responsible_role VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Current Data:** 5 compliance steps

##### Company Compliance Steps Table
```sql
-- EXISTING TABLE
CREATE TABLE company_compliance_steps (
    id INTEGER PRIMARY KEY,
    company_compliance_id INTEGER NOT NULL REFERENCES company_compliance(id),
    compliance_step_id INTEGER NOT NULL REFERENCES compliance_steps(id),
    status VARCHAR DEFAULT 'Pending',
    completed_by VARCHAR,
    completed_at TIMESTAMP,
    evidence_file_path VARCHAR,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_compliance_id, compliance_step_id)
);
```
**Current Data:** Empty (ready for admin-agent to populate)

##### Dapr State Management Tables
```sql
-- EXISTING DAPR TABLES
CREATE TABLE dapr_metadata (...);  -- Dapr metadata storage
CREATE TABLE state (...);          -- Dapr state store
```

## Workflow Definitions

### 1. Company Onboarding Workflow

```mermaid
graph TD
    A[New Company] --> B[Analyze Industry & Location]
    B --> C[Find Matching Compliance Requirements]
    C --> D[Create Company Compliance Records]
    D --> E[Generate Compliance Steps]
    E --> F[Set Due Dates]
    F --> G[Assign Responsibilities]
    G --> H[Send Notifications]
    H --> I[End]
```

**Activities:**
- `AnalyzeCompanyActivity`: Extract industry and location from company data
- `FindComplianceRequirementsActivity`: Query matching compliance requirements
- `CreateCompanyComplianceActivity`: Create company_compliance records
- `GenerateComplianceStepsActivity`: Create company_compliance_steps records
- `SetDueDatesActivity`: Calculate and assign due dates
- `AssignResponsibilitiesActivity`: Assign steps to responsible parties
- `SendNotificationsActivity`: Alert stakeholders of new assignments

### 2. Compliance Step Generation Workflow

```mermaid
graph TD
    A[Company Compliance Created] --> B[Get Compliance Steps]
    B --> C[Create Company Step Records]
    C --> D[Calculate Priorities]
    D --> E[Set Estimated Durations]
    E --> F[Assign Responsible Roles]
    F --> G[Create Step Timeline]
    G --> H[Update Status]
    H --> I[End]
```

**Activities:**
- `GetComplianceStepsActivity`: Retrieve steps for compliance requirement
- `CreateCompanyStepsActivity`: Create company_compliance_steps records
- `CalculatePrioritiesActivity`: Set step priorities based on severity
- `SetDurationsActivity`: Assign estimated duration from compliance_steps
- `AssignRolesActivity`: Map responsible roles to specific people
- `CreateTimelineActivity`: Generate step execution timeline
- `UpdateStatusActivity`: Update company_compliance status

### 3. Step Completion Workflow

```mermaid
graph TD
    A[Step Started] --> B[Validate Prerequisites]
    B --> C[Execute Step]
    C --> D[Upload Evidence]
    D --> E[Validate Evidence]
    E --> F{Evidence Valid?}
    F -->|Yes| G[Mark Step Complete]
    F -->|No| H[Request Additional Evidence]
    H --> D
    G --> I[Update Compliance Progress]
    I --> J[Check All Steps Complete]
    J --> K{All Complete?}
    K -->|Yes| L[Mark Compliance Complete]
    K -->|No| M[Continue Monitoring]
    L --> N[Generate Report]
    M --> O[End]
    N --> O
```

**Activities:**
- `ValidatePrerequisitesActivity`: Check if previous steps are complete
- `ExecuteStepActivity`: Guide step execution process
- `UploadEvidenceActivity`: Handle evidence file uploads
- `ValidateEvidenceActivity`: Verify evidence meets requirements
- `MarkStepCompleteActivity`: Update company_compliance_steps status
- `UpdateComplianceProgressActivity`: Update company_compliance progress
- `CheckCompletionActivity`: Verify all steps are complete
- `MarkComplianceCompleteActivity`: Mark overall compliance as complete
- `GenerateReportActivity`: Create compliance completion report

### 4. Compliance Reporting Workflow

```mermaid
graph TD
    A[Report Request] --> B[Gather Company Data]
    B --> C[Collect Compliance Status]
    C --> D[Aggregate Step Progress]
    D --> E[Calculate Completion Rates]
    E --> F[Identify Overdue Items]
    F --> G[Generate Insights]
    G --> H[Format Report]
    H --> I[Send Report]
    I --> J[End]
```

## Agent Definitions

### 1. Compliance Matcher Agent

**Purpose**: Match companies to applicable compliance requirements based on industry and location

**Capabilities:**
- Industry-specific compliance analysis
- Location-based regulatory mapping
- Automatic requirement assignment
- Gap analysis for missing requirements

**Database Operations:**
- Query `compliance_requirements` by industry/location
- Create `company_compliance` records
- Update company compliance status

### 2. Step Generator Agent

**Purpose**: Generate detailed compliance steps for company-compliance pairs

**Capabilities:**
- Step template instantiation
- Timeline calculation
- Resource estimation
- Role assignment

**Database Operations:**
- Query `compliance_steps` for requirements
- Create `company_compliance_steps` records
- Set due dates and assignments

### 3. Progress Monitor Agent

**Purpose**: Monitor compliance step progress and identify bottlenecks

**Capabilities:**
- Progress tracking
- Deadline monitoring
- Bottleneck identification
- Performance analytics

**Database Operations:**
- Query `company_compliance_steps` status
- Update progress metrics
- Identify overdue steps

### 4. Evidence Validator Agent

**Purpose**: Validate uploaded evidence files and documentation

**Capabilities:**
- File format validation
- Content verification
- Completeness checking
- Quality assessment

**Database Operations:**
- Update `evidence_file_path` in `company_compliance_steps`
- Validate evidence requirements
- Mark steps as complete

### 5. Notification Agent

**Purpose**: Send alerts and notifications for compliance activities

**Capabilities:**
- Due date alerts
- Completion notifications
- Escalation management
- Multi-channel messaging

**Database Operations:**
- Query overdue steps
- Track notification history
- Update notification status

## API Endpoints

### Company Management
- `GET /api/companies` - List companies
- `GET /api/companies/{id}` - Get company details
- `POST /api/companies/{id}/onboard` - Start company onboarding workflow

### Compliance Management
- `GET /api/companies/{id}/compliance` - Get company compliance status
- `POST /api/companies/{id}/compliance/{req_id}/steps` - Generate compliance steps
- `GET /api/compliance-steps/{id}` - Get step details
- `PUT /api/compliance-steps/{id}/complete` - Mark step complete
- `POST /api/compliance-steps/{id}/evidence` - Upload evidence

### Reporting
- `GET /api/companies/{id}/reports` - Get compliance reports
- `POST /api/reports/generate` - Generate new report
- `GET /api/dashboard/overview` - Get dashboard overview

### Workflow Management
- `POST /api/workflows/onboarding/start` - Start onboarding workflow
- `POST /api/workflows/step-generation/start` - Start step generation workflow
- `GET /api/workflows/{instanceId}/status` - Get workflow status
- `POST /api/workflows/{instanceId}/events/{eventName}` - Raise workflow event

## Configuration

### Dapr Components

#### State Store (PostgreSQL - compliance_sentinel database)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "postgresql://username:password@host:port/compliance_sentinel"
```

#### Pub/Sub (Redis)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: "localhost:6379"
```

#### Workflow Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: dapr
spec:
  type: workflow.dapr
  version: v1
```

## Implementation Plan

### Phase 1: Foundation (Week 1)
1. Set up Python FastAPI service
2. Configure Dapr components
3. Implement database connection to compliance_sentinel
4. Create basic CRUD operations

### Phase 2: Core Workflows (Week 2)
1. Implement Company Onboarding Workflow
2. Create Compliance Matcher Agent
3. Implement Step Generator Agent
4. Set up basic API endpoints

### Phase 3: Advanced Features (Week 3)
1. Implement Step Completion Workflow
2. Add Evidence Validator Agent
3. Create Progress Monitor Agent
4. Add notification system

### Phase 4: Integration & Testing (Week 4)
1. End-to-end workflow testing
2. Performance optimization
3. Demo preparation
4. Documentation completion

## Technology Stack

- **Runtime**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon - compliance_sentinel)
- **Database ORM**: SQLAlchemy + asyncpg
- **Message Broker**: Redis
- **Orchestration**: Dapr Workflows
- **Agents**: Dapr Agents (Python SDK)
- **State Management**: Dapr State Store
- **Communication**: Dapr Pub/Sub
- **Containerization**: Docker
- **Deployment**: Kubernetes

## Success Metrics

1. **Workflow Resilience**: Workflows can recover from failures and resume processing
2. **Agent Collaboration**: Multiple agents work together to complete compliance processes
3. **Scalability**: System handles multiple companies and compliance requirements simultaneously
4. **Step-by-Step Tracking**: Detailed progress monitoring at individual step level
5. **Evidence Management**: Robust evidence upload and validation system
6. **Real-time Monitoring**: Live compliance status updates and notifications

This architecture leverages the existing sophisticated compliance_sentinel database schema to build a comprehensive compliance management system using Dapr's distributed application capabilities.
