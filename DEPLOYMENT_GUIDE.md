# Deployment Guide - ACEest Fitness & Gym

## Quick Start Guide

This guide provides step-by-step instructions for deploying the ACEest Fitness application.

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Docker installed and running
- [ ] Docker Hub account created
- [ ] Kubernetes cluster (Minikube/Cloud) configured
- [ ] Jenkins server accessible
- [ ] SonarQube server configured
- [ ] kubectl configured and connected to cluster

## Step 1: Local Setup

### 1.1 Clone and Setup

```bash
git clone <your-repo-url>
cd Devops_Assignment2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Run Locally

```bash
# Run base version
python app.py

# Run version 1.1
python app_v1.1.py

# Run version 1.2
python app_v1.2.py

# Run version 1.3
python app_v1.3.py
```

### 1.3 Run Tests

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=. --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

## Step 2: Docker Setup

### 2.1 Update Docker Hub Username

Replace `your-dockerhub-username` in:
- All Dockerfiles
- Jenkinsfile
- Kubernetes YAML files

### 2.2 Build Docker Images

```bash
# Build base image
docker build -t your-dockerhub-username/aceest-fitness:latest -f Dockerfile .

# Build version images
docker build -t your-dockerhub-username/aceest-fitness:v1.1 -f Dockerfile.v1.1 .
docker build -t your-dockerhub-username/aceest-fitness:v1.2 -f Dockerfile.v1.2 .
docker build -t your-dockerhub-username/aceest-fitness:v1.3 -f Dockerfile.v1.3 .

# Verify images
docker images | grep aceest-fitness
```

### 2.3 Test Docker Images Locally

```bash
# Run container
docker run -d -p 5000:5000 --name aceest-test your-dockerhub-username/aceest-fitness:latest

# Test health endpoint
curl http://localhost:5000/health

# View logs
docker logs aceest-test

# Stop and remove
docker stop aceest-test
docker rm aceest-test
```

### 2.4 Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push images
docker push your-dockerhub-username/aceest-fitness:latest
docker push your-dockerhub-username/aceest-fitness:v1.1
docker push your-dockerhub-username/aceest-fitness:v1.2
docker push your-dockerhub-username/aceest-fitness:v1.3
```

## Step 3: Jenkins Configuration

### 3.1 Install Required Plugins

In Jenkins, go to: Manage Jenkins → Manage Plugins → Available

Install:
- Pipeline
- Docker Pipeline
- SonarQube Scanner
- HTML Publisher
- JUnit

### 3.2 Configure Credentials

Go to: Manage Jenkins → Manage Credentials → System → Global credentials

Add:
1. **Docker Hub Credentials**
   - Kind: Username with password
   - ID: `docker-hub-credentials`
   - Username: Your Docker Hub username
   - Password: Your Docker Hub password

2. **Kubernetes Config**
   - Kind: Secret file
   - ID: `kubeconfig`
   - File: Your kubeconfig file

3. **SonarQube Token**
   - Kind: Secret text
   - ID: `sonar-token`
   - Secret: Your SonarQube token

### 3.3 Configure SonarQube

1. Install SonarQube server
2. Create project: `aceest-fitness`
3. Generate token
4. In Jenkins: Manage Jenkins → Configure System → SonarQube servers
   - Add SonarQube installation
   - Name: `SonarQube`
   - Server URL: Your SonarQube URL
   - Server authentication token: Your token

### 3.4 Create Pipeline

1. New Item → Pipeline
2. Name: `aceest-fitness-pipeline`
3. Pipeline → Definition: Pipeline script from SCM
4. SCM: Git
5. Repository URL: Your GitHub repository
6. Credentials: (if private repo)
7. Branch: `*/main` or `*/master`
8. Script Path: `Jenkinsfile`

### 3.5 Trigger Pipeline

- Manual: Click "Build Now"
- Automatic: Configure webhook in GitHub
  - Settings → Webhooks → Add webhook
  - Payload URL: `http://your-jenkins-url/github-webhook/`
  - Content type: `application/json`
  - Events: `Just the push event`

## Step 4: Kubernetes Deployment

### 4.1 Update Kubernetes Manifests

Replace `your-dockerhub-username` in all YAML files in `k8s/` directory.

### 4.2 Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 4.3 Create Secrets

```bash
# Edit secret.yaml with your values
kubectl apply -f k8s/secret.yaml
```

### 4.4 Create ConfigMap

```bash
kubectl apply -f k8s/configmap.yaml
```

### 4.5 Deploy Application

Choose one deployment strategy:

#### Option 1: Rolling Update (Recommended for Start)

