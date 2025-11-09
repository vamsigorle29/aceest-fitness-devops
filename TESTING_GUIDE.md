# Complete Testing Guide - 100% Assignment Verification

This guide will help you verify that all components are working correctly to ensure you get 100% on the assignment.

## 🎯 Pre-Testing Checklist

Before starting, ensure you have:
- [ ] Python 3.11+ installed
- [ ] Docker installed and running
- [ ] Docker Hub account
- [ ] Kubernetes cluster (Minikube or cloud)
- [ ] Jenkins server access
- [ ] SonarQube server access
- [ ] Git configured

---

## Phase 1: Local Application Testing

### 1.1 Test Python Application

```bash
# Navigate to project directory
cd Devops_Assignment2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test Base Version
python app.py
# Open browser: http://localhost:5000
# Expected: Application loads, you can add workouts
# Test: Add a workout, view summary
# Press Ctrl+C to stop

# Test Version 1.1
python app_v1.1.py
# Expected: Enhanced UI with categories
# Test: Add workouts in different categories

# Test Version 1.2
python app_v1.2.py
# Expected: Workout plans and diet guide tabs
# Test: Navigate through tabs

# Test Version 1.3
python app_v1.3.py
# Expected: User info, calorie calculation
# Test: Save user info, add workout with calories
```

**✅ Success Criteria:**
- All versions start without errors
- Can add workouts successfully
- API endpoints respond correctly
- Health check returns 200 OK

### 1.2 Test API Endpoints

```bash
# In another terminal, test API endpoints

# Health Check
curl http://localhost:5000/health
# Expected: {"status": "healthy", "version": "1.0"}

# Get Workouts
curl http://localhost:5000/api/workouts
# Expected: JSON with workout categories

# Add Workout
curl -X POST http://localhost:5000/api/workouts \
  -H "Content-Type: application/json" \
  -d '{"category": "Workout", "exercise": "Push-ups", "duration": 30}'
# Expected: {"message": "Workout added successfully", ...}

# Get Summary
curl http://localhost:5000/api/workouts/summary
# Expected: JSON with total_time and category_totals
```

**✅ Success Criteria:**
- All endpoints return correct status codes
- JSON responses are valid
- Data persists during session

---

## Phase 2: Unit Testing

### 2.1 Run All Tests

```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run all tests
pytest -v

# Expected output:
# ============== test session starts ==============
# tests/test_app.py::TestHealthEndpoint::test_health_check PASSED
# tests/test_app.py::TestWorkoutAPI::test_add_workout_success PASSED
# ... (all tests should PASS)
# ============== X passed in X.XXs ==============
```

**✅ Success Criteria:**
- All tests pass (15+ tests)
- No failures or errors
- Exit code: 0

### 2.2 Test Coverage

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing

# Expected output:
# ----------- coverage: platform win32, python 3.11.x -----------
# Name              Stmts   Miss  Cover
# ------------------------------------
# app.py                XX      X    XX%
# app_v1.1.py           XX      X    XX%
# app_v1.3.py           XX      X    XX%
# ------------------------------------
# TOTAL                 XXX      X    XX%
```

**✅ Success Criteria:**
- Coverage > 85%
- Coverage report generated in `htmlcov/`
- Open `htmlcov/index.html` in browser to view detailed coverage

### 2.3 Test Specific Versions

```bash
# Test base version
pytest tests/test_app.py -v

# Test version 1.1
pytest tests/test_app_v1.1.py -v

# Test version 1.3
pytest tests/test_app_v1.3.py -v
```

**✅ Success Criteria:**
- All version-specific tests pass
- No import errors
- All assertions pass

---

## Phase 3: Docker Testing

### 3.1 Build Docker Images

```bash
# Replace 'your-username' with your Docker Hub username

# Build base image
docker build -t your-username/aceest-fitness:latest -f Dockerfile .
# Expected: Successfully built <image-id>
# Expected: Successfully tagged your-username/aceest-fitness:latest

# Build version images
docker build -t your-username/aceest-fitness:v1.1 -f Dockerfile.v1.1 .
docker build -t your-username/aceest-fitness:v1.2 -f Dockerfile.v1.2 .
docker build -t your-username/aceest-fitness:v1.3 -f Dockerfile.v1.3 .

