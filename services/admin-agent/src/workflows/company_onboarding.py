"""
Company Onboarding Workflow
Analyzes companies and assigns compliance requirements based on industry and location
"""

from typing import Dict, Any, List
from dapr.ext.workflow import WorkflowContext, WorkflowActivityContext, workflow_activity
from dapr.ext.workflow import when_any, when_all
import structlog

logger = structlog.get_logger(__name__)


@workflow_activity
async def analyze_company_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze company details and extract key information"""
    try:
        company_id = input_data.get("company_id")
        company_name = input_data.get("company_name")
        industry = input_data.get("industry")
        location = input_data.get("location")
        
        logger.info("Analyzing company", 
                   company_id=company_id, 
                   company_name=company_name,
                   industry=industry, 
                   location=location)
        
        # Analyze industry and location to determine compliance scope
        analysis_result = {
            "company_id": company_id,
            "company_name": company_name,
            "industry": industry.lower() if industry else "",
            "location": location.lower() if location else "",
            "risk_level": "medium",  # Default risk level
            "compliance_scope": []
        }
        
        # Determine compliance scope based on industry
        if "technology" in analysis_result["industry"]:
            analysis_result["compliance_scope"].extend(["data_protection", "security"])
            analysis_result["risk_level"] = "high"
        
        if "finance" in analysis_result["industry"]:
            analysis_result["compliance_scope"].extend(["financial_controls", "data_protection", "security"])
            analysis_result["risk_level"] = "critical"
        
        if "healthcare" in analysis_result["industry"]:
            analysis_result["compliance_scope"].extend(["data_protection", "security", "healthcare_specific"])
            analysis_result["risk_level"] = "high"
        
        # Location-specific requirements
        if "australia" in analysis_result["location"]:
            analysis_result["compliance_scope"].append("australian_privacy")
        
        logger.info("Company analysis completed", 
                   company_id=company_id,
                   risk_level=analysis_result["risk_level"],
                   compliance_scope=analysis_result["compliance_scope"])
        
        return analysis_result
        
    except Exception as e:
        logger.error("Failed to analyze company", company_id=input_data.get("company_id"), error=str(e))
        raise


@workflow_activity
async def find_compliance_requirements_activity(ctx: WorkflowActivityContext, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find matching compliance requirements based on analysis"""
    try:
        industry = analysis_data.get("industry", "")
        location = analysis_data.get("location", "")
        compliance_scope = analysis_data.get("compliance_scope", [])
        
        logger.info("Finding compliance requirements", 
                   industry=industry, 
                   location=location,
                   scope=compliance_scope)
        
        # Mock compliance requirements matching
        # In real implementation, this would query the database
        matching_requirements = []
        
        # Technology industry requirements
        if "technology" in industry:
            matching_requirements.extend([
                {
                    "id": 1,
                    "name": "Data Protection Assessment",
                    "framework": "GDPR",
                    "severity_level": "High",
                    "mandatory": True
                },
                {
                    "id": 3,
                    "name": "Security Audit",
                    "framework": "ISO27001", 
                    "severity_level": "High",
                    "mandatory": True
                }
            ])
        
        # Finance industry requirements
        if "finance" in industry:
            matching_requirements.extend([
                {
                    "id": 1,
                    "name": "Data Protection Assessment",
                    "framework": "GDPR",
                    "severity_level": "High",
                    "mandatory": True
                },
                {
                    "id": 2,
                    "name": "Financial Controls Review",
                    "framework": "SOX",
                    "severity_level": "Critical",
                    "mandatory": True
                },
                {
                    "id": 3,
                    "name": "Security Audit",
                    "framework": "ISO27001",
                    "severity_level": "High", 
                    "mandatory": True
                }
            ])
        
        # Healthcare industry requirements
        if "healthcare" in industry:
            matching_requirements.extend([
                {
                    "id": 1,
                    "name": "Data Protection Assessment",
                    "framework": "GDPR",
                    "severity_level": "High",
                    "mandatory": True
                },
                {
                    "id": 3,
                    "name": "Security Audit",
                    "framework": "ISO27001",
                    "severity_level": "High",
                    "mandatory": True
                }
            ])
        
        # Remove duplicates based on ID
        unique_requirements = []
        seen_ids = set()
        for req in matching_requirements:
            if req["id"] not in seen_ids:
                unique_requirements.append(req)
                seen_ids.add(req["id"])
        
        logger.info("Found compliance requirements", 
                   count=len(unique_requirements),
                   requirements=[r["name"] for r in unique_requirements])
        
        return unique_requirements
        
    except Exception as e:
        logger.error("Failed to find compliance requirements", error=str(e))
        raise