```bash
kubectl apply -f k8s/rolling-update-deployment.yaml
kubectl rollout status deployment/aceest-fitness -n aceest-fitness
```

#### Option 2: Blue-Green Deployment

```bash
kubectl apply -f k8s/blue-green-deployment.yaml

# Initially, service points to blue
# To switch to green:
kubectl patch service aceest-fitness-service -n aceest-fitness \
  -p '{"spec":{"selector":{"color":"green"}}}'
```

#### Option 3: Canary Deployment

**Note**: Requires Istio to be installed

```bash
# Install Istio first
# Then:
kubectl apply -f k8s/canary-deployment.yaml
```

#### Option 4: Shadow Deployment

```bash
kubectl apply -f k8s/shadow-deployment.yaml
```

#### Option 5: A/B Testing

**Note**: Requires Istio to be installed

```bash
# Install Istio first
# Then:
kubectl apply -f k8s/ab-testing-deployment.yaml
```

### 4.6 Verify Deployment

```bash
# Check pods
kubectl get pods -n aceest-fitness

# Check services
kubectl get svc -n aceest-fitness

# Get external IP (for LoadBalancer)
kubectl get svc aceest-fitness-service -n aceest-fitness

# View logs
kubectl logs -f deployment/aceest-fitness -n aceest-fitness

# Test health endpoint
curl http://<external-ip>/health
```

## Step 5: Access Application

### 5.1 Get Service URL

```bash
# For LoadBalancer
kubectl get svc aceest-fitness-service -n aceest-fitness

# For Minikube
minikube service aceest-fitness-service -n aceest-fitness
```

### 5.2 Application Endpoints

- **Home**: `http://<service-ip>/`
- **Health Check**: `http://<service-ip>/health`
- **API**: `http://<service-ip>/api/workouts`
- **Summary**: `http://<service-ip>/summary`

## Step 6: Monitoring and Maintenance

### 6.1 View Logs

```bash
# Pod logs
kubectl logs -f deployment/aceest-fitness -n aceest-fitness

# Specific pod
kubectl logs <pod-name> -n aceest-fitness
```

### 6.2 Check Status

```bash
# Deployment status
kubectl get deployment -n aceest-fitness

# Pod status
kubectl get pods -n aceest-fitness

# Service status
kubectl get svc -n aceest-fitness

# Events
kubectl get events -n aceest-fitness --sort-by='.lastTimestamp'
```

### 6.3 Rollback

```bash
# View rollout history
kubectl rollout history deployment/aceest-fitness -n aceest-fitness

# Rollback to previous version
kubectl rollout undo deployment/aceest-fitness -n aceest-fitness

# Rollback to specific revision
kubectl rollout undo deployment/aceest-fitness --to-revision=2 -n aceest-fitness
```

### 6.4 Scale Deployment

```bash
# Scale to 5 replicas
kubectl scale deployment aceest-fitness --replicas=5 -n aceest-fitness

# Auto-scaling (requires metrics server)
kubectl autoscale deployment aceest-fitness --min=2 --max=10 --cpu-percent=80 -n aceest-fitness
```

## Troubleshooting

### Issue: Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n aceest-fitness

# Check events
kubectl get events -n aceest-fitness

# Common issues:
# - Image pull errors: Check Docker Hub credentials
# - Resource limits: Check resource requests/limits
# - Health check failures: Check application health endpoint
```

### Issue: Service not accessible

```bash
# Check service endpoints
kubectl get endpoints aceest-fitness-service -n aceest-fitness

# Check service selector matches pod labels
kubectl get pods --show-labels -n aceest-fitness
kubectl get svc aceest-fitness-service -o yaml -n aceest-fitness
```

### Issue: Jenkins pipeline fails

- Check Jenkins console output
- Verify credentials are configured
- Check Docker daemon is running (if using Docker-in-Docker)
- Verify SonarQube connection
- Check Kubernetes connectivity

### Issue: SonarQube quality gate fails

- Review SonarQube dashboard
- Fix code quality issues
- Increase test coverage
- Address security vulnerabilities

## Next Steps

1. Set up monitoring (Prometheus/Grafana)
2. Configure logging (ELK stack)
3. Set up database (PostgreSQL)
4. Implement authentication
5. Add CI/CD for multiple environments
6. Set up backup and disaster recovery

## Support

For issues or questions:
- Check README.md for detailed documentation
- Review ASSIGNMENT_REPORT.md for architecture details
- Check Jenkins pipeline logs
- Review Kubernetes events and logs

---

**Last Updated**: [Current Date]

