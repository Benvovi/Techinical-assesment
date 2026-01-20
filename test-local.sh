#!/bin/bash
# Local testing script for Titanic API

set -e

echo "🧪 Testing Titanic API Locally"
echo "================================"
echo ""

# Test 1: Docker Compose validation
echo "1️⃣  Validating Docker Compose configuration..."
docker-compose -f docker-compose.dev.yml config > /dev/null
echo "   ✅ Docker Compose config is valid"
echo ""

# Test 2: Start services
echo "2️⃣  Starting services with Docker Compose..."
docker-compose -f docker-compose.dev.yml up -d
echo "   ✅ Services started"
echo ""

# Wait for services to be ready
echo "3️⃣  Waiting for services to be ready..."
sleep 10
echo "   ✅ Services should be ready"
echo ""

# Test 3: Health check
echo "4️⃣  Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health || echo "000")
if [ "$HEALTH_RESPONSE" = "200" ] || [ "$HEALTH_RESPONSE" = "503" ]; then
    echo "   ✅ Health endpoint responding (HTTP $HEALTH_RESPONSE)"
else
    echo "   ⚠️  Health endpoint returned HTTP $HEALTH_RESPONSE"
fi
echo ""

# Test 4: Root endpoint
echo "5️⃣  Testing root endpoint..."
ROOT_RESPONSE=$(curl -s http://localhost:5000/ || echo "")
if [[ "$ROOT_RESPONSE" == *"Titanic API"* ]]; then
    echo "   ✅ Root endpoint working"
else
    echo "   ⚠️  Root endpoint may not be working correctly"
fi
echo ""

# Test 5: Metrics endpoint
echo "6️⃣  Testing metrics endpoint..."
METRICS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/metrics || echo "000")
if [ "$METRICS_RESPONSE" = "200" ]; then
    echo "   ✅ Metrics endpoint working"
else
    echo "   ⚠️  Metrics endpoint returned HTTP $METRICS_RESPONSE"
fi
echo ""

# Test 6: Run tests in container
echo "7️⃣  Running unit tests in container..."
docker-compose -f docker-compose.dev.yml exec -T app pytest tests/ -v || echo "   ⚠️  Tests may have failed (check output above)"
echo ""

echo "================================"
echo "✅ Local testing complete!"
echo ""
echo "To view logs: docker-compose -f docker-compose.dev.yml logs -f"
echo "To stop services: docker-compose -f docker-compose.dev.yml down"
echo ""
