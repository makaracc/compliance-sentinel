"""
Step Generation Workflow
Creates detailed compliance steps for company compliance requirements
"""

from typing import Dict, Any, List
from dapr.ext.workflow import WorkflowContext, WorkflowActivityContext, workflow_activity
import structlog

logger = structlog.get_logger(__name__)


@workflow_activity
async def get_compliance_steps_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get compliance steps for a specific compliance requirement"""
    try:
        compliance_requirement_id = input_data.get("compliance_requirement_id")
        
        logger.info("Getting compliance steps", 
                   compliance_requirement_id=compliance_requirement_id)
        
        # Mock compliance steps data
        # In real implementation, this would query the compliance_steps table
        steps_templates = {
            1: [  # Data Protection Assessment (GDPR)
                {
                    "step_number": 1,
                    "title": "Data Inventory and Mapping",
                    "description": "Identify and document all personal data processing activities",
                    "required_documentation": "Data flow diagrams, processing records, data inventory spreadsheet",
                    "estimated_duration_hours": 16,
                    "responsible_role": "Data Protection Officer"
                },
                {
                    "step_number": 2,
                    "title": "Privacy Impact Assessment",
                    "description": "Conduct privacy impact assessment for high-risk processing activities",
                    "required_documentation": "PIA report, risk assessment matrix, mitigation measures",
                    "estimated_duration_hours": 24,
                    "responsible_role": "Legal Team"
                },
                {
                    "step_number": 3,
                    "title": "Consent Management Review",
                    "description": "Review and update consent mechanisms and privacy notices",
                    "required_documentation": "Updated privacy policy, consent forms, opt-out mechanisms",
                    "estimated_duration_hours": 12,
                    "responsible_role": "Legal Team"
                },
                {
                    "step_number": 4,
                    "title": "Data Subject Rights Implementation",
                    "description": "Implement processes for handling data subject requests",
                    "required_documentation": "Request handling procedures, response templates, tracking system",
                    "estimated_duration_hours": 20,
                    "responsible_role": "Data Protection Officer"
                }
            ],
            2: [  # Financial Controls Review (SOX)
                {
                    "step_number": 1,
                    "title": "Internal Controls Documentation",
                    "description": "Document all financial reporting internal controls",
                    "required_documentation": "Control matrices, process flowcharts, control descriptions",
                    "estimated_duration_hours": 40,
                    "responsible_role": "Internal Audit"
                },
                {
                    "step_number": 2,
                    "title": "Control Testing and Evaluation",
                    "description": "Test effectiveness of internal controls over financial reporting",
                    "required_documentation": "Testing procedures, test results, deficiency reports",
                    "estimated_duration_hours": 60,
                    "responsible_role": "Internal Audit"
                },
                {
                    "step_number": 3,
                    "title": "Management Assessment",
                    "description": "Management assessment of internal control effectiveness",
                    "required_documentation": "Management assessment report, certification letters",
                    "estimated_duration_hours": 20,
                    "responsible_role": "CFO"
                },
                {
                    "step_number": 4,
                    "title": "External Auditor Coordination",
                    "description": "Coordinate with external auditors for SOX compliance review",
                    "required_documentation": "Auditor communications, management letter responses",
                    "estimated_duration_hours": 16,
                    "responsible_role": "Finance Team"
                }
            ],
            3: [  # Security Audit (ISO27001)
                {
                    "step_number": 1,
                    "title": "Information Security Risk Assessment",
                    "description": "Conduct comprehensive information security risk assessment",
                    "required_documentation": "Risk register, threat analysis, vulnerability assessment",
                    "estimated_duration_hours": 32,
                    "responsible_role": "CISO"
                },
                {
                    "step_number": 2,
                    "title": "Security Controls Implementation",
                    "description": "Implement required security controls based on risk assessment",
                    "required_documentation": "Control implementation plan, configuration documents, test results",
                    "estimated_duration_hours": 80,
                    "responsible_role": "IT Security Team"
                },
                {
                    "step_number": 3,
                    "title": "Security Awareness Training",
                    "description": "Conduct security awareness training for all employees",
                    "required_documentation": "Training materials, attendance records, assessment results",
                    "estimated_duration_hours": 24,
                    "responsible_role": "HR Team"
                },
                {
                    "step_number": 4,
                    "title": "Incident Response Plan",
                    "description": "Develop and test incident response procedures",
                    "required_documentation": "Incident response plan, contact lists, test scenarios",
                    "estimated_duration_hours": 16,
                    "responsible_role": "IT Security Team"
                }
            ]
        }
        
        steps = steps_templates.get(compliance_requirement_id, [])
        
        logger.info("Retrieved compliance steps", 
                   compliance_requirement_id=compliance_requirement_id,
                   steps_count=len(steps))
        
        return steps
        
    except Exception as e:
        logger.error("Failed to get compliance steps", 
                    compliance_requirement_id=input_data.get("compliance_requirement_id"), 
                    error=str(e))
        raise


@workflow_activity
async def create_company_steps_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create company compliance step records"""
    try:
        company_compliance_id = input_data.get("company_compliance_id")
        company_id = input_data.get("company_id")
        steps = input_data.get("steps", [])
        
        logger.info("Creating company compliance steps", 
                   company_compliance_id=company_compliance_id,
                   steps_count=len(steps))
        
        created_steps = []
        
        for step in steps:
            # Mock company compliance step creation
            # In real implementation, this would insert into company_compliance_steps table
            company_step = {
                "id": f"ccs_{company_compliance_id}_{step['step_number']}",
                "company_compliance_id": company_compliance_id,
                "compliance_step_id": f"cs_{step['step_number']}",
                "step_number": step["step_number"],
                "title": step["title"],
                "description": step["description"],
                "required_documentation": step["required_documentation"],
                "estimated_duration_hours": step["estimated_duration_hours"],
                "responsible_role": step["responsible_role"],
                "status": "Pending",
                "completed_by": None,
                "completed_at": None,
                "evidence_file_path": None,
                "notes": None
            }
            
            created_steps.append(company_step)
            
            logger.info("Created company compliance step",
                       company_compliance_id=company_compliance_id,
                       step_number=step["step_number"],
                       title=step["title"])
        
        logger.info("Company compliance steps created", 
                   company_compliance_id=company_compliance_id,
                   steps_created=len(created_steps))
        
        return created_steps
        
    except Exception as e:
        logger.error("Failed to create company compliance steps", 
                    company_compliance_id=input_data.get("company_compliance_id"), 
                    error=str(e))
        raise


