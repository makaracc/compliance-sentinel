"""
Compliance Reporting Workflow
Generates comprehensive compliance status reports and analytics
"""

from typing import Dict, Any, List
from dapr.ext.workflow import WorkflowContext, WorkflowActivityContext, workflow_activity
import structlog

logger = structlog.get_logger(__name__)


@workflow_activity
async def gather_company_data_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Gather comprehensive company data"""
    try:
        company_id = input_data.get("company_id")
        
        logger.info("Gathering company data", company_id=company_id)
        
        # Mock company data gathering
        # In real implementation, this would query companies table
        company_data = {
            "company_id": company_id,
            "name": "TechCorp Australia",
            "industry": "technology",
            "location": "Australia",
            "contact_email": "compliance@techcorp.com.au",
            "employee_count": 250,
            "annual_revenue": 50000000,
            "data_processing_volume": "high",
            "regulatory_jurisdictions": ["Australia", "EU", "US"],
            "business_units": ["Engineering", "Sales", "Marketing", "HR", "Finance"],
            "onboarding_date": "2024-01-15T00:00:00Z"
        }
        
        logger.info("Company data gathered", 
                   company_id=company_id,
                   company_name=company_data["name"])
        
        return company_data
        
    except Exception as e:
        logger.error("Failed to gather company data", 
                    company_id=input_data.get("company_id"), 
                    error=str(e))
        raise


@workflow_activity
async def collect_compliance_status_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect compliance status for all requirements"""
    try:
        company_id = input_data.get("company_id")
        
        logger.info("Collecting compliance status", company_id=company_id)
        
        # Mock compliance status collection
        # In real implementation, this would query company_compliance table
        compliance_status = [
            {
                "compliance_requirement_id": 1,
                "requirement_name": "Data Protection Assessment",
                "framework": "GDPR",
                "status": "Completed",
                "completion_percentage": 100,
                "due_date": "2024-07-15",
                "completion_date": "2024-07-10",
                "assigned_to": "sarah.jones@company.com",
                "priority": "High",
                "total_steps": 4,
                "completed_steps": 4,
                "overall_score": 92,
                "last_updated": "2024-07-10T14:30:00Z"
            },
            {
                "compliance_requirement_id": 2,
                "requirement_name": "Financial Controls Review",
                "framework": "SOX",
                "status": "In Progress",
                "completion_percentage": 75,
                "due_date": "2024-08-30",
                "completion_date": None,
                "assigned_to": "audit-team@company.com",
                "priority": "Critical",
                "total_steps": 4,
                "completed_steps": 3,
                "overall_score": 85,
                "last_updated": "2024-07-12T09:15:00Z"
            },
            {
                "compliance_requirement_id": 3,
                "requirement_name": "Security Audit",
                "framework": "ISO27001",
                "status": "In Progress",
                "completion_percentage": 50,
                "due_date": "2024-09-15",
                "completion_date": None,
                "assigned_to": "security-team@company.com",
                "priority": "High",
                "total_steps": 4,
                "completed_steps": 2,
                "overall_score": 78,
                "last_updated": "2024-07-11T16:45:00Z"
            }
        ]
        
        logger.info("Compliance status collected", 
                   company_id=company_id,
                   requirements_count=len(compliance_status))
        
        return compliance_status
        
    except Exception as e:
        logger.error("Failed to collect compliance status", 
                    company_id=input_data.get("company_id"), 
                    error=str(e))
        raise


