"""
Step Generator Agent
Creates detailed compliance steps for company compliance requirements
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta, timezone
import structlog

logger = structlog.get_logger(__name__)


class StepGeneratorAgent:
    """Agent for generating detailed compliance steps"""
    
    def __init__(self):
        self.name = "step_generator_agent"
        self.version = "1.0.0"
        self.capabilities = [
            "step_template_generation",
            "timeline_planning",
            "resource_estimation",
            "dependency_mapping"
        ]
        
        # Step templates for different compliance frameworks
        self.step_templates = {
            "GDPR": [
                {
                    "step_number": 1,
                    "title": "Data Inventory and Mapping",
                    "description": "Identify and document all personal data processing activities",
                    "category": "assessment",
                    "complexity": "medium",
                    "base_hours": 16,
                    "required_skills": ["data_analysis", "process_mapping"],
                    "deliverables": ["Data flow diagrams", "Processing records", "Data inventory"]
                },
                {
                    "step_number": 2,
                    "title": "Privacy Impact Assessment",
                    "description": "Conduct privacy impact assessment for high-risk processing",
                    "category": "assessment",
                    "complexity": "high",
                    "base_hours": 24,
                    "required_skills": ["legal_analysis", "risk_assessment"],
                    "deliverables": ["PIA report", "Risk assessment", "Mitigation measures"]
                },
                {
                    "step_number": 3,
                    "title": "Consent Management Review",
                    "description": "Review and update consent mechanisms and privacy notices",
                    "category": "implementation",
                    "complexity": "medium",
                    "base_hours": 12,
                    "required_skills": ["legal_writing", "ux_design"],
                    "deliverables": ["Updated privacy policy", "Consent forms", "Opt-out mechanisms"]
                },
                {
                    "step_number": 4,
                    "title": "Data Subject Rights Implementation",
                    "description": "Implement processes for handling data subject requests",
                    "category": "implementation",
                    "complexity": "high",
                    "base_hours": 20,
                    "required_skills": ["process_design", "system_integration"],
                    "deliverables": ["Request procedures", "Response templates", "Tracking system"]
                }
            ],
            "SOX": [
                {
                    "step_number": 1,
                    "title": "Internal Controls Documentation",
                    "description": "Document all financial reporting internal controls",
                    "category": "documentation",
                    "complexity": "high",
                    "base_hours": 40,
                    "required_skills": ["financial_analysis", "process_documentation"],
                    "deliverables": ["Control matrices", "Process flowcharts", "Control descriptions"]
                },
                {
                    "step_number": 2,
                    "title": "Control Testing and Evaluation",
                    "description": "Test effectiveness of internal controls over financial reporting",
                    "category": "testing",
                    "complexity": "high",
                    "base_hours": 60,
                    "required_skills": ["audit_testing", "financial_controls"],
                    "deliverables": ["Testing procedures", "Test results", "Deficiency reports"]
                },
                {
                    "step_number": 3,
                    "title": "Management Assessment",
                    "description": "Management assessment of internal control effectiveness",
                    "category": "assessment",
                    "complexity": "medium",
                    "base_hours": 20,
                    "required_skills": ["management_review", "financial_reporting"],
                    "deliverables": ["Assessment report", "Certification letters"]
                },
                {
                    "step_number": 4,
                    "title": "External Auditor Coordination",
                    "description": "Coordinate with external auditors for SOX compliance review",
                    "category": "coordination",
                    "complexity": "medium",
                    "base_hours": 16,
                    "required_skills": ["audit_coordination", "communication"],
                    "deliverables": ["Auditor communications", "Management responses"]
                }
            ],
            "ISO27001": [
                {
                    "step_number": 1,
                    "title": "Information Security Risk Assessment",
                    "description": "Conduct comprehensive information security risk assessment",
                    "category": "assessment",
                    "complexity": "high",
                    "base_hours": 32,
                    "required_skills": ["security_analysis", "risk_assessment"],
                    "deliverables": ["Risk register", "Threat analysis", "Vulnerability assessment"]
                },
                {
                    "step_number": 2,
                    "title": "Security Controls Implementation",
                    "description": "Implement required security controls based on risk assessment",
                    "category": "implementation",
                    "complexity": "high",
                    "base_hours": 80,
                    "required_skills": ["security_implementation", "system_configuration"],
                    "deliverables": ["Control implementation plan", "Configuration docs", "Test results"]
                },
                {
                    "step_number": 3,
                    "title": "Security Awareness Training",
                    "description": "Conduct security awareness training for all employees",
                    "category": "training",
                    "complexity": "medium",
                    "base_hours": 24,
                    "required_skills": ["training_design", "security_awareness"],
                    "deliverables": ["Training materials", "Attendance records", "Assessment results"]
                },
                {
                    "step_number": 4,
                    "title": "Incident Response Plan",
                    "description": "Develop and test incident response procedures",
                    "category": "planning",
                    "complexity": "medium",
                    "base_hours": 16,
                    "required_skills": ["incident_response", "crisis_management"],
                    "deliverables": ["Response plan", "Contact lists", "Test scenarios"]
                }
            ]
        }
        
        logger.info("Step Generator Agent initialized", 
                   agent_name=self.name,
                   templates_count=len(self.step_templates))
    
    async def generate_steps(self, compliance_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate steps for a compliance requirement"""
        try:
            framework = compliance_data.get("framework")
            company_id = compliance_data.get("company_id")
            company_size = compliance_data.get("company_size", "medium")
            complexity_factor = compliance_data.get("complexity_factor", 1.0)
            
            logger.info("Generating compliance steps", 
                       framework=framework,
                       company_id=company_id,
                       company_size=company_size)
            
            if framework not in self.step_templates:
                logger.warning("No template found for framework", framework=framework)
                return []
            
            template_steps = self.step_templates[framework]
            generated_steps = []
            
            for template in template_steps:
                step = template.copy()
                
                # Adjust effort based on company size
                size_multiplier = {
                    "small": 0.7,
                    "medium": 1.0,
                    "large": 1.3,
                    "enterprise": 1.6
                }.get(company_size, 1.0)
                
                # Adjust effort based on complexity
                complexity_multiplier = {
                    "low": 0.8,
                    "medium": 1.0,
                    "high": 1.4
                }.get(template["complexity"], 1.0)
                
                # Calculate final effort
                base_hours = template["base_hours"]
                adjusted_hours = int(base_hours * size_multiplier * complexity_multiplier * complexity_factor)
                
                step.update({
                    "estimated_duration_hours": adjusted_hours,
                    "company_size_factor": size_multiplier,
                    "complexity_factor": complexity_multiplier,
                    "framework": framework,
                    "company_id": company_id
                })
                
                generated_steps.append(step)
            
            logger.info("Steps generated", 
                       framework=framework,
                       steps_count=len(generated_steps),
                       total_hours=sum(s["estimated_duration_hours"] for s in generated_steps))
            
            return generated_steps
            
        except Exception as e:
            logger.error("Failed to generate steps", 
                        framework=compliance_data.get("framework"), 
                        error=str(e))
            raise
    
    async def assign_resources(self, steps: List[Dict[str, Any]], company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assign resources and roles to steps"""
        try:
            company_id = company_data.get("company_id")
            
            logger.info("Assigning resources to steps", 
                       company_id=company_id,
                       steps_count=len(steps))
            
            # Mock role assignments based on required skills
            skill_to_role_mapping = {
                "data_analysis": "Data Analyst",
                "process_mapping": "Business Analyst",
                "legal_analysis": "Legal Counsel",
                "risk_assessment": "Risk Manager",
                "legal_writing": "Legal Counsel",
                "ux_design": "UX Designer",
                "process_design": "Business Analyst",
                "system_integration": "IT Architect",
                "financial_analysis": "Financial Analyst",
                "process_documentation": "Business Analyst",
                "audit_testing": "Internal Auditor",
                "financial_controls": "Finance Manager",
                "management_review": "Senior Management",
                "financial_reporting": "Finance Manager",
                "audit_coordination": "Audit Manager",
                "communication": "Project Manager",
                "security_analysis": "Security Analyst",
                "security_implementation": "Security Engineer",
                "system_configuration": "System Administrator",
                "training_design": "Training Specialist",
                "security_awareness": "Security Officer",
                "incident_response": "Security Manager",
                "crisis_management": "Operations Manager"
            }
            
            # Mock team assignments
            team_assignments = {
                "Data Analyst": "data.analyst@company.com",
                "Business Analyst": "business.analyst@company.com",
                "Legal Counsel": "legal@company.com",
                "Risk Manager": "risk.manager@company.com",
                "UX Designer": "ux.designer@company.com",
                "IT Architect": "it.architect@company.com",
                "Financial Analyst": "financial.analyst@company.com",
                "Internal Auditor": "internal.auditor@company.com",
                "Finance Manager": "finance.manager@company.com",
                "Senior Management": "management@company.com",
                "Audit Manager": "audit.manager@company.com",
                "Project Manager": "project.manager@company.com",
                "Security Analyst": "security.analyst@company.com",
                "Security Engineer": "security.engineer@company.com",
                "System Administrator": "sysadmin@company.com",
                "Training Specialist": "training@company.com",
                "Security Officer": "security.officer@company.com",
                "Security Manager": "security.manager@company.com",
                "Operations Manager": "operations.manager@company.com"
            }
            
            assigned_steps = []
            
            for step in steps:
                required_skills = step.get("required_skills", [])
                
                # Determine primary responsible role
                primary_role = "Project Manager"  # Default
                if required_skills:
                    primary_skill = required_skills[0]
                    primary_role = skill_to_role_mapping.get(primary_skill, "Project Manager")
                
                # Assign team members
                assigned_to = team_assignments.get(primary_role, "team@company.com")
                
                # Determine supporting roles
                supporting_roles = []
                for skill in required_skills[1:]:  # Skip first skill (primary)
                    role = skill_to_role_mapping.get(skill)
                    if role and role != primary_role:
                        supporting_roles.append(role)
                
                step.update({
                    "responsible_role": primary_role,
                    "assigned_to": assigned_to,
                    "supporting_roles": supporting_roles,
                    "team_size": 1 + len(supporting_roles),
                    "resource_allocation": {
                        "primary": primary_role,
                        "supporting": supporting_roles,
                        "estimated_fte": round((step["estimated_duration_hours"] / 40) / 4, 2)  # Assuming 40 hours/week, 4 weeks
                    }
                })
                
                assigned_steps.append(step)
                
                logger.info("Assigned step resources",
                           step_number=step["step_number"],
                           title=step["title"],
                           primary_role=primary_role,
                           supporting_roles_count=len(supporting_roles))
            
            logger.info("Resource assignment completed", 
                       company_id=company_id,
                       steps_assigned=len(assigned_steps))
            
            return assigned_steps
            
        except Exception as e:
            logger.error("Failed to assign resources", 
                        company_id=company_data.get("company_id"), 
                        error=str(e))
            raise
    
    async def create_timeline(self, steps: List[Dict[str, Any]], timeline_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create execution timeline for steps"""
        try:
            overall_due_date = timeline_data.get("due_date")
            buffer_percentage = timeline_data.get("buffer_percentage", 20)
            parallel_execution = timeline_data.get("allow_parallel", True)
            
            logger.info("Creating step timeline", 
                       steps_count=len(steps),
                       due_date=overall_due_date,
                       parallel_allowed=parallel_execution)
            
            # Parse due date and ensure timezone awareness
            if overall_due_date:
                if isinstance(overall_due_date, str):
                    # Handle ISO format with Z suffix
                    if overall_due_date.endswith('Z'):
                        overall_due_date = overall_due_date[:-1] + '+00:00'
                    due_date = datetime.fromisoformat(overall_due_date)
                    # Ensure timezone awareness
                    if due_date.tzinfo is None:
                        due_date = due_date.replace(tzinfo=timezone.utc)
                else:
                    due_date = overall_due_date
                    if due_date.tzinfo is None:
                        due_date = due_date.replace(tzinfo=timezone.utc)
            else:
                due_date = datetime.now(timezone.utc) + timedelta(days=90)
            
            # Sort steps by dependencies and complexity
            sorted_steps = sorted(steps, key=lambda x: (
                x.get("step_number", 999),
                {"high": 0, "medium": 1, "low": 2}.get(x.get("complexity", "medium"), 1)
            ))
            
            # Calculate timeline
            timeline_steps = []
            current_date = datetime.now(timezone.utc)
            
            for i, step in enumerate(sorted_steps):
                # Calculate step duration
                estimated_hours = step.get("estimated_duration_hours", 8)
                estimated_days = max(1, (estimated_hours + 7) // 8)  # Convert to days
                
                # Add buffer
                buffer_days = max(1, int(estimated_days * buffer_percentage / 100))
                total_days = estimated_days + buffer_days
                
                # Determine start date
                if i == 0:
                    start_date = current_date
                else:
                    # Check if can run in parallel
                    if parallel_execution and step.get("category") != "assessment":
                        # Can start after first step if not assessment
                        start_date = datetime.fromisoformat(timeline_steps[0]["end_date"]) + timedelta(days=1)
                    else:
                        # Sequential execution
                        start_date = datetime.fromisoformat(timeline_steps[i-1]["end_date"]) + timedelta(days=1)
                
                end_date = start_date + timedelta(days=total_days)
                
                # Check if exceeds overall due date
                if end_date > due_date:
                    logger.warning("Step timeline exceeds due date", 
                                 step_number=step["step_number"],
                                 step_end=end_date.strftime("%Y-%m-%d"),
                                 overall_due=due_date.strftime("%Y-%m-%d"))
                
                step.update({
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "estimated_days": estimated_days,
                    "buffer_days": buffer_days,
                    "total_allocated_days": total_days,
                    "timeline_risk": "high" if end_date > due_date else "medium" if (due_date - end_date).days < 7 else "low"
                })
                
                timeline_steps.append(step)
                
                logger.info("Step timeline created",
                           step_number=step["step_number"],
                           start_date=start_date.strftime("%Y-%m-%d"),
                           end_date=end_date.strftime("%Y-%m-%d"),
                           total_days=total_days)
            
            # Calculate overall timeline metrics
            if timeline_steps:
                project_start = min(datetime.fromisoformat(s["start_date"]) for s in timeline_steps)
                project_end = max(datetime.fromisoformat(s["end_date"]) for s in timeline_steps)
                project_duration = (project_end - project_start).days
                
                logger.info("Timeline creation completed", 
                           project_start=project_start.strftime("%Y-%m-%d"),
                           project_end=project_end.strftime("%Y-%m-%d"),
                           project_duration_days=project_duration)
            
            return timeline_steps
            
        except Exception as e:
            logger.error("Failed to create timeline", error=str(e))
            raise
    
    async def process_compliance_requirement(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete step generation process for a compliance requirement"""
        try:
            company_compliance_id = input_data.get("company_compliance_id")
            framework = input_data.get("framework")
            company_data = input_data.get("company_data", {})
            
            logger.info("Processing compliance requirement for step generation", 
                       company_compliance_id=company_compliance_id,
                       framework=framework)
            
            # Step 1: Generate steps from template
            compliance_data = {
                "framework": framework,
                "company_id": company_data.get("company_id"),
                "company_size": company_data.get("size", "medium"),
                "complexity_factor": input_data.get("complexity_factor", 1.0)
            }
            
            generated_steps = await self.generate_steps(compliance_data)
            
            if not generated_steps:
                return {
                    "success": False,
                    "message": f"No step template found for framework: {framework}",
                    "company_compliance_id": company_compliance_id
                }
            
            # Step 2: Assign resources
            assigned_steps = await self.assign_resources(generated_steps, company_data)
            
            # Step 3: Create timeline
            timeline_data = {
                "due_date": input_data.get("due_date"),
                "buffer_percentage": input_data.get("buffer_percentage", 20),
                "allow_parallel": input_data.get("allow_parallel", True)
            }
            
            final_steps = await self.create_timeline(assigned_steps, timeline_data)
            
            # Generate summary
            total_hours = sum(step["estimated_duration_hours"] for step in final_steps)
            total_days = sum(step["total_allocated_days"] for step in final_steps)
            
            result = {
                "success": True,
                "company_compliance_id": company_compliance_id,
                "framework": framework,
                "agent": self.name,
                "generated_steps": final_steps,
                "summary": {
                    "total_steps": len(final_steps),
                    "total_estimated_hours": total_hours,
                    "total_allocated_days": total_days,
                    "unique_roles_required": len(set(step["responsible_role"] for step in final_steps)),
                    "complexity_distribution": {
                        "high": len([s for s in final_steps if s["complexity"] == "high"]),
                        "medium": len([s for s in final_steps if s["complexity"] == "medium"]),
                        "low": len([s for s in final_steps if s["complexity"] == "low"])
                    },
                    "category_distribution": {
                        category: len([s for s in final_steps if s["category"] == category])
                        for category in set(step["category"] for step in final_steps)
                    }
                },
                "recommendations": [
                    "Review resource assignments and adjust based on team availability",
                    "Consider parallel execution where possible to optimize timeline",
                    "Establish regular checkpoint meetings to monitor progress",
                    "Prepare necessary tools and templates before step execution"
                ]
            }
            
            logger.info("Compliance requirement processing completed", 
                       company_compliance_id=company_compliance_id,
                       steps_generated=len(final_steps),
                       total_hours=total_hours)
            
            return result
            
        except Exception as e:
            logger.error("Failed to process compliance requirement", 
                        company_compliance_id=input_data.get("company_compliance_id"), 
                        error=str(e))
            
            return {
                "success": False,
                "company_compliance_id": input_data.get("company_compliance_id"),
                "agent": self.name,
                "error": str(e),
                "message": "Step generation failed"
            }


# Global agent instance
step_generator_agent = StepGeneratorAgent()