@workflow_activity
async def create_company_compliance_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create company compliance records"""
    try:
        company_id = input_data.get("company_id")
        requirements = input_data.get("requirements", [])
        risk_level = input_data.get("risk_level", "medium")
        
        logger.info("Creating company compliance records", 
                   company_id=company_id,
                   requirement_count=len(requirements))
        
        created_records = []
        
        for requirement in requirements:
            # Mock company compliance record creation
            # In real implementation, this would insert into database
            compliance_record = {
                "id": f"cc_{company_id}_{requirement['id']}",
                "company_id": company_id,
                "compliance_requirement_id": requirement["id"],
                "status": "Not Started",
                "assigned_to": None,
                "due_date": None,
                "priority": requirement.get("severity_level", "Medium"),
                "mandatory": requirement.get("mandatory", True),
                "framework": requirement.get("framework"),
                "requirement_name": requirement.get("name")
            }
            
            created_records.append(compliance_record)
            
            logger.info("Created compliance record",
                       company_id=company_id,
                       requirement_name=requirement.get("name"),
                       framework=requirement.get("framework"))
        
        logger.info("Company compliance records created", 
                   company_id=company_id,
                   records_created=len(created_records))
        
        return created_records
        
    except Exception as e:
        logger.error("Failed to create company compliance records", 
                    company_id=input_data.get("company_id"), 
                    error=str(e))
        raise


@workflow_activity
async def set_due_dates_activity(ctx: WorkflowActivityContext, compliance_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Set due dates for compliance records based on priority and framework"""
    try:
        from datetime import datetime, timedelta
        
        logger.info("Setting due dates for compliance records", count=len(compliance_records))
        
        updated_records = []
        
        for record in compliance_records:
            # Calculate due date based on priority and framework
            days_to_add = 90  # Default 90 days
            
            if record.get("priority") == "Critical":
                days_to_add = 30
            elif record.get("priority") == "High":
                days_to_add = 60
            elif record.get("priority") == "Medium":
                days_to_add = 90
            else:
                days_to_add = 120
            
            # Framework-specific adjustments
            framework = record.get("framework", "")
            if framework == "SOX":
                days_to_add = min(days_to_add, 45)  # SOX is time-sensitive
            elif framework == "GDPR":
                days_to_add = min(days_to_add, 60)  # GDPR has strict timelines
            
            due_date = datetime.now() + timedelta(days=days_to_add)
            record["due_date"] = due_date.isoformat()
            record["days_to_complete"] = days_to_add
            
            updated_records.append(record)
            
            logger.info("Set due date for compliance record",
                       requirement_name=record.get("requirement_name"),
                       framework=framework,
                       priority=record.get("priority"),
                       due_date=due_date.strftime("%Y-%m-%d"),
                       days_to_complete=days_to_add)
        
        logger.info("Due dates set for all compliance records", count=len(updated_records))
        
        return updated_records
        
    except Exception as e:
        logger.error("Failed to set due dates", error=str(e))
        raise