@workflow_activity
async def aggregate_step_progress_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Aggregate detailed step progress across all compliance requirements"""
    try:
        company_id = input_data.get("company_id")
        compliance_status = input_data.get("compliance_status", [])
        
        logger.info("Aggregating step progress", 
                   company_id=company_id,
                   requirements_count=len(compliance_status))
        
        # Mock step progress aggregation
        # In real implementation, this would query company_compliance_steps table
        step_progress = {
            "total_steps": 0,
            "completed_steps": 0,
            "in_progress_steps": 0,
            "pending_steps": 0,
            "overdue_steps": 0,
            "steps_by_priority": {
                "Critical": {"total": 0, "completed": 0},
                "High": {"total": 0, "completed": 0},
                "Medium": {"total": 0, "completed": 0},
                "Low": {"total": 0, "completed": 0}
            },
            "steps_by_framework": {},
            "average_completion_time": 12.5,  # days
            "evidence_quality_scores": []
        }
        
        for compliance in compliance_status:
            total_steps = compliance.get("total_steps", 0)
            completed_steps = compliance.get("completed_steps", 0)
            framework = compliance.get("framework", "Unknown")
            
            step_progress["total_steps"] += total_steps
            step_progress["completed_steps"] += completed_steps
            
            # Calculate in-progress and pending
            if compliance.get("status") == "In Progress":
                step_progress["in_progress_steps"] += (total_steps - completed_steps)
            elif compliance.get("status") == "Not Started":
                step_progress["pending_steps"] += total_steps
            
            # Framework breakdown
            if framework not in step_progress["steps_by_framework"]:
                step_progress["steps_by_framework"][framework] = {
                    "total": 0, "completed": 0, "completion_rate": 0
                }
            
            step_progress["steps_by_framework"][framework]["total"] += total_steps
            step_progress["steps_by_framework"][framework]["completed"] += completed_steps
        
        # Calculate completion rates
        for framework_data in step_progress["steps_by_framework"].values():
            if framework_data["total"] > 0:
                framework_data["completion_rate"] = round(
                    (framework_data["completed"] / framework_data["total"]) * 100, 1
                )
        
        # Mock evidence quality scores
        step_progress["evidence_quality_scores"] = [92, 85, 78, 88, 95, 82]
        step_progress["average_evidence_quality"] = round(
            sum(step_progress["evidence_quality_scores"]) / len(step_progress["evidence_quality_scores"]), 1
        )
        
        logger.info("Step progress aggregated", 
                   company_id=company_id,
                   total_steps=step_progress["total_steps"],
                   completed_steps=step_progress["completed_steps"])
        
        return step_progress
        
    except Exception as e:
        logger.error("Failed to aggregate step progress", 
                    company_id=input_data.get("company_id"), 
                    error=str(e))
        raise


@workflow_activity
async def calculate_completion_rates_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate various completion rates and metrics"""
    try:
        compliance_status = input_data.get("compliance_status", [])
        step_progress = input_data.get("step_progress", {})
        
        logger.info("Calculating completion rates")
        
        # Overall completion metrics
        total_requirements = len(compliance_status)
        completed_requirements = len([c for c in compliance_status if c.get("status") == "Completed"])
        in_progress_requirements = len([c for c in compliance_status if c.get("status") == "In Progress"])
        not_started_requirements = len([c for c in compliance_status if c.get("status") == "Not Started"])
        
        # Calculate rates
        overall_completion_rate = (completed_requirements / total_requirements * 100) if total_requirements > 0 else 0
        step_completion_rate = (step_progress.get("completed_steps", 0) / step_progress.get("total_steps", 1) * 100)
        
        # Priority-based completion
        critical_requirements = [c for c in compliance_status if c.get("priority") == "Critical"]
        critical_completion_rate = (
            len([c for c in critical_requirements if c.get("status") == "Completed"]) / 
            len(critical_requirements) * 100
        ) if critical_requirements else 100
        
        # Time-based metrics
        from datetime import datetime, timedelta
        current_date = datetime.now()
        overdue_requirements = []
        
        for compliance in compliance_status:
            if compliance.get("due_date") and compliance.get("status") != "Completed":
                due_date = datetime.fromisoformat(compliance["due_date"].replace('Z', '+00:00'))
                if due_date < current_date:
                    overdue_requirements.append(compliance)
        
        completion_metrics = {
            "overall_completion_rate": round(overall_completion_rate, 1),
            "step_completion_rate": round(step_completion_rate, 1),
            "critical_completion_rate": round(critical_completion_rate, 1),
            "requirements_summary": {
                "total": total_requirements,
                "completed": completed_requirements,
                "in_progress": in_progress_requirements,
                "not_started": not_started_requirements,
                "overdue": len(overdue_requirements)
            },
            "step_summary": {
                "total": step_progress.get("total_steps", 0),
                "completed": step_progress.get("completed_steps", 0),
                "in_progress": step_progress.get("in_progress_steps", 0),
                "pending": step_progress.get("pending_steps", 0)
            },
            "performance_indicators": {
                "on_track": overall_completion_rate >= 80,
                "critical_compliance_met": critical_completion_rate >= 90,
                "no_overdue_items": len(overdue_requirements) == 0,
                "quality_threshold_met": step_progress.get("average_evidence_quality", 0) >= 85
            },
            "risk_level": "low" if overall_completion_rate >= 90 else "medium" if overall_completion_rate >= 70 else "high"
        }
        
        logger.info("Completion rates calculated", 
                   overall_rate=completion_metrics["overall_completion_rate"],
                   step_rate=completion_metrics["step_completion_rate"],
                   risk_level=completion_metrics["risk_level"])
        
        return completion_metrics
        
    except Exception as e:
        logger.error("Failed to calculate completion rates", error=str(e))
        raise


