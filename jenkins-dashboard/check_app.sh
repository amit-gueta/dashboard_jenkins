#!/bin/bash

echo "Attempting to build and start services using Docker Compose..."
# Changed exit 1 to a message and return for non-interactive script
docker-compose up --build -d
if [ $? -ne 0 ]; then
    echo "ERROR: docker-compose up failed. Please check the logs."
    # exit 1 # Replaced with return for agent compatibility
    return 1
fi

echo ""
echo "Services should be starting up. Waiting for 20 seconds..."
sleep 20 # Wait for services to initialize, especially the database and backend

echo ""
echo "Performing health checks..."

# Check backend health
echo "Checking backend health endpoint (http://localhost:8000/api/v1/health)..."
curl -s http://localhost:8000/api/v1/health | grep "healthy"
if [ $? -ne 0 ]; then
    echo "WARNING: Backend health endpoint did not return 'healthy' or is not accessible."
    echo "Full response:"
    curl http://localhost:8000/api/v1/health
    echo ""
else
    echo "Backend health check: OK"
    echo ""
fi

# Check backend OpenAPI docs
echo "Checking backend OpenAPI docs (http://localhost:8000/api/v1/openapi.json)..."
curl -s http://localhost:8000/api/v1/openapi.json | grep "Jenkins Dashboard Backend" > /dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: Backend OpenAPI JSON does not seem correct or is not accessible."
else
    echo "Backend OpenAPI JSON check: OK"
    echo ""
fi

echo "---------------------------------------------------------------------"
echo "Application Test Script Finished."
echo ""
echo "You should now be able to access:"
echo "- Backend OpenAPI Docs: http://localhost:8000/api/v1/docs"
echo "- Frontend UI: http://localhost:3000"
echo ""
echo "If you encountered warnings, please check the Docker logs for each service:"
echo "  docker-compose logs postgres_db"
echo "  docker-compose logs backend"
echo "  docker-compose logs frontend"
echo ""
echo "To stop the services, run: docker-compose down"
echo "---------------------------------------------------------------------"