@workflow_activity
async def calculate_priorities_activity(ctx: WorkflowActivityContext, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Calculate step priorities based on various factors"""
    try:
        logger.info("Calculating step priorities", steps_count=len(steps))
        
        updated_steps = []
        
        for step in steps:
            # Calculate priority based on multiple factors
            priority_score = 0
            
            # Base priority on step number (earlier steps are more important)
            if step["step_number"] == 1:
                priority_score += 3
            elif step["step_number"] == 2:
                priority_score += 2
            else:
                priority_score += 1
            
            # Adjust based on estimated duration (longer tasks get higher priority)
            duration = step.get("estimated_duration_hours", 0)
            if duration > 40:
                priority_score += 2
            elif duration > 20:
                priority_score += 1
            
            # Adjust based on responsible role (critical roles get higher priority)
            role = step.get("responsible_role", "").lower()
            if any(critical_role in role for critical_role in ["ciso", "cfo", "dpo"]):
                priority_score += 2
            elif any(important_role in role for important_role in ["audit", "legal"]):
                priority_score += 1
            
            # Convert score to priority level
            if priority_score >= 6:
                priority = "Critical"
            elif priority_score >= 4:
                priority = "High"
            elif priority_score >= 2:
                priority = "Medium"
            else:
                priority = "Low"
            
            step["priority"] = priority
            step["priority_score"] = priority_score
            
            updated_steps.append(step)
            
            logger.info("Calculated step priority",
                       step_number=step["step_number"],
                       title=step["title"],
                       priority=priority,
                       score=priority_score)
        
        logger.info("Step priorities calculated", 
                   steps_count=len(updated_steps),
                   critical=len([s for s in updated_steps if s["priority"] == "Critical"]),
                   high=len([s for s in updated_steps if s["priority"] == "High"]),
                   medium=len([s for s in updated_steps if s["priority"] == "Medium"]),
                   low=len([s for s in updated_steps if s["priority"] == "Low"]))
        
        return updated_steps
        
    except Exception as e:
        logger.error("Failed to calculate step priorities", error=str(e))
        raise


@workflow_activity
async def assign_roles_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Assign specific people to responsible roles"""
    try:
        steps = input_data.get("steps", [])
        company_id = input_data.get("company_id")
        
        logger.info("Assigning roles to steps", 
                   company_id=company_id,
                   steps_count=len(steps))
        
        # Mock role assignments
        # In real implementation, this would query company org chart or user assignments
        role_assignments = {
            "Data Protection Officer": "sarah.jones@company.com",
            "Legal Team": "legal-team@company.com",
            "Internal Audit": "audit-team@company.com",
            "CFO": "cfo@company.com",
            "Finance Team": "finance-team@company.com",
            "CISO": "security-chief@company.com",
            "IT Security Team": "security-team@company.com",
            "HR Team": "hr-team@company.com"
        }
        
        updated_steps = []
        
        for step in steps:
            responsible_role = step.get("responsible_role")
            assigned_to = role_assignments.get(responsible_role, f"{responsible_role.lower().replace(' ', '.')}@company.com")
            
            step["assigned_to"] = assigned_to
            step["assignment_date"] = ctx.current_utc_datetime.isoformat()
            
            updated_steps.append(step)
            
            logger.info("Assigned step to person",
                       step_number=step["step_number"],
                       title=step["title"],
                       responsible_role=responsible_role,
                       assigned_to=assigned_to)
        
        logger.info("Role assignments completed", 
                   company_id=company_id,
                   steps_assigned=len(updated_steps))
        
        return updated_steps
        
    except Exception as e:
        logger.error("Failed to assign roles", 
                    company_id=input_data.get("company_id"), 
                    error=str(e))
        raise


@workflow_activity
async def create_step_timeline_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create timeline for step execution"""
    try:
        from datetime import datetime, timedelta
        
        steps = input_data.get("steps", [])
        company_compliance_due_date = input_data.get("due_date")
        
        logger.info("Creating step timeline", 
                   steps_count=len(steps),
                   overall_due_date=company_compliance_due_date)
        
        # Parse overall due date
        if company_compliance_due_date:
            overall_due = datetime.fromisoformat(company_compliance_due_date.replace('Z', '+00:00'))
        else:
            overall_due = datetime.now() + timedelta(days=90)
        
        # Sort steps by priority and step number
        sorted_steps = sorted(steps, key=lambda x: (
            {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}.get(x.get("priority", "Medium"), 2),
            x.get("step_number", 999)
        ))
        
        # Calculate timeline working backwards from due date
        current_date = overall_due
        updated_steps = []
        
        for step in reversed(sorted_steps):
            # Calculate step duration with buffer
            estimated_hours = step.get("estimated_duration_hours", 8)
            estimated_days = max(1, (estimated_hours + 7) // 8)  # Convert hours to days, minimum 1 day
            
            # Add buffer based on priority
            priority = step.get("priority", "Medium")
            if priority == "Critical":
                buffer_days = max(2, estimated_days // 2)
            elif priority == "High":
                buffer_days = max(1, estimated_days // 3)
            else:
                buffer_days = max(1, estimated_days // 4)
            
            total_days = estimated_days + buffer_days
            
            # Set step due date
            step_due_date = current_date
            step_start_date = current_date - timedelta(days=total_days)
            
            step["due_date"] = step_due_date.isoformat()
            step["start_date"] = step_start_date.isoformat()
            step["estimated_days"] = estimated_days
            step["buffer_days"] = buffer_days
            step["total_allocated_days"] = total_days
            
            # Move current date back for next step
            current_date = step_start_date - timedelta(days=1)
            
            updated_steps.insert(0, step)  # Insert at beginning to maintain order
            
            logger.info("Set step timeline",
                       step_number=step["step_number"],
                       title=step["title"],
                       priority=priority,
                       start_date=step_start_date.strftime("%Y-%m-%d"),
                       due_date=step_due_date.strftime("%Y-%m-%d"),
                       allocated_days=total_days)
        
        logger.info("Step timeline created", 
                   steps_count=len(updated_steps),
                   timeline_start=updated_steps[0]["start_date"] if updated_steps else None,
                   timeline_end=overall_due.strftime("%Y-%m-%d"))
        
        return updated_steps
        
    except Exception as e:
        logger.error("Failed to create step timeline", error=str(e))
        raise


async def step_generation_workflow(ctx: WorkflowContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main step generation workflow
    
    Steps:
    1. Get compliance steps template
    2. Create company compliance step records
    3. Calculate step priorities
    4. Assign roles to specific people
    5. Create execution timeline
    """
    try:
        company_compliance_id = input_data.get("company_compliance_id")
        company_id = input_data.get("company_id")
        compliance_requirement_id = input_data.get("compliance_requirement_id")
        
        logger.info("Starting step generation workflow", 
                   company_compliance_id=company_compliance_id,
                   company_id=company_id,
                   compliance_requirement_id=compliance_requirement_id)
        
        # Step 1: Get compliance steps template
        steps_input = {"compliance_requirement_id": compliance_requirement_id}
        steps_template = await ctx.call_activity(
            get_compliance_steps_activity,
            input=steps_input
        )
        
        if not steps_template:
            logger.warning("No steps template found", 
                          compliance_requirement_id=compliance_requirement_id)
            return {
                "success": True,
                "company_compliance_id": company_compliance_id,
                "message": "No steps template found for this compliance requirement",
                "steps": []
            }
        
        # Step 2: Create company compliance step records
        create_steps_input = {
            "company_compliance_id": company_compliance_id,
            "company_id": company_id,
            "steps": steps_template
        }
        
        company_steps = await ctx.call_activity(
            create_company_steps_activity,
            input=create_steps_input
        )
        
        # Step 3: Calculate step priorities
        prioritized_steps = await ctx.call_activity(
            calculate_priorities_activity,
            input=company_steps
        )
        
        # Step 4: Assign roles to specific people
        assignment_input = {
            "steps": prioritized_steps,
            "company_id": company_id
        }
        
        assigned_steps = await ctx.call_activity(
            assign_roles_activity,
            input=assignment_input
        )
        
        # Step 5: Create execution timeline
        timeline_input = {
            "steps": assigned_steps,
            "due_date": input_data.get("due_date")
        }
        
        final_steps = await ctx.call_activity(
            create_step_timeline_activity,
            input=timeline_input
        )
        
        # Workflow completion
        result = {
            "success": True,
            "company_compliance_id": company_compliance_id,
            "company_id": company_id,
            "compliance_requirement_id": compliance_requirement_id,
            "steps": final_steps,
            "summary": {
                "total_steps": len(final_steps),
                "critical_steps": len([s for s in final_steps if s.get("priority") == "Critical"]),
                "high_priority_steps": len([s for s in final_steps if s.get("priority") == "High"]),
                "total_estimated_hours": sum(s.get("estimated_duration_hours", 0) for s in final_steps),
                "timeline_start": final_steps[0]["start_date"] if final_steps else None,
                "timeline_end": final_steps[-1]["due_date"] if final_steps else None
            }
        }
        
        logger.info("Step generation workflow completed successfully",
                   company_compliance_id=company_compliance_id,
                   steps_created=len(final_steps),
                   total_hours=result["summary"]["total_estimated_hours"])
        
        return result
        
    except Exception as e:
        logger.error("Step generation workflow failed", 
                    company_compliance_id=input_data.get("company_compliance_id"), 
                    error=str(e))
        
        return {
            "success": False,
            "company_compliance_id": input_data.get("company_compliance_id"),
            "error": str(e),
            "message": "Step generation workflow failed"
        }
