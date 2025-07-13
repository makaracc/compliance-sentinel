"""
SQLAlchemy models for compliance_sentinel database
"""

from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped
from pydantic import BaseModel, Field

Base = declarative_base()


# SQLAlchemy Models (Database Tables)
class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    location = Column(String, nullable=False)
    address = Column(Text)
    contact_email = Column(String)
    contact_phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company_compliance = relationship("CompanyCompliance", back_populates="company")


class ComplianceRequirement(Base):
    __tablename__ = "compliance_requirements"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    industry = Column(String, nullable=False)
    location = Column(String)
    regulatory_body = Column(String)
    severity_level = Column(String, default="Medium")
    due_frequency = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company_compliance = relationship("CompanyCompliance", back_populates="compliance_requirement")
    compliance_steps = relationship("ComplianceStep", back_populates="compliance_requirement")


class CompanyCompliance(Base):
    __tablename__ = "company_compliance"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    compliance_requirement_id = Column(Integer, ForeignKey("compliance_requirements.id"), nullable=False)
    status = Column(String, default="Not Started")
    assigned_to = Column(String)
    due_date = Column(Date)
    completion_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="company_compliance")
    compliance_requirement = relationship("ComplianceRequirement", back_populates="company_compliance")
    company_compliance_steps = relationship("CompanyComplianceStep", back_populates="company_compliance")


class ComplianceStep(Base):
    __tablename__ = "compliance_steps"
    
    id = Column(Integer, primary_key=True)
    compliance_requirement_id = Column(Integer, ForeignKey("compliance_requirements.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    required_documentation = Column(Text)
    estimated_duration_hours = Column(Integer)
    responsible_role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    compliance_requirement = relationship("ComplianceRequirement", back_populates="compliance_steps")
    company_compliance_steps = relationship("CompanyComplianceStep", back_populates="compliance_step")


class CompanyComplianceStep(Base):
    __tablename__ = "company_compliance_steps"
    
    id = Column(Integer, primary_key=True)
    company_compliance_id = Column(Integer, ForeignKey("company_compliance.id"), nullable=False)
    compliance_step_id = Column(Integer, ForeignKey("compliance_steps.id"), nullable=False)
    status = Column(String, default="Pending")
    completed_by = Column(String)
    completed_at = Column(DateTime)
    evidence_file_path = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company_compliance = relationship("CompanyCompliance", back_populates="company_compliance_steps")
    compliance_step = relationship("ComplianceStep", back_populates="company_compliance_steps")


# Pydantic Models (API Schemas)
class CompanyBase(BaseModel):
    name: str = Field(..., description="Company name")
    industry: str = Field(..., description="Industry sector")
    location: str = Field(..., description="Company location")
    address: Optional[str] = Field(None, description="Company address")
    contact_email: Optional[str] = Field(None, description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone")


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ComplianceRequirementResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    industry: str
    location: Optional[str]
    regulatory_body: Optional[str]
    severity_level: str
    due_frequency: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CompanyComplianceBase(BaseModel):
    status: str = Field(default="Not Started", description="Compliance status")
    assigned_to: Optional[str] = Field(None, description="Person assigned to this compliance")
    due_date: Optional[date] = Field(None, description="Due date for compliance")
    completion_date: Optional[date] = Field(None, description="Completion date")
    notes: Optional[str] = Field(None, description="Additional notes")


class CompanyComplianceCreate(CompanyComplianceBase):
    company_id: int
    compliance_requirement_id: int


class CompanyComplianceUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None
    completion_date: Optional[date] = None
    notes: Optional[str] = None


class CompanyComplianceResponse(CompanyComplianceBase):
    id: int
    company_id: int
    compliance_requirement_id: int
    created_at: datetime
    updated_at: datetime
    company: CompanyResponse
    compliance_requirement: ComplianceRequirementResponse
    
    class Config:
        from_attributes = True


class ComplianceStepResponse(BaseModel):
    id: int
    compliance_requirement_id: int
    step_number: int
    title: str
    description: Optional[str]
    required_documentation: Optional[str]
    estimated_duration_hours: Optional[int]
    responsible_role: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class CompanyComplianceStepBase(BaseModel):
    status: str = Field(default="Pending", description="Step status")
    completed_by: Optional[str] = Field(None, description="Person who completed the step")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    evidence_file_path: Optional[str] = Field(None, description="Path to evidence file")
    notes: Optional[str] = Field(None, description="Step notes")


class CompanyComplianceStepCreate(CompanyComplianceStepBase):
    company_compliance_id: int
    compliance_step_id: int


class CompanyComplianceStepUpdate(BaseModel):
    status: Optional[str] = None
    completed_by: Optional[str] = None
    completed_at: Optional[datetime] = None
    evidence_file_path: Optional[str] = None
    notes: Optional[str] = None


class CompanyComplianceStepResponse(CompanyComplianceStepBase):
    id: int
    company_compliance_id: int
    compliance_step_id: int
    created_at: datetime
    updated_at: datetime
    compliance_step: ComplianceStepResponse
    
    class Config:
        from_attributes = True


# Task Management Models
class TaskBase(BaseModel):
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: str = Field(default="Medium", description="Task priority")
    assigned_to: Optional[str] = Field(None, description="Person assigned to task")
    due_date: Optional[date] = Field(None, description="Task due date")
    status: str = Field(default="Pending", description="Task status")


class TaskCreate(TaskBase):
    company_compliance_step_id: Optional[int] = Field(None, description="Related compliance step")


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class TaskResponse(TaskBase):
    id: int
    company_compliance_step_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Workflow Models
class WorkflowStartRequest(BaseModel):
    workflow_name: str = Field(..., description="Name of the workflow to start")
    input_data: dict = Field(default={}, description="Input data for the workflow")


class WorkflowResponse(BaseModel):
    instance_id: str = Field(..., description="Workflow instance ID")
    workflow_name: str = Field(..., description="Workflow name")
    status: str = Field(..., description="Workflow status")
    input_data: dict = Field(default={}, description="Workflow input data")
    output_data: Optional[dict] = Field(None, description="Workflow output data")
    started_at: datetime = Field(..., description="Workflow start time")
    completed_at: Optional[datetime] = Field(None, description="Workflow completion time")


# Dashboard and Reporting Models
class ComplianceOverview(BaseModel):
    total_companies: int
    total_requirements: int
    total_steps: int
    completed_steps: int
    pending_steps: int
    overdue_steps: int
    completion_rate: float


class CompanyComplianceOverview(BaseModel):
    company: CompanyResponse
    total_requirements: int
    completed_requirements: int
    in_progress_requirements: int
    not_started_requirements: int
    completion_rate: float
    overdue_count: int