@workflow_activity
async def identify_overdue_items_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify overdue compliance items and steps"""
    try:
        compliance_status = input_data.get("compliance_status", [])
        
        logger.info("Identifying overdue items")
        
        from datetime import datetime
        current_date = datetime.now()
        
        overdue_items = []
        
        for compliance in compliance_status:
            if compliance.get("status") != "Completed" and compliance.get("due_date"):
                due_date = datetime.fromisoformat(compliance["due_date"].replace('Z', '+00:00'))
                
                if due_date < current_date:
                    days_overdue = (current_date - due_date).days
                    
                    overdue_item = {
                        "type": "compliance_requirement",
                        "id": compliance["compliance_requirement_id"],
                        "name": compliance["requirement_name"],
                        "framework": compliance["framework"],
                        "due_date": compliance["due_date"],
                        "days_overdue": days_overdue,
                        "assigned_to": compliance["assigned_to"],
                        "priority": compliance["priority"],
                        "completion_percentage": compliance["completion_percentage"],
                        "urgency": "critical" if days_overdue > 30 else "high" if days_overdue > 14 else "medium"
                    }
                    
                    overdue_items.append(overdue_item)
        
        # Sort by days overdue (most overdue first)
        overdue_items.sort(key=lambda x: x["days_overdue"], reverse=True)
        
        logger.info("Overdue items identified", count=len(overdue_items))
        
        return overdue_items
        
    except Exception as e:
        logger.error("Failed to identify overdue items", error=str(e))
        raise


@workflow_activity
async def generate_insights_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate insights and recommendations"""
    try:
        company_data = input_data.get("company_data", {})
        completion_metrics = input_data.get("completion_metrics", {})
        overdue_items = input_data.get("overdue_items", [])
        
        logger.info("Generating insights and recommendations")
        
        insights = {
            "key_insights": [],
            "recommendations": [],
            "risk_assessment": {
                "overall_risk": completion_metrics.get("risk_level", "medium"),
                "risk_factors": [],
                "mitigation_strategies": []
            },
            "performance_trends": {
                "completion_velocity": "steady",  # Mock trend
                "quality_trend": "improving",     # Mock trend
                "resource_utilization": "optimal" # Mock trend
            },
            "benchmarking": {
                "industry_average_completion": 75,
                "company_performance": completion_metrics.get("overall_completion_rate", 0),
                "performance_vs_industry": "above_average"
            }
        }
        
        # Generate key insights
        overall_rate = completion_metrics.get("overall_completion_rate", 0)
        
        if overall_rate >= 90:
            insights["key_insights"].append("Excellent compliance performance - company is exceeding industry standards")
        elif overall_rate >= 75:
            insights["key_insights"].append("Good compliance progress - on track to meet regulatory requirements")
        else:
            insights["key_insights"].append("Compliance performance needs improvement - risk of regulatory issues")
        
        if len(overdue_items) > 0:
            insights["key_insights"].append(f"{len(overdue_items)} compliance items are overdue and require immediate attention")
        
        critical_rate = completion_metrics.get("critical_completion_rate", 0)
        if critical_rate < 90:
            insights["key_insights"].append("Critical compliance requirements need prioritization")
        
        # Generate recommendations
        if len(overdue_items) > 0:
            insights["recommendations"].append({
                "priority": "high",
                "category": "overdue_items",
                "recommendation": "Address overdue compliance items immediately",
                "action_items": [
                    "Review resource allocation for overdue items",
                    "Escalate critical overdue requirements to management",
                    "Implement accelerated completion timeline"
                ]
            })
        
        if overall_rate < 80:
            insights["recommendations"].append({
                "priority": "medium",
                "category": "performance_improvement",
                "recommendation": "Improve overall compliance completion rate",
                "action_items": [
                    "Increase resource allocation to compliance activities",
                    "Provide additional training to compliance teams",
                    "Implement automated compliance tracking tools"
                ]
            })
        
        # Risk assessment
        if len(overdue_items) > 2:
            insights["risk_assessment"]["risk_factors"].append("Multiple overdue compliance requirements")
        
        if critical_rate < 80:
            insights["risk_assessment"]["risk_factors"].append("Critical compliance requirements not meeting targets")
        
        # Mitigation strategies
        insights["risk_assessment"]["mitigation_strategies"] = [
            "Implement weekly compliance review meetings",
            "Establish clear escalation procedures for overdue items",
            "Invest in compliance automation tools",
            "Conduct regular compliance training programs"
        ]
        
        logger.info("Insights generated", 
                   insights_count=len(insights["key_insights"]),
                   recommendations_count=len(insights["recommendations"]))
        
        return insights
        
    except Exception as e:
        logger.error("Failed to generate insights", error=str(e))
        raise


