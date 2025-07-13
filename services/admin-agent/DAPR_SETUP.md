# Dapr Setup Guide for Admin Agent

## 📋 **Dapr Files Created**

### **Core Configuration:**
- `dapr.yaml` - Main Dapr configuration
- `.env.dapr` - Environment variables for Dapr
- `run-with-dapr.sh` - Development run script

### **Components:**
- `components/statestore.yaml` - PostgreSQL state store
- `components/pubsub.yaml` - Redis pub/sub
- `components/workflow.yaml` - Dapr workflows
- `components/cors.yaml` - CORS middleware
- `components/secrets.yaml` - Secret management
- `components/subscription.yaml` - Pub/sub subscriptions

### **Deployment:**
- `Dockerfile` - Container image
- `docker-compose.yml` - Local development with Docker
- `k8s/deployment.yaml` - Kubernetes deployment
- `k8s/dapr-components.yaml` - Kubernetes Dapr components

## 🚀 **Quick Start**

### **Prerequisites:**
1. **Install Dapr CLI:**
   ```bash
   # Install Dapr CLI
   wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
   
   # Initialize Dapr
   dapr init
   ```

2. **Install Dependencies:**
   ```bash
   # Redis (for pub/sub)
   docker run -d --name redis -p 6379:6379 redis:7-alpine
   
   # Zipkin (for tracing)
   docker run -d --name zipkin -p 9411:9411 openzipkin/zipkin
   ```

### **Run with Dapr (Development):**
```bash
cd /workspaces/compliance-sentinel/services/admin-agent

# Make script executable
chmod +x run-with-dapr.sh

# Run with Dapr
./run-with-dapr.sh
```

### **Run with Docker Compose:**
```bash
# Build and run everything
docker-compose up --build

# Run in background
docker-compose up -d --build
```

## 🔧 **Dapr Components Explained**

### **1. State Store (PostgreSQL)**
```yaml
# components/statestore.yaml
- Stores workflow state and application data
- Uses compliance_sentinel database
- Enables actor state management
```

### **2. Pub/Sub (Redis)**
```yaml
# components/pubsub.yaml
- Handles event messaging between services
- Topics: compliance-events, step-events, task-events
- Enables decoupled communication
```

### **3. Workflows**
```yaml
# components/workflow.yaml
- Enables Dapr workflow orchestration
- Actor-based workflow backend
- Supports our 4 compliance workflows
```

### **4. Secrets Management**
```yaml
# components/secrets.yaml
- Manages sensitive configuration
- Environment-based secret store
- Database credentials and API keys
```

## 📊 **Monitoring & Observability**

### **Metrics:**
- **Endpoint**: http://localhost:9090/metrics
- **Dapr Metrics**: Workflow execution, pub/sub, state operations
- **App Metrics**: API calls, database operations, agent activities

### **Tracing:**
- **Zipkin UI**: http://localhost:9411
- **Distributed Tracing**: End-to-end request tracking
- **Workflow Tracing**: Step-by-step workflow execution

### **Health Checks:**
- **App Health**: http://localhost:8000/health/
- **Dapr Health**: http://localhost:3500/v1.0/healthz
- **Detailed Health**: http://localhost:8000/health/detailed

## 🧪 **Testing with Dapr**

### **1. Test Dapr Connectivity:**
```bash
# Check Dapr status
dapr status

# Test state store
curl -X POST http://localhost:3500/v1.0/state/statestore \
  -H "Content-Type: application/json" \
  -d '[{"key": "test", "value": "hello dapr"}]'

# Test pub/sub
curl -X POST http://localhost:3500/v1.0/publish/pubsub/test-topic \
  -H "Content-Type: application/json" \
  -d '{"message": "hello world"}'
```

### **2. Test Workflows:**
```bash
# Start company onboarding workflow
curl -X POST http://localhost:8000/api/workflows/start \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_name": "company_onboarding_workflow",
    "input_data": {
      "company_id": 1,
      "company_name": "Test Corp",
      "industry": "technology",
      "location": "australia"
    }
  }'
```

### **3. Test Agents:**
```bash
# Test compliance matcher agent
curl -X GET http://localhost:8000/api/companies/1/compliance-overview

# Test step management
curl -X GET http://localhost:8000/api/steps/

# Test task management
curl -X GET http://localhost:8000/api/tasks/
```

## 🐳 **Docker Deployment**

### **Build Image:**
```bash
docker build -t admin-agent:latest .
```

### **Run with Docker Compose:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f admin-agent

# Stop services
docker-compose down
```

## ☸️ **Kubernetes Deployment**

### **Deploy to Kubernetes:**
```bash
# Apply Dapr components
kubectl apply -f k8s/dapr-components.yaml

# Deploy application
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods -l app=admin-agent
kubectl get svc admin-agent-service
```

### **Access Application:**
```bash
# Port forward to access locally
kubectl port-forward svc/admin-agent-service 8000:80

# Access Swagger UI
open http://localhost:8000/docs
```

## 🔍 **Troubleshooting**

### **Common Issues:**

1. **Dapr not initialized:**
   ```bash
   dapr init
   ```

2. **Redis connection failed:**
   ```bash
   docker run -d --name redis -p 6379:6379 redis:7-alpine
   ```

3. **Database connection failed:**
   - Update DATABASE_URL in .env.dapr
   - Ensure compliance_sentinel database exists

4. **Workflow registration failed:**
   - Check workflow imports in src/workflows/registry.py
   - Verify Dapr workflow component is running

### **Debug Commands:**
```bash
# Check Dapr logs
dapr logs --app-id admin-agent

# Check component status
dapr components --kubernetes

# Test Dapr APIs directly
curl http://localhost:3500/v1.0/healthz
```

## 🎯 **Production Considerations**

### **Security:**
- Use proper secret management (Azure Key Vault, AWS Secrets Manager)
- Enable TLS for all Dapr communication
- Configure proper RBAC and network policies

### **Scalability:**
- Configure horizontal pod autoscaling
- Use external state store (managed PostgreSQL)
- Set up Redis cluster for pub/sub

### **Monitoring:**
- Integrate with Prometheus/Grafana
- Set up alerting for workflow failures
- Monitor Dapr sidecar resource usage

## ✅ **Verification Checklist**

- [ ] Dapr CLI installed and initialized
- [ ] Redis running on port 6379
- [ ] PostgreSQL compliance_sentinel database accessible
- [ ] All Dapr components loaded successfully
- [ ] Application starts without errors
- [ ] Swagger UI accessible at /docs
- [ ] Health checks passing
- [ ] Workflows can be started via API
- [ ] Agents responding to requests
- [ ] Metrics available at :9090/metrics
- [ ] Tracing data visible in Zipkin

**The Admin Agent is now fully configured with Dapr and ready for the hackathon!** 🎉