@workflow_activity
async def send_onboarding_notifications_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send notifications about company onboarding completion"""
    try:
        company_id = input_data.get("company_id")
        company_name = input_data.get("company_name")
        compliance_records = input_data.get("compliance_records", [])
        
        logger.info("Sending onboarding notifications", 
                   company_id=company_id,
                   company_name=company_name)
        
        # Mock notification sending
        # In real implementation, this would send emails, Slack messages, etc.
        notifications_sent = []
        
        # Notification to compliance team
        compliance_notification = {
            "type": "email",
            "recipient": "compliance-team@company.com",
            "subject": f"New Company Onboarded: {company_name}",
            "message": f"Company {company_name} (ID: {company_id}) has been onboarded with {len(compliance_records)} compliance requirements.",
            "sent_at": datetime.now().isoformat()
        }
        notifications_sent.append(compliance_notification)
        
        # Notification for each high-priority requirement
        for record in compliance_records:
            if record.get("priority") in ["Critical", "High"]:
                priority_notification = {
                    "type": "slack",
                    "channel": "#compliance-alerts",
                    "message": f"🚨 {record.get('priority')} priority compliance requirement assigned: {record.get('requirement_name')} for {company_name}",
                    "sent_at": datetime.now().isoformat()
                }
                notifications_sent.append(priority_notification)
        
        logger.info("Onboarding notifications sent", 
                   company_id=company_id,
                   notifications_count=len(notifications_sent))
        
        return {
            "company_id": company_id,
            "notifications_sent": len(notifications_sent),
            "notification_details": notifications_sent
        }
        
    except Exception as e:
        logger.error("Failed to send onboarding notifications", 
                    company_id=input_data.get("company_id"), 
                    error=str(e))
        raise


async def company_onboarding_workflow(ctx: WorkflowContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main company onboarding workflow
    
    Steps:
    1. Analyze company details
    2. Find matching compliance requirements
    3. Create company compliance records
    4. Set due dates
    5. Send notifications
    """
    try:
        logger.info("Starting company onboarding workflow", 
                   company_id=input_data.get("company_id"),
                   company_name=input_data.get("company_name"))
        
        # Step 1: Analyze company
        analysis_result = await ctx.call_activity(
            analyze_company_activity,
            input=input_data
        )
        
        # Step 2: Find compliance requirements
        requirements = await ctx.call_activity(
            find_compliance_requirements_activity,
            input=analysis_result
        )
        
        if not requirements:
            logger.warning("No compliance requirements found", 
                          company_id=input_data.get("company_id"))
            return {
                "success": True,
                "company_id": input_data.get("company_id"),
                "message": "No compliance requirements found for this company",
                "compliance_records": []
            }
        
        # Step 3: Create company compliance records
        compliance_input = {
            "company_id": analysis_result["company_id"],
            "requirements": requirements,
            "risk_level": analysis_result["risk_level"]
        }
        
        compliance_records = await ctx.call_activity(
            create_company_compliance_activity,
            input=compliance_input
        )
        
        # Step 4: Set due dates
        updated_records = await ctx.call_activity(
            set_due_dates_activity,
            input=compliance_records
        )
        
        # Step 5: Send notifications
        notification_input = {
            "company_id": input_data.get("company_id"),
            "company_name": input_data.get("company_name"),
            "compliance_records": updated_records
        }
        
        notification_result = await ctx.call_activity(
            send_onboarding_notifications_activity,
            input=notification_input
        )
        
        # Workflow completion
        result = {
            "success": True,
            "company_id": input_data.get("company_id"),
            "company_name": input_data.get("company_name"),
            "analysis": analysis_result,
            "compliance_records": updated_records,
            "notifications": notification_result,
            "summary": {
                "requirements_assigned": len(updated_records),
                "critical_requirements": len([r for r in updated_records if r.get("priority") == "Critical"]),
                "high_priority_requirements": len([r for r in updated_records if r.get("priority") == "High"]),
                "notifications_sent": notification_result.get("notifications_sent", 0)
            }
        }
        
        logger.info("Company onboarding workflow completed successfully",
                   company_id=input_data.get("company_id"),
                   requirements_assigned=len(updated_records),
                   notifications_sent=notification_result.get("notifications_sent", 0))
        
        return result
        
    except Exception as e:
        logger.error("Company onboarding workflow failed", 
                    company_id=input_data.get("company_id"), 
                    error=str(e))
        
        return {
            "success": False,
            "company_id": input_data.get("company_id"),
            "error": str(e),
            "message": "Company onboarding workflow failed"
        }