# Verify images
docker images | grep aceest-fitness
# Expected: All 4 images listed
```

**✅ Success Criteria:**
- All images build successfully
- No build errors
- Images are tagged correctly
- Image sizes are reasonable (< 500MB)

### 3.2 Test Docker Containers Locally

```bash
# Test base image
docker run -d -p 5000:5000 --name test-app your-username/aceest-fitness:latest

# Wait a few seconds, then test
curl http://localhost:5000/health
# Expected: {"status": "healthy", "version": "1.0"}

# Test in browser
# Open: http://localhost:5000
# Expected: Application loads and works

# Check logs
docker logs test-app
# Expected: No errors, Gunicorn started

# Stop and remove
docker stop test-app
docker rm test-app

# Test version 1.3
docker run -d -p 5000:5000 --name test-v13 your-username/aceest-fitness:v1.3
curl http://localhost:5000/health
# Expected: {"status": "healthy", "version": "1.3"}
docker stop test-v13 && docker rm test-v13
```

**✅ Success Criteria:**
- Containers start successfully
- Health endpoint works
- Application is accessible
- No errors in logs

### 3.3 Push to Docker Hub

```bash
# Login to Docker Hub
docker login
# Enter your username and password

# Push all images
docker push your-username/aceest-fitness:latest
docker push your-username/aceest-fitness:v1.1
docker push your-username/aceest-fitness:v1.2
docker push your-username/aceest-fitness:v1.3

# Verify on Docker Hub website
# Go to: https://hub.docker.com/r/your-username/aceest-fitness
# Expected: All tags visible
```

**✅ Success Criteria:**
- All images pushed successfully
- Images visible on Docker Hub
- Tags are correct
- Images are accessible (public or with access)

---

## Phase 4: Jenkins Pipeline Testing

### 4.1 Configure Jenkins

1. **Install Plugins** (if not already):
   - Pipeline
   - Docker Pipeline
   - SonarQube Scanner
   - HTML Publisher
   - JUnit

2. **Add Credentials**:
   - Docker Hub: Username/Password
   - Kubernetes: kubeconfig file
   - SonarQube: Token

3. **Configure SonarQube**:
   - Add SonarQube server in Jenkins
   - Configure server URL and token

### 4.2 Create Pipeline

1. New Item → Pipeline
2. Name: `aceest-fitness-pipeline`
3. Pipeline → Definition: Pipeline script from SCM
4. SCM: Git
5. Repository URL: Your GitHub repo
6. Script Path: `Jenkinsfile`

### 4.3 Run Pipeline

```bash
# Trigger pipeline manually or push to GitHub

# Monitor pipeline in Jenkins:
# - Blue Ocean view (recommended)
# - Classic view
```

**✅ Success Criteria for Each Stage:**

1. **Checkout**: ✅ Repository cloned successfully
2. **Unit Tests**: ✅ All tests pass, coverage > 85%
3. **Code Quality**: ✅ SonarQube analysis completes
4. **Quality Gate**: ✅ Quality gate passes
5. **Build Docker Images**: ✅ All 4 images build successfully
6. **Test Docker Images**: ✅ Container test passes
7. **Push to Docker Hub**: ✅ All images pushed
8. **Deploy to Kubernetes**: ✅ Deployment successful (if on main/master)

**Expected Pipeline Duration:** 5-10 minutes

### 4.4 Verify Pipeline Artifacts

- [ ] Test results published
- [ ] Coverage report (HTML) published
- [ ] SonarQube report link available
- [ ] Build logs show no errors
- [ ] All stages show green (success)

---

## Phase 5: SonarQube Testing

### 5.1 Run SonarQube Analysis

```bash
# Install SonarQube Scanner (if not installed)
# Download from: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/

# Run analysis locally
sonar-scanner \
  -Dsonar.projectKey=aceest-fitness \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token

