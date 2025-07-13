#!/usr/bin/env python3
"""
Test script for Dapr workflows and agents
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from agents.compliance_matcher import compliance_matcher_agent
from agents.step_generator import step_generator_agent
from agents.progress_monitor import progress_monitor_agent
from agents.evidence_validator import evidence_validator_agent
from agents.notification import notification_agent


class WorkflowAgentTester:
    """Test workflows and agents functionality"""
    
    def __init__(self):
        self.test_company_data = {
            "company_id": 1,
            "company_name": "TechCorp Australia",
            "industry": "technology",
            "location": "australia",
            "size": "medium"
        }
    
    async def test_compliance_matcher_agent(self):
        """Test compliance matcher agent"""
        print("\n🔍 Testing Compliance Matcher Agent...")
        
        try:
            # Test company analysis
            analysis_result = await compliance_matcher_agent.analyze_company(self.test_company_data)
            print(f"✅ Company Analysis: {analysis_result['risk_level']} risk, {len(analysis_result['applicable_frameworks'])} frameworks")
            
            # Test requirement matching
            requirements = await compliance_matcher_agent.match_requirements(analysis_result)
            print(f"✅ Requirements Matched: {len(requirements)} requirements")
            
            # Test risk assessment
            risk_assessment = await compliance_matcher_agent.assess_risk(self.test_company_data, requirements)
            print(f"✅ Risk Assessment: {risk_assessment['risk_level']} risk, {risk_assessment['estimated_total_effort_days']} days effort")
            
            # Test complete processing
            result = await compliance_matcher_agent.process_company(self.test_company_data)
            print(f"✅ Complete Processing: {result['success']}, {result['summary']['total_requirements']} requirements")
            
            return result
            
        except Exception as e:
            print(f"❌ Compliance Matcher Agent failed: {e}")
            return None
    
    async def test_step_generator_agent(self):
        """Test step generator agent"""
        print("\n🔍 Testing Step Generator Agent...")
        
        try:
            # Test step generation
            compliance_data = {
                "framework": "GDPR",
                "company_id": 1,
                "company_size": "medium",
                "complexity_factor": 1.0
            }
            
            steps = await step_generator_agent.generate_steps(compliance_data)
            print(f"✅ Steps Generated: {len(steps)} steps for GDPR")
            
            # Test resource assignment
            assigned_steps = await step_generator_agent.assign_resources(steps, self.test_company_data)
            print(f"✅ Resources Assigned: {len(assigned_steps)} steps with assignments")
            
            # Test timeline creation
            timeline_data = {
                "due_date": "2024-12-31T23:59:59Z",
                "buffer_percentage": 20,
                "allow_parallel": True
            }
            
            timeline_steps = await step_generator_agent.create_timeline(assigned_steps, timeline_data)
            print(f"✅ Timeline Created: {len(timeline_steps)} steps with timeline")
            
            # Test complete processing
            input_data = {
                "company_compliance_id": "cc_1_1",
                "framework": "GDPR",
                "company_data": self.test_company_data,
                "due_date": "2024-12-31T23:59:59Z"
            }
            
            result = await step_generator_agent.process_compliance_requirement(input_data)
            print(f"✅ Complete Processing: {result['success']}, {result['summary']['total_steps']} steps, {result['summary']['total_estimated_hours']} hours")
            
            return result
            
        except Exception as e:
            print(f"❌ Step Generator Agent failed: {e}")
            return None
    
    async def test_progress_monitor_agent(self):
        """Test progress monitor agent"""
        print("\n🔍 Testing Progress Monitor Agent...")
        
        try:
            # Test company progress monitoring
            progress_data = await progress_monitor_agent.monitor_company_progress(1)
            print(f"✅ Progress Monitoring: {progress_data['overall_completion']}% complete, {len(progress_data['bottlenecks'])} bottlenecks")
            
            return progress_data
            
        except Exception as e:
            print(f"❌ Progress Monitor Agent failed: {e}")
            return None
    
    async def test_evidence_validator_agent(self):
        """Test evidence validator agent"""
        print("\n🔍 Testing Evidence Validator Agent...")
        
        try:
            # Test evidence validation
            evidence_data = {
                "step_id": "ccs_1_1",
                "file_path": "/uploads/evidence/test_document.pdf",
                "required_documentation": "Data flow diagrams, processing records"
            }
            
            validation_result = await evidence_validator_agent.validate_evidence(evidence_data)
            print(f"✅ Evidence Validation: {validation_result['validation_status']}, score: {validation_result['quality_score']}")
            
            return validation_result
            
        except Exception as e:
            print(f"❌ Evidence Validator Agent failed: {e}")
            return None
    
    async def test_notification_agent(self):
        """Test notification agent"""
        print("\n🔍 Testing Notification Agent...")
        
        try:
            # Test notification sending
            notification_data = {
                "type": "step_completed",
                "priority": "high",
                "message": "GDPR Data Inventory step completed",
                "recipient": "compliance@company.com"
            }
            
            result = await notification_agent.send_notification(notification_data)
            print(f"✅ Notification Sent: {result['success']}, {result['channels_used']} channels used")
            
            return result
            
        except Exception as e:
            print(f"❌ Notification Agent failed: {e}")
            return None
    
    async def test_agent_collaboration(self):
        """Test agents working together"""
        print("\n🔍 Testing Agent Collaboration...")
        
        try:
            # Step 1: Compliance Matcher analyzes company
            matcher_result = await compliance_matcher_agent.process_company(self.test_company_data)
            
            if not matcher_result or not matcher_result.get("success"):
                print("❌ Compliance matching failed")
                return
            
            # Step 2: Step Generator creates steps for first requirement
            first_requirement = matcher_result["matched_requirements"][0]
            step_input = {
                "company_compliance_id": f"cc_{self.test_company_data['company_id']}_{first_requirement['id']}",
                "framework": first_requirement["framework"],
                "company_data": self.test_company_data,
                "due_date": "2024-12-31T23:59:59Z"
            }
            
            step_result = await step_generator_agent.process_compliance_requirement(step_input)
            
            if not step_result or not step_result.get("success"):
                print("❌ Step generation failed")
                return
            
            # Step 3: Progress Monitor checks status
            progress_result = await progress_monitor_agent.monitor_company_progress(self.test_company_data["company_id"])
            
            # Step 4: Evidence Validator validates sample evidence
            evidence_data = {
                "step_id": step_result["generated_steps"][0]["id"] if step_result["generated_steps"] else "test_step",
                "file_path": "/uploads/evidence/sample.pdf"
            }
            
            evidence_result = await evidence_validator_agent.validate_evidence(evidence_data)
            
            # Step 5: Notification Agent sends completion notification
            notification_data = {
                "type": "workflow_completed",
                "priority": "medium",
                "message": f"Company {self.test_company_data['company_name']} onboarding workflow completed"
            }
            
            notification_result = await notification_agent.send_notification(notification_data)
            
            print("✅ Agent Collaboration Successful:")
            print(f"   - Matched {len(matcher_result['matched_requirements'])} requirements")
            print(f"   - Generated {step_result['summary']['total_steps']} steps")
            print(f"   - Progress: {progress_result['overall_completion']}% complete")
            print(f"   - Evidence validation: {evidence_result['validation_status']}")
            print(f"   - Notifications sent via {notification_result['channels_used']} channels")
            
            return {
                "compliance_matching": matcher_result,
                "step_generation": step_result,
                "progress_monitoring": progress_result,
                "evidence_validation": evidence_result,
                "notifications": notification_result
            }
            
        except Exception as e:
            print(f"❌ Agent collaboration failed: {e}")
            return None
    
    async def run_all_tests(self):
        """Run all agent tests"""
        print("🚀 Starting Workflow and Agent Tests")
        print("=" * 60)
        
        # Test individual agents
        matcher_result = await self.test_compliance_matcher_agent()
        step_result = await self.test_step_generator_agent()
        progress_result = await self.test_progress_monitor_agent()
        evidence_result = await self.test_evidence_validator_agent()
        notification_result = await self.test_notification_agent()
        
        # Test agent collaboration
        collaboration_result = await self.test_agent_collaboration()
        
        print("\n" + "=" * 60)
        print("🏁 Workflow and Agent Tests Completed!")
        
        # Summary
        successful_tests = sum([
            1 if matcher_result and matcher_result.get("success") else 0,
            1 if step_result and step_result.get("success") else 0,
            1 if progress_result else 0,
            1 if evidence_result else 0,
            1 if notification_result and notification_result.get("success") else 0,
            1 if collaboration_result else 0
        ])
        
        print(f"\n📊 Test Results: {successful_tests}/6 tests passed")
        
        if successful_tests == 6:
            print("🎉 All tests passed! Workflows and agents are ready for deployment.")
        else:
            print("⚠️  Some tests failed. Review the output above for details.")
        
        return {
            "total_tests": 6,
            "passed_tests": successful_tests,
            "success_rate": (successful_tests / 6) * 100,
            "results": {
                "compliance_matcher": matcher_result,
                "step_generator": step_result,
                "progress_monitor": progress_result,
                "evidence_validator": evidence_result,
                "notification": notification_result,
                "collaboration": collaboration_result
            }
        }


async def main():
    """Main test function"""
    tester = WorkflowAgentTester()
    results = await tester.run_all_tests()
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: test_results.json")


if __name__ == "__main__":
    asyncio.run(main())