@workflow_activity
async def format_report_activity(ctx: WorkflowActivityContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the final compliance report"""
    try:
        from datetime import datetime
        
        logger.info("Formatting compliance report")
        
        report_id = f"cr_{int(datetime.now().timestamp())}"
        
        formatted_report = {
            "report_metadata": {
                "report_id": report_id,
                "report_type": "comprehensive_compliance_status",
                "generated_at": datetime.now().isoformat(),
                "generated_by": "admin-agent-workflow",
                "report_period": "current_status",
                "version": "1.0"
            },
            "executive_summary": {
                "company_name": input_data.get("company_data", {}).get("name", "Unknown"),
                "overall_compliance_rate": input_data.get("completion_metrics", {}).get("overall_completion_rate", 0),
                "risk_level": input_data.get("completion_metrics", {}).get("risk_level", "medium"),
                "total_requirements": input_data.get("completion_metrics", {}).get("requirements_summary", {}).get("total", 0),
                "completed_requirements": input_data.get("completion_metrics", {}).get("requirements_summary", {}).get("completed", 0),
                "overdue_items": len(input_data.get("overdue_items", [])),
                "key_achievements": [
                    "GDPR compliance assessment completed successfully",
                    "Security framework implementation in progress",
                    "Financial controls review 75% complete"
                ],
                "immediate_actions_required": len([item for item in input_data.get("overdue_items", []) if item.get("urgency") == "critical"])
            },
            "detailed_sections": {
                "company_profile": input_data.get("company_data", {}),
                "compliance_status": input_data.get("compliance_status", []),
                "step_progress": input_data.get("step_progress", {}),
                "completion_metrics": input_data.get("completion_metrics", {}),
                "overdue_analysis": input_data.get("overdue_items", []),
                "insights_and_recommendations": input_data.get("insights", {})
            },
            "appendices": {
                "methodology": "Automated compliance tracking and analysis using Dapr workflows",
                "data_sources": ["company_compliance table", "company_compliance_steps table", "compliance_requirements table"],
                "report_limitations": ["Data current as of report generation time", "Manual verification recommended for critical decisions"]
            }
        }
        
        logger.info("Report formatted", 
                   report_id=report_id,
                   sections_count=len(formatted_report["detailed_sections"]))
        
        return formatted_report
        
    except Exception as e:
        logger.error("Failed to format report", error=str(e))
        raise


@workflow_activity
async def send_report_activity(ctx: WorkflowActivityContext, report: Dict[str, Any]) -> Dict[str, Any]:
    """Send the compliance report to stakeholders"""
    try:
        report_id = report.get("report_metadata", {}).get("report_id")
        company_name = report.get("executive_summary", {}).get("company_name")
        
        logger.info("Sending compliance report", 
                   report_id=report_id,
                   company_name=company_name)
        
        # Mock report distribution
        # In real implementation, this would send emails, save to file system, etc.
        distribution_result = {
            "report_id": report_id,
            "distribution_channels": [
                {
                    "channel": "email",
                    "recipients": ["compliance-team@company.com", "management@company.com"],
                    "status": "sent",
                    "sent_at": ctx.current_utc_datetime.isoformat()
                },
                {
                    "channel": "dashboard",
                    "location": "/reports/compliance/latest",
                    "status": "published",
                    "published_at": ctx.current_utc_datetime.isoformat()
                },
                {
                    "channel": "file_system",
                    "location": f"/reports/compliance/{report_id}.json",
                    "status": "saved",
                    "saved_at": ctx.current_utc_datetime.isoformat()
                }
            ],
            "access_links": [
                f"https://compliance-dashboard.company.com/reports/{report_id}",
                f"https://api.company.com/compliance/reports/{report_id}"
            ],
            "notifications_sent": 5
        }
        
        logger.info("Report sent successfully", 
                   report_id=report_id,
                   channels=len(distribution_result["distribution_channels"]),
                   notifications=distribution_result["notifications_sent"])
        
        return distribution_result
        
    except Exception as e:
        logger.error("Failed to send report", error=str(e))
        raise


async def compliance_reporting_workflow(ctx: WorkflowContext, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main compliance reporting workflow
    
    Steps:
    1. Gather company data
    2. Collect compliance status
    3. Aggregate step progress
    4. Calculate completion rates
    5. Identify overdue items
    6. Generate insights
    7. Format report
    8. Send report
    """
    try:
        company_id = input_data.get("company_id")
        report_type = input_data.get("report_type", "comprehensive")
        
        logger.info("Starting compliance reporting workflow", 
                   company_id=company_id,
                   report_type=report_type)
        
        # Step 1: Gather company data
        company_data = await ctx.call_activity(
            gather_company_data_activity,
            input=input_data
        )
        
        # Step 2: Collect compliance status
        compliance_status = await ctx.call_activity(
            collect_compliance_status_activity,
            input={"company_id": company_id}
        )
        
        # Step 3: Aggregate step progress
        step_progress_input = {
            "company_id": company_id,
            "compliance_status": compliance_status
        }
        
        step_progress = await ctx.call_activity(
            aggregate_step_progress_activity,
            input=step_progress_input
        )
        
        # Step 4: Calculate completion rates
        completion_rates_input = {
            "compliance_status": compliance_status,
            "step_progress": step_progress
        }
        
        completion_metrics = await ctx.call_activity(
            calculate_completion_rates_activity,
            input=completion_rates_input
        )
        
        # Step 5: Identify overdue items
        overdue_items = await ctx.call_activity(
            identify_overdue_items_activity,
            input={"compliance_status": compliance_status}
        )
        
        # Step 6: Generate insights
        insights_input = {
            "company_data": company_data,
            "completion_metrics": completion_metrics,
            "overdue_items": overdue_items
        }
        
        insights = await ctx.call_activity(
            generate_insights_activity,
            input=insights_input
        )
        
        # Step 7: Format report
        format_input = {
            "company_data": company_data,
            "compliance_status": compliance_status,
            "step_progress": step_progress,
            "completion_metrics": completion_metrics,
            "overdue_items": overdue_items,
            "insights": insights
        }
        
        formatted_report = await ctx.call_activity(
            format_report_activity,
            input=format_input
        )
        
        # Step 8: Send report
        distribution_result = await ctx.call_activity(
            send_report_activity,
            input=formatted_report
        )
        
        # Workflow completion
        result = {
            "success": True,
            "company_id": company_id,
            "report": formatted_report,
            "distribution": distribution_result,
            "summary": {
                "report_id": formatted_report.get("report_metadata", {}).get("report_id"),
                "overall_compliance_rate": completion_metrics.get("overall_completion_rate", 0),
                "risk_level": completion_metrics.get("risk_level", "medium"),
                "overdue_items_count": len(overdue_items),
                "recommendations_count": len(insights.get("recommendations", [])),
                "report_sent": True,
                "notifications_sent": distribution_result.get("notifications_sent", 0)
            }
        }
        
        logger.info("Compliance reporting workflow completed successfully",
                   company_id=company_id,
                   report_id=result["summary"]["report_id"],
                   compliance_rate=result["summary"]["overall_compliance_rate"])
        
        return result
        
    except Exception as e:
        logger.error("Compliance reporting workflow failed", 
                    company_id=input_data.get("company_id"), 
                    error=str(e))
        
        return {
            "success": False,
            "company_id": input_data.get("company_id"),
            "error": str(e),
            "message": "Compliance reporting workflow failed"
        }