# Or let Jenkins run it (recommended)
```

### 5.2 Verify SonarQube Results

Go to SonarQube dashboard:
- **Coverage**: Should be > 80%
- **Duplications**: Should be < 3%
- **Maintainability Rating**: Should be A
- **Reliability Rating**: Should be A
- **Security Rating**: Should be A
- **Quality Gate**: Should be PASSED

**✅ Success Criteria:**
- Quality gate passes
- No critical bugs
- No security vulnerabilities
- Coverage meets threshold

---

## Phase 6: Kubernetes Deployment Testing

### 6.1 Prerequisites

```bash
# Verify kubectl is configured
kubectl cluster-info
# Expected: Cluster information displayed

# Verify namespace
kubectl get namespace aceest-fitness
# If not exists, create it:
kubectl apply -f k8s/namespace.yaml
```

### 6.2 Update Kubernetes Manifests

**IMPORTANT**: Replace `your-dockerhub-username` in all YAML files:

```bash
# Use find and replace in your editor or:
# Windows PowerShell:
(Get-Content k8s\*.yaml) -replace 'your-dockerhub-username', 'your-actual-username' | Set-Content k8s\*.yaml

# Linux/Mac:
sed -i 's/your-dockerhub-username/your-actual-username/g' k8s/*.yaml
```

### 6.3 Deploy Base Components

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml
# Expected: namespace/aceest-fitness created

# Create secret
kubectl apply -f k8s/secret.yaml
# Expected: secret/aceest-fitness-secret created

# Create configmap
kubectl apply -f k8s/configmap.yaml
# Expected: configmap/aceest-fitness-config created
```

### 6.4 Test Rolling Update Deployment

```bash
# Deploy
kubectl apply -f k8s/rolling-update-deployment.yaml

# Check deployment status
kubectl get deployment -n aceest-fitness
# Expected: aceest-fitness deployment shows 3/3 ready

# Check pods
kubectl get pods -n aceest-fitness
# Expected: 3 pods in Running state

# Check service
kubectl get svc -n aceest-fitness
# Expected: Service with external IP (LoadBalancer) or ClusterIP

# Get service URL
kubectl get svc aceest-fitness-service -n aceest-fitness
# Note the EXTERNAL-IP or use port-forward

# Test health endpoint
kubectl port-forward svc/aceest-fitness-service 8080:80 -n aceest-fitness
# In another terminal:
curl http://localhost:8080/health
# Expected: {"status": "healthy", "version": "1.3"}

# Test application
# Open: http://localhost:8080 (or external IP)
# Expected: Application loads and works
```

**✅ Success Criteria:**
- Deployment successful
- All pods running
- Service accessible
- Health check passes
- Application works

### 6.5 Test Blue-Green Deployment

```bash
# Deploy blue-green
kubectl apply -f k8s/blue-green-deployment.yaml

# Check both deployments
kubectl get deployment -n aceest-fitness
# Expected: aceest-fitness-blue and aceest-fitness-green

# Initially, service points to blue
kubectl get svc aceest-fitness-service -n aceest-fitness -o yaml | grep color
# Expected: color: blue

# Test blue version
kubectl port-forward svc/aceest-fitness-service 8080:80 -n aceest-fitness
curl http://localhost:8080/health
# Expected: Version 1.2 (blue)

# Switch to green
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"color":"green"}}}'

# Test green version
curl http://localhost:8080/health
# Expected: Version 1.3 (green)

# Rollback to blue
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"color":"blue"}}}'
```

**✅ Success Criteria:**
- Both deployments exist
- Traffic switches instantly
- No downtime during switch
- Rollback works

### 6.6 Test Canary Deployment

**Note**: Requires Istio installation

```bash
# Install Istio first (if not installed)
# Then deploy:
kubectl apply -f k8s/canary-deployment.yaml

# Check deployments
kubectl get deployment -n aceest-fitness
# Expected: aceest-fitness-stable (9 replicas) and aceest-fitness-canary (1 replica)

# Verify traffic split (90% stable, 10% canary)
# Send multiple requests and check versions
for i in {1..10}; do curl http://localhost:8080/health; done
# Expected: Mostly version 1.2 (stable), some version 1.3 (canary)
```

**✅ Success Criteria:**
- Canary deployment works
- Traffic split is correct
- Both versions accessible

### 6.7 Test Shadow Deployment

```bash
# Deploy shadow
kubectl apply -f k8s/shadow-deployment.yaml

# Check deployments
kubectl get deployment -n aceest-fitness
# Expected: aceest-fitness-production and aceest-fitness-shadow

# Production receives all traffic
kubectl port-forward svc/aceest-fitness-service 8080:80 -n aceest-fitness
curl http://localhost:8080/health
# Expected: Version 1.2 (production)

# Shadow runs in background (monitoring only)
kubectl get pods -l environment=shadow -n aceest-fitness
# Expected: Shadow pods running
```

**✅ Success Criteria:**
- Production deployment works
- Shadow deployment runs alongside
- No user impact from shadow

### 6.8 Test A/B Testing Deployment

**Note**: Requires Istio installation

```bash
# Deploy A/B testing
kubectl apply -f k8s/ab-testing-deployment.yaml

# Check deployments
kubectl get deployment -n aceest-fitness
# Expected: aceest-fitness-version-a and aceest-fitness-version-b

# Test traffic split (50/50)
for i in {1..20}; do curl http://localhost:8080/health; done
# Expected: ~50% version 1.2 (A), ~50% version 1.3 (B)
```

**✅ Success Criteria:**
- Both versions deployed
- Traffic split 50/50
- Both versions accessible

### 6.9 Test Rollback

```bash
# View rollout history
kubectl rollout history deployment/aceest-fitness -n aceest-fitness

# Rollback to previous version
kubectl rollout undo deployment/aceest-fitness -n aceest-fitness

# Check status
kubectl rollout status deployment/aceest-fitness -n aceest-fitness
# Expected: Rollback successful

# Verify version
curl http://localhost:8080/health
# Expected: Previous version
```

**✅ Success Criteria:**
- Rollback completes successfully
- Application works after rollback
- No downtime during rollback

---

## Phase 7: End-to-End Testing

### 7.1 Complete Workflow Test

1. **Make a code change**:
   ```bash
   # Edit app.py (add a comment)
   git add .
   git commit -m "Test: Verify CI/CD pipeline"
   git push origin main
   ```

2. **Monitor Jenkins**:
   - Pipeline should trigger automatically
   - All stages should pass
   - New Docker image should be built and pushed

3. **Verify Deployment**:
   - New version should deploy to Kubernetes
   - Application should update without downtime

**✅ Success Criteria:**
- Code change triggers pipeline
- All stages pass
- New version deploys
- Application works with new version

### 7.2 Test All Endpoints

```bash
# Get service URL
SERVICE_URL="http://<your-service-ip>"  # Or use port-forward

# Test all endpoints
curl $SERVICE_URL/health
curl $SERVICE_URL/
curl $SERVICE_URL/api/workouts
curl -X POST $SERVICE_URL/api/workouts \
  -H "Content-Type: application/json" \
  -d '{"category": "Workout", "exercise": "Test", "duration": 10}'
curl $SERVICE_URL/api/workouts/summary
curl $SERVICE_URL/summary
```

**✅ Success Criteria:**
- All endpoints respond
- No 404 or 500 errors
- Data persists correctly

---

## Phase 8: Final Verification Checklist

### 8.1 Application Requirements ✅

- [ ] Flask application works (all 4 versions)
- [ ] All API endpoints functional
- [ ] Health check endpoint works
- [ ] Application handles errors gracefully
- [ ] UI is responsive and functional

### 8.2 Testing Requirements ✅

- [ ] All unit tests pass (15+ tests)
- [ ] Test coverage > 85%
- [ ] Coverage reports generated
- [ ] Tests run in CI/CD pipeline
- [ ] Test results published in Jenkins

### 8.3 CI/CD Requirements ✅

- [ ] Jenkins pipeline configured
- [ ] Pipeline runs on code push
- [ ] All pipeline stages pass
- [ ] Docker images build successfully
- [ ] Images pushed to Docker Hub
- [ ] Deployment automated

### 8.4 Containerization Requirements ✅

- [ ] All versions containerized
- [ ] Docker images work locally
- [ ] Images pushed to Docker Hub
- [ ] Images tagged correctly
- [ ] Health checks in containers

### 8.5 Kubernetes Requirements ✅

- [ ] Application deployed to Kubernetes
- [ ] All 5 deployment strategies work
- [ ] Rollback mechanisms work
- [ ] Health checks configured
- [ ] Service accessible
- [ ] Zero-downtime deployment achieved

### 8.6 Code Quality Requirements ✅

- [ ] SonarQube analysis passes
- [ ] Quality gate passes
- [ ] Coverage > 80%
- [ ] No critical bugs
- [ ] No security vulnerabilities

### 8.7 Documentation Requirements ✅

- [ ] README.md complete
- [ ] ASSIGNMENT_REPORT.md (2-3 pages)
- [ ] All URLs documented
- [ ] Deployment guide included
- [ ] Challenges documented

### 8.8 Repository Requirements ✅

- [ ] GitHub repository public/accessible
- [ ] All code committed
- [ ] Proper branching structure
- [ ] Version tags created
- [ ] README updated with links

---

## 🎯 100% Assignment Checklist

### Must Have (Critical):

1. ✅ **Flask Application**: All 4 versions working
2. ✅ **Unit Tests**: >85% coverage, all tests pass
3. ✅ **Jenkins Pipeline**: Fully automated, all stages pass
4. ✅ **Docker Images**: All versions on Docker Hub
5. ✅ **Kubernetes**: At least 3 deployment strategies working
6. ✅ **SonarQube**: Quality gate passes
7. ✅ **Documentation**: README and 2-3 page report
8. ✅ **GitHub**: Repository accessible with all code

### Should Have (Important):

1. ✅ **All 5 Deployment Strategies**: Rolling, Blue-Green, Canary, Shadow, A/B
2. ✅ **Rollback Mechanisms**: Working for all strategies
3. ✅ **Health Checks**: Configured and working
4. ✅ **Zero-Downtime**: Achieved in deployments
5. ✅ **Code Quality**: A rating in SonarQube

### Nice to Have (Bonus):

1. ✅ **Monitoring**: Health check endpoints
2. ✅ **Logging**: Structured logging
3. ✅ **Security**: Secrets management
4. ✅ **Scalability**: Resource limits configured

---

## 🐛 Troubleshooting Common Issues

### Issue: Tests Fail

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run tests with verbose output
pytest -vv
```

### Issue: Docker Build Fails

```bash
# Check Docker is running
docker ps

# Clean build (no cache)
docker build --no-cache -t your-username/aceest-fitness:latest -f Dockerfile .

# Check Dockerfile syntax
docker build --dry-run -f Dockerfile .
```

### Issue: Kubernetes Deployment Fails

```bash
# Check cluster connectivity
kubectl cluster-info

# Check pod status
kubectl describe pod <pod-name> -n aceest-fitness

# Check events
kubectl get events -n aceest-fitness --sort-by='.lastTimestamp'

# Common issues:
# - Image pull errors: Check Docker Hub credentials
# - Resource limits: Check resource requests
# - Health check failures: Check /health endpoint
```

### Issue: Jenkins Pipeline Fails

- Check Jenkins console output
- Verify credentials are configured
- Check Docker daemon is running
- Verify SonarQube connection
- Check Kubernetes connectivity

### Issue: SonarQube Quality Gate Fails

- Review SonarQube dashboard
- Fix code quality issues
- Increase test coverage
- Address security vulnerabilities

---

## 📊 Success Metrics

If all tests pass, you should see:

- ✅ **Test Coverage**: >85%
- ✅ **Code Quality**: A rating
- ✅ **Build Success Rate**: 100%
- ✅ **Deployment Time**: <5 minutes
- ✅ **Zero-Downtime**: Achieved
- ✅ **Rollback Time**: <1 minute

---

## 🎓 Final Submission Checklist

Before submitting, verify:

1. [ ] All tests pass locally
2. [ ] All Docker images built and pushed
3. [ ] Jenkins pipeline runs successfully
4. [ ] SonarQube quality gate passes
5. [ ] Kubernetes deployments work
6. [ ] All endpoints accessible
7. [ ] Documentation complete
8. [ ] GitHub repository updated
9. [ ] All URLs documented
10. [ ] Assignment report complete

---

**If all phases pass, you're ready for 100%! 🎉**

Good luck with your assignment!

