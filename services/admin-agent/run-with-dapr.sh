#!/bin/bash

# Admin Agent - Run with Dapr
echo "🚀 Starting Admin Agent with Dapr..."

# Set environment variables
export DAPR_HTTP_PORT=3500
export DAPR_GRPC_PORT=50001
export DATABASE_URL="postgresql+asyncpg://username:password@host:5432/compliance_sentinel"
export DEBUG=true

# Create components directory if it doesn't exist
mkdir -p components

# Start the application with Dapr
dapr run \
  --app-id admin-agent \
  --app-port 8000 \
  --dapr-http-port 3500 \
  --dapr-grpc-port 50001 \
  --components-path ./components \
  --config ./dapr.yaml \
  --log-level info \
  --enable-profiling \
  --enable-metrics \
  --metrics-port 9090 \
  -- python src/main.py

echo "✅ Admin Agent with Dapr stopped"
