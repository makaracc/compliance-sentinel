"""
Compliance Matcher Agent
Matches companies to applicable compliance requirements based on industry and location
"""

from typing import Dict, Any, List
import structlog

logger = structlog.get_logger(__name__)


class ComplianceMatcherAgent:
    """Agent for matching companies to compliance requirements"""
    
    def __init__(self):
        self.name = "compliance_matcher_agent"
        self.version = "1.0.0"
        self.capabilities = [
            "industry_analysis",
            "location_mapping", 
            "requirement_matching",
            "risk_assessment"
        ]
        
        # Industry to compliance framework mapping
        self.industry_compliance_map = {
            "technology": ["GDPR", "ISO27001", "SOC2"],
            "finance": ["GDPR", "SOX", "ISO27001", "PCI-DSS", "Basel III"],
            "healthcare": ["GDPR", "HIPAA", "ISO27001", "FDA"],
            "retail": ["GDPR", "PCI-DSS", "ISO27001"],
            "manufacturing": ["ISO27001", "ISO9001", "OSHA"],
            "education": ["GDPR", "FERPA", "ISO27001"],
            "government": ["FISMA", "ISO27001", "NIST"]
        }
        
        # Location to regulatory framework mapping
        self.location_compliance_map = {
            "australia": ["Privacy Act", "ACSC", "APRA"],
            "eu": ["GDPR", "NIS2", "DORA"],
            "us": ["SOX", "HIPAA", "CCPA", "NIST"],
            "uk": ["UK GDPR", "Data Protection Act", "FCA"],
            "canada": ["PIPEDA", "CPPA"],
            "singapore": ["PDPA", "MAS"]
        }
        
        logger.info("Compliance Matcher Agent initialized", 
                   agent_name=self.name,
                   capabilities=len(self.capabilities))
    
    async def analyze_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze company to determine compliance requirements"""
        try:
            company_id = company_data.get("company_id")
            industry = company_data.get("industry", "").lower()
            location = company_data.get("location", "").lower()
            
            logger.info("Analyzing company for compliance matching", 
                       company_id=company_id,
                       industry=industry,
                       location=location)
            
            analysis_result = {
                "company_id": company_id,
                "industry": industry,
                "location": location,
                "applicable_frameworks": [],
                "risk_level": "medium",
                "mandatory_requirements": [],
                "recommended_requirements": [],
                "analysis_confidence": 0.0
            }
            
            # Industry-based requirements
            industry_frameworks = []
            for ind_key, frameworks in self.industry_compliance_map.items():
                if ind_key in industry:
                    industry_frameworks.extend(frameworks)
                    break
            
            # Location-based requirements
            location_frameworks = []
            for loc_key, frameworks in self.location_compliance_map.items():
                if loc_key in location:
                    location_frameworks.extend(frameworks)
                    break
            
            # Combine and deduplicate
            all_frameworks = list(set(industry_frameworks + location_frameworks))
            analysis_result["applicable_frameworks"] = all_frameworks
            
            # Determine mandatory vs recommended
            mandatory_frameworks = ["GDPR", "SOX", "HIPAA", "PCI-DSS"]
            for framework in all_frameworks:
                if framework in mandatory_frameworks:
                    analysis_result["mandatory_requirements"].append(framework)
                else:
                    analysis_result["recommended_requirements"].append(framework)
            
            # Calculate risk level
            risk_score = 0
            if "finance" in industry:
                risk_score += 3
            if "healthcare" in industry:
                risk_score += 3
            if "technology" in industry:
                risk_score += 2
            if len(analysis_result["mandatory_requirements"]) > 2:
                risk_score += 2
            
            if risk_score >= 5:
                analysis_result["risk_level"] = "critical"
            elif risk_score >= 3:
                analysis_result["risk_level"] = "high"
            elif risk_score >= 1:
                analysis_result["risk_level"] = "medium"
            else:
                analysis_result["risk_level"] = "low"
            
            # Calculate confidence based on data completeness
            confidence = 0.5  # Base confidence
            if industry:
                confidence += 0.3
            if location:
                confidence += 0.2
            
            analysis_result["analysis_confidence"] = round(confidence, 2)
            
            logger.info("Company analysis completed", 
                       company_id=company_id,
                       frameworks_count=len(all_frameworks),
                       risk_level=analysis_result["risk_level"],
                       confidence=analysis_result["analysis_confidence"])
            
            return analysis_result
            
        except Exception as e:
            logger.error("Failed to analyze company", 
                        company_id=company_data.get("company_id"), 
                        error=str(e))
            raise
    
    async def match_requirements(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Match analysis result to specific compliance requirements"""
        try:
            company_id = analysis_result.get("company_id")
            applicable_frameworks = analysis_result.get("applicable_frameworks", [])
            
            logger.info("Matching compliance requirements", 
                       company_id=company_id,
                       frameworks=applicable_frameworks)
            
            # Mock requirement matching
            # In real implementation, this would query compliance_requirements table
            requirement_templates = {
                "GDPR": {
                    "id": 1,
                    "name": "Data Protection Assessment",
                    "framework": "GDPR",
                    "severity_level": "High",
                    "mandatory": True,
                    "estimated_duration_days": 60
                },
                "SOX": {
                    "id": 2,
                    "name": "Financial Controls Review",
                    "framework": "SOX",
                    "severity_level": "Critical",
                    "mandatory": True,
                    "estimated_duration_days": 90
                },
                "ISO27001": {
                    "id": 3,
                    "name": "Security Audit",
                    "framework": "ISO27001",
                    "severity_level": "High",
                    "mandatory": False,
                    "estimated_duration_days": 75
                },
                "HIPAA": {
                    "id": 4,
                    "name": "Healthcare Privacy Assessment",
                    "framework": "HIPAA",
                    "severity_level": "Critical",
                    "mandatory": True,
                    "estimated_duration_days": 45
                },
                "PCI-DSS": {
                    "id": 5,
                    "name": "Payment Card Security Assessment",
                    "framework": "PCI-DSS",
                    "severity_level": "High",
                    "mandatory": True,
                    "estimated_duration_days": 30
                }
            }
            
            matched_requirements = []
            
            for framework in applicable_frameworks:
                if framework in requirement_templates:
                    requirement = requirement_templates[framework].copy()
                    
                    # Adjust based on company risk level
                    risk_level = analysis_result.get("risk_level", "medium")
                    if risk_level == "critical":
                        requirement["priority_boost"] = 2
                        requirement["estimated_duration_days"] = int(requirement["estimated_duration_days"] * 0.8)
                    elif risk_level == "high":
                        requirement["priority_boost"] = 1
                        requirement["estimated_duration_days"] = int(requirement["estimated_duration_days"] * 0.9)
                    
                    matched_requirements.append(requirement)
            
            logger.info("Requirements matched", 
                       company_id=company_id,
                       matched_count=len(matched_requirements))
            
            return matched_requirements
            
        except Exception as e:
            logger.error("Failed to match requirements", 
                        company_id=analysis_result.get("company_id"), 
                        error=str(e))
            raise
    
    async def assess_risk(self, company_data: Dict[str, Any], requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess compliance risk for the company"""
        try:
            company_id = company_data.get("company_id")
            
            logger.info("Assessing compliance risk", 
                       company_id=company_id,
                       requirements_count=len(requirements))
            
            risk_assessment = {
                "company_id": company_id,
                "overall_risk_score": 0,
                "risk_level": "low",
                "risk_factors": [],
                "mitigation_recommendations": [],
                "priority_requirements": [],
                "estimated_total_effort_days": 0
            }
            
            # Calculate risk score
            risk_score = 0
            total_effort = 0
            
            for requirement in requirements:
                # Add risk based on severity
                severity = requirement.get("severity_level", "Medium")
                if severity == "Critical":
                    risk_score += 4
                elif severity == "High":
                    risk_score += 3
                elif severity == "Medium":
                    risk_score += 2
                else:
                    risk_score += 1
                
                # Add to total effort
                total_effort += requirement.get("estimated_duration_days", 30)
                
                # Track priority requirements
                if requirement.get("mandatory", False) and severity in ["Critical", "High"]:
                    risk_assessment["priority_requirements"].append({
                        "name": requirement.get("name"),
                        "framework": requirement.get("framework"),
                        "severity": severity,
                        "estimated_days": requirement.get("estimated_duration_days", 30)
                    })
            
            risk_assessment["overall_risk_score"] = risk_score
            risk_assessment["estimated_total_effort_days"] = total_effort
            
            # Determine risk level
            if risk_score >= 12:
                risk_assessment["risk_level"] = "critical"
            elif risk_score >= 8:
                risk_assessment["risk_level"] = "high"
            elif risk_score >= 4:
                risk_assessment["risk_level"] = "medium"
            else:
                risk_assessment["risk_level"] = "low"
            
            # Identify risk factors
            if len(requirements) > 3:
                risk_assessment["risk_factors"].append("Multiple compliance requirements")
            
            if total_effort > 180:  # More than 6 months
                risk_assessment["risk_factors"].append("High implementation effort required")
            
            critical_requirements = [r for r in requirements if r.get("severity_level") == "Critical"]
            if len(critical_requirements) > 1:
                risk_assessment["risk_factors"].append("Multiple critical compliance requirements")
            
            # Generate mitigation recommendations
            if risk_assessment["risk_level"] in ["critical", "high"]:
                risk_assessment["mitigation_recommendations"].extend([
                    "Establish dedicated compliance team",
                    "Implement phased compliance approach",
                    "Consider external compliance consultants",
                    "Prioritize critical requirements first"
                ])
            
            if total_effort > 120:
                risk_assessment["mitigation_recommendations"].append(
                    "Allocate additional resources for compliance implementation"
                )
            
            logger.info("Risk assessment completed", 
                       company_id=company_id,
                       risk_level=risk_assessment["risk_level"],
                       risk_score=risk_score,
                       total_effort_days=total_effort)
            
            return risk_assessment
            
        except Exception as e:
            logger.error("Failed to assess risk", 
                        company_id=company_data.get("company_id"), 
                        error=str(e))
            raise
    
    async def process_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete company processing pipeline"""
        try:
            company_id = company_data.get("company_id")
            
            logger.info("Processing company through compliance matcher", 
                       company_id=company_id)
            
            # Step 1: Analyze company
            analysis_result = await self.analyze_company(company_data)
            
            # Step 2: Match requirements
            matched_requirements = await self.match_requirements(analysis_result)
            
            # Step 3: Assess risk
            risk_assessment = await self.assess_risk(company_data, matched_requirements)
            
            # Combine results
            result = {
                "success": True,
                "company_id": company_id,
                "agent": self.name,
                "analysis": analysis_result,
                "matched_requirements": matched_requirements,
                "risk_assessment": risk_assessment,
                "summary": {
                    "total_requirements": len(matched_requirements),
                    "mandatory_requirements": len([r for r in matched_requirements if r.get("mandatory", False)]),
                    "risk_level": risk_assessment.get("risk_level"),
                    "estimated_effort_days": risk_assessment.get("estimated_total_effort_days"),
                    "priority_requirements_count": len(risk_assessment.get("priority_requirements", []))
                },
                "recommendations": {
                    "immediate_actions": [
                        "Review and approve compliance implementation plan",
                        "Allocate necessary resources for compliance activities",
                        "Establish compliance project timeline"
                    ],
                    "next_steps": [
                        "Begin with highest priority requirements",
                        "Set up regular compliance review meetings",
                        "Implement compliance tracking system"
                    ]
                }
            }
            
            logger.info("Company processing completed", 
                       company_id=company_id,
                       requirements_matched=len(matched_requirements),
                       risk_level=risk_assessment.get("risk_level"))
            
            return result
            
        except Exception as e:
            logger.error("Failed to process company", 
                        company_id=company_data.get("company_id"), 
                        error=str(e))
            
            return {
                "success": False,
                "company_id": company_data.get("company_id"),
                "agent": self.name,
                "error": str(e),
                "message": "Company processing failed"
            }


# Global agent instance
compliance_matcher_agent = ComplianceMatcherAgent()
