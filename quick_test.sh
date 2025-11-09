#!/bin/bash

# Quick Test Script for ACEest Fitness Application
# This script runs basic tests to verify everything is working

echo "=========================================="
echo "ACEest Fitness - Quick Test Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASSED${NC}: $2"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}: $2"
        ((FAILED++))
    fi
}

echo "Phase 1: Python Environment"
echo "---------------------------"

# Check Python version
python3 --version > /dev/null 2>&1
print_result $? "Python 3 installed"

# Check virtual environment
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ PASSED${NC}: Virtual environment exists"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC}: Virtual environment not found (run: python -m venv venv)"
fi

# Check requirements
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✓ PASSED${NC}: requirements.txt exists"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}: requirements.txt not found"
    ((FAILED++))
fi

echo ""
echo "Phase 2: Application Files"
echo "---------------------------"

# Check application files
for file in app.py app_v1.1.py app_v1.2.py app_v1.3.py; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ PASSED${NC}: $file exists"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}: $file not found"
        ((FAILED++))
    fi
done

echo ""
echo "Phase 3: Test Files"
echo "-------------------"

# Check test files
for file in tests/test_app.py tests/test_app_v1.1.py tests/test_app_v1.3.py; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ PASSED${NC}: $file exists"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}: $file not found"
        ((FAILED++))
    fi
done

echo ""
echo "Phase 4: Docker Files"
echo "---------------------"

# Check Dockerfiles
for file in Dockerfile Dockerfile.v1.1 Dockerfile.v1.2 Dockerfile.v1.3; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ PASSED${NC}: $file exists"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}: $file not found"
        ((FAILED++))
    fi
done

# Check Docker
docker --version > /dev/null 2>&1
print_result $? "Docker installed"

echo ""
echo "Phase 5: Kubernetes Files"
echo "------------------------"

# Check Kubernetes files
K8S_FILES=("k8s/namespace.yaml" "k8s/configmap.yaml" "k8s/secret.yaml" 
           "k8s/rolling-update-deployment.yaml" "k8s/blue-green-deployment.yaml"
           "k8s/canary-deployment.yaml" "k8s/shadow-deployment.yaml" 
           "k8s/ab-testing-deployment.yaml")

for file in "${K8S_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ PASSED${NC}: $file exists"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}: $file not found"
        ((FAILED++))
    fi
done

# Check kubectl
kubectl version --client > /dev/null 2>&1
print_result $? "kubectl installed"

echo ""
echo "Phase 6: CI/CD Files"
echo "-------------------"

# Check CI/CD files
if [ -f "Jenkinsfile" ]; then
    echo -e "${GREEN}✓ PASSED${NC}: Jenkinsfile exists"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}: Jenkinsfile not found"
    ((FAILED++))
fi

if [ -f "sonar-project.properties" ]; then
    echo -e "${GREEN}✓ PASSED${NC}: sonar-project.properties exists"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}: sonar-project.properties not found"
    ((FAILED++))
fi

echo ""
echo "Phase 7: Documentation"
echo "---------------------"

# Check documentation
DOC_FILES=("README.md" "ASSIGNMENT_REPORT.md" "DEPLOYMENT_GUIDE.md" "TESTING_GUIDE.md")

for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ PASSED${NC}: $file exists"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}: $file not found"
        ((FAILED++))
    fi
done

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All file checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run: pytest --cov=. --cov-report=html"
    echo "2. Build Docker images"
    echo "3. Test Jenkins pipeline"
    echo "4. Deploy to Kubernetes"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please fix the issues above.${NC}"
    exit 1
fi

