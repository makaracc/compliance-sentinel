#!/usr/bin/env python3
"""
Test script for Admin Agent microservice
"""

import asyncio
import httpx
import json
from datetime import date, datetime


class AdminAgentTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def test_health_endpoints(self):
        """Test health check endpoints"""
        print("🔍 Testing Health Endpoints...")
        
        try:
            # Basic health check
            response = await self.client.get(f"{self.base_url}/health/")
            print(f"✅ Basic Health: {response.status_code} - {response.json()}")
            
            # Liveness check
            response = await self.client.get(f"{self.base_url}/health/live")
            print(f"✅ Liveness: {response.status_code} - {response.json()}")
            
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    async def test_root_endpoint(self):
        """Test root endpoint"""
        print("\n🔍 Testing Root Endpoint...")
        
        try:
            response = await self.client.get(f"{self.base_url}/")
            print(f"✅ Root: {response.status_code}")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
            
        except Exception as e:
            print(f"❌ Root endpoint failed: {e}")
    
    async def test_swagger_docs(self):
        """Test Swagger documentation"""
        print("\n🔍 Testing Swagger Documentation...")
        
        try:
            # OpenAPI schema
            response = await self.client.get(f"{self.base_url}/openapi.json")
            print(f"✅ OpenAPI Schema: {response.status_code}")
            
            # Swagger UI (this will return HTML)
            response = await self.client.get(f"{self.base_url}/docs")
            print(f"✅ Swagger UI: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Swagger docs failed: {e}")
    
    async def test_companies_endpoints(self):
        """Test companies endpoints"""
        print("\n🔍 Testing Companies Endpoints...")
        
        try:
            # List companies (should work even with empty database)
            response = await self.client.get(f"{self.base_url}/api/companies/")
            print(f"✅ List Companies: {response.status_code}")
            
            # Test company creation (will fail without database, but endpoint should exist)
            company_data = {
                "name": "Test Company",
                "industry": "technology",
                "location": "Australia",
                "contact_email": "test@company.com"
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/companies/",
                json=company_data
            )
            print(f"📝 Create Company: {response.status_code}")
            if response.status_code != 500:  # Expected to fail without DB
                print(f"   Response: {response.json()}")
            
        except Exception as e:
            print(f"❌ Companies endpoints failed: {e}")
    
    async def test_tasks_endpoints(self):
        """Test tasks endpoints"""
        print("\n🔍 Testing Tasks Endpoints...")
        
        try:
            # List tasks (should work with in-memory storage)
            response = await self.client.get(f"{self.base_url}/api/tasks/")
            print(f"✅ List Tasks: {response.status_code} - {response.json()}")
            
            # Create a test task
            task_data = {
                "title": "Test Task",
                "description": "This is a test task",
                "priority": "High",
                "assigned_to": "Test User",
                "due_date": str(date.today()),
                "status": "Pending"
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/tasks/",
                json=task_data
            )
            print(f"✅ Create Task: {response.status_code}")
            if response.status_code == 201:
                task = response.json()
                print(f"   Created Task ID: {task['id']}")
                
                # Test getting the created task
                response = await self.client.get(f"{self.base_url}/api/tasks/{task['id']}")
                print(f"✅ Get Task: {response.status_code}")
                
                # Test updating the task
                update_data = {"status": "In Progress"}
                response = await self.client.put(
                    f"{self.base_url}/api/tasks/{task['id']}",
                    json=update_data
                )
                print(f"✅ Update Task: {response.status_code}")
                
                # Test completing the task
                response = await self.client.post(
                    f"{self.base_url}/api/tasks/{task['id']}/complete?completed_by=Test User"
                )
                print(f"✅ Complete Task: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Tasks endpoints failed: {e}")
    
    async def test_compliance_endpoints(self):
        """Test compliance endpoints"""
        print("\n🔍 Testing Compliance Endpoints...")
        
        try:
            # List compliance requirements (will fail without database)
            response = await self.client.get(f"{self.base_url}/api/compliance/requirements")
            print(f"📝 List Compliance Requirements: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Compliance endpoints failed: {e}")
    
    async def test_workflow_endpoints(self):
        """Test workflow endpoints"""
        print("\n🔍 Testing Workflow Endpoints...")
        
        try:
            # Test workflow start (will fail without Dapr)
            workflow_data = {
                "workflow_name": "test_workflow",
                "input_data": {"test": "data"}
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/workflows/start",
                json=workflow_data
            )
            print(f"📝 Start Workflow: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Workflow endpoints failed: {e}")
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Admin Agent Service Tests")
        print("=" * 50)
        
        await self.test_health_endpoints()
        await self.test_root_endpoint()
        await self.test_swagger_docs()
        await self.test_companies_endpoints()
        await self.test_tasks_endpoints()
        await self.test_compliance_endpoints()
        await self.test_workflow_endpoints()
        
        print("\n" + "=" * 50)
        print("🏁 Tests completed!")
        print("\n📖 Access Swagger Documentation at: http://localhost:8000/docs")
        print("📊 Access ReDoc Documentation at: http://localhost:8000/redoc")
        
        await self.client.aclose()


async def main():
    """Main test function"""
    tester = AdminAgentTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
