# ACEest Fitness & Gym - DevOps CI/CD Pipeline

A comprehensive DevOps implementation for ACEest Fitness & Gym application with full CI/CD automation, containerization, and Kubernetes deployment strategies.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment Strategies](#deployment-strategies)
- [Testing](#testing)
- [Docker Images](#docker-images)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Monitoring & Health Checks](#monitoring--health-checks)

## 🎯 Overview

This project demonstrates a complete DevOps CI/CD pipeline for a Flask-based fitness tracking web application. It includes:

- **Version Control**: Git/GitHub with structured branching and tagging
- **CI/CD**: Jenkins automated pipeline
- **Testing**: Pytest unit tests with coverage reporting
- **Code Quality**: SonarQube static analysis
- **Containerization**: Docker images for all application versions
- **Orchestration**: Kubernetes with multiple deployment strategies
- **Container Registry**: Docker Hub integration

## 📁 Project Structure

```
.
├── app.py                    # Base Flask application
├── app_v1.1.py              # Version 1.1 application
├── app_v1.2.py              # Version 1.2 application
├── app_v1.3.py              # Version 1.3 application
├── requirements.txt          # Python dependencies
├── Dockerfile                # Base Docker image
├── Dockerfile.v1.1          # Version 1.1 Docker image
├── Dockerfile.v1.2          # Version 1.2 Docker image
├── Dockerfile.v1.3          # Version 1.3 Docker image
├── Jenkinsfile              # Jenkins CI/CD pipeline
├── pytest.ini               # Pytest configuration
├── sonar-project.properties # SonarQube configuration
├── tests/                   # Unit tests
│   ├── test_app.py
│   ├── test_app_v1.1.py
│   └── test_app_v1.3.py
├── k8s/                     # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── rolling-update-deployment.yaml
│   ├── blue-green-deployment.yaml
│   ├── canary-deployment.yaml
│   ├── shadow-deployment.yaml
│   └── ab-testing-deployment.yaml
├── templates/               # HTML templates
└── static/                  # Static files (CSS, JS)
```

## ✨ Features

### Application Versions

- **Base Version (app.py)**: Core workout tracking functionality
- **Version 1.1**: Enhanced UI with categories and timestamps
- **Version 1.2**: Added workout plans and diet guide tabs
- **Version 1.3**: Advanced features with progress tracking, user info, and calorie calculation

### Key Features

- Workout logging with categories (Warm-up, Workout, Cool-down)
- Workout summary and statistics
- User information management (BMI, BMR calculation)
- Calorie calculation based on MET values
- Progress tracking and visualization
- RESTful API endpoints
- Health check endpoints

## 🔧 Prerequisites

- **Python 3.11+**
- **Docker** and **Docker Hub** account
- **Jenkins** (with required plugins)
- **Kubernetes** cluster (Minikube, EKS, GKE, or AKS)
- **SonarQube** server
- **Git** and **GitHub** account

### Required Jenkins Plugins

- Pipeline
- Docker Pipeline
- SonarQube Scanner
- HTML Publisher
- JUnit

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd Devops_Assignment2
```

### 2. Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Run tests
pytest --cov=. --cov-report=html
```

### 3. Docker Setup

```bash
# Build base image
docker build -t your-dockerhub-username/aceest-fitness:latest -f Dockerfile .

# Build version-specific images
docker build -t your-dockerhub-username/aceest-fitness:v1.1 -f Dockerfile.v1.1 .
docker build -t your-dockerhub-username/aceest-fitness:v1.2 -f Dockerfile.v1.2 .
docker build -t your-dockerhub-username/aceest-fitness:v1.3 -f Dockerfile.v1.3 .

# Test locally
docker run -p 5000:5000 your-dockerhub-username/aceest-fitness:latest

# Push to Docker Hub
docker login
docker push your-dockerhub-username/aceest-fitness:latest
```

### 4. Jenkins Configuration

1. **Create Credentials**:
   - `docker-hub-credentials`: Docker Hub username/password
   - `kubeconfig`: Kubernetes config file
   - `sonar-token`: SonarQube authentication token

2. **Configure SonarQube**:
   - Install SonarQube server
   - Create project in SonarQube
   - Generate authentication token
   - Configure in Jenkins (Manage Jenkins → Configure System → SonarQube servers)

3. **Create Pipeline**:
   - New Item → Pipeline
   - Configure → Pipeline → Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: Your GitHub repository
   - Script Path: Jenkinsfile

### 5. Kubernetes Setup

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets
kubectl apply -f k8s/secret.yaml

# Create configmap
kubectl apply -f k8s/configmap.yaml

# Deploy application (choose strategy)
kubectl apply -f k8s/rolling-update-deployment.yaml
# OR
kubectl apply -f k8s/blue-green-deployment.yaml
# OR
kubectl apply -f k8s/canary-deployment.yaml
```

## 🔄 CI/CD Pipeline

The Jenkins pipeline includes the following stages:

1. **Checkout**: Clone repository and get commit hash
2. **Unit Tests**: Run Pytest with coverage reporting
3. **Code Quality**: SonarQube analysis
4. **Quality Gate**: Wait for SonarQube quality gate approval
5. **Build Docker Images**: Build all version images in parallel
6. **Test Docker Images**: Verify images work correctly
7. **Push to Docker Hub**: Push all images with tags
8. **Deploy to Kubernetes**: Deploy to cluster (on main/master branch)

### Pipeline Triggers

- Push to repository
- Pull request creation
- Manual trigger
- Scheduled builds (optional)

## 🎯 Deployment Strategies

### 1. Rolling Update (Default)

Gradual replacement of old pods with new ones.

```bash
kubectl apply -f k8s/rolling-update-deployment.yaml
kubectl rollout status deployment/aceest-fitness -n aceest-fitness
```

**Features**:
- Zero-downtime deployment
- Automatic rollback on failure
- Configurable surge and unavailable pods

### 2. Blue-Green Deployment

Maintains two identical production environments.

```bash
kubectl apply -f k8s/blue-green-deployment.yaml

# Switch traffic from blue to green
kubectl patch service aceest-fitness-service -n aceest-fitness -p '{"spec":{"selector":{"color":"green"}}}'

# Rollback to blue
kubectl patch service aceest-fitness-service -n aceest-fitness -p '{"spec":{"selector":{"color":"blue"}}}'
```

**Features**:
- Instant rollback
- Full environment testing before switch
- No version mixing

### 3. Canary Deployment

Gradually roll out changes to a subset of users.

```bash
kubectl apply -f k8s/canary-deployment.yaml

# Requires Istio for traffic splitting
# 90% traffic to stable, 10% to canary
```

**Features**:
- Risk mitigation
- Gradual rollout
- Easy rollback

### 4. Shadow Deployment

Deploy new version alongside production, mirroring traffic.

```bash
kubectl apply -f k8s/shadow-deployment.yaml
```

**Features**:
- Test new version with real traffic
- No impact on users
- Performance comparison

### 5. A/B Testing

Split traffic between two versions for comparison.

```bash
kubectl apply -f k8s/ab-testing-deployment.yaml

# Requires Istio
# 50% traffic to version A, 50% to version B
```

**Features**:
- User experience comparison
- Data-driven decisions
- Feature validation

## 🧪 Testing

### Run Tests Locally

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific test file
pytest tests/test_app.py -v

# Specific test
pytest tests/test_app.py::TestHealthEndpoint::test_health_check -v
```

### Test Coverage

- Unit tests for all application versions
- API endpoint testing
- Health check validation
- Error handling tests
- Coverage reports generated in `htmlcov/`

## 🐳 Docker Images

All versions are containerized and available on Docker Hub:

- `your-dockerhub-username/aceest-fitness:latest`
- `your-dockerhub-username/aceest-fitness:v1.1`
- `your-dockerhub-username/aceest-fitness:v1.2`
- `your-dockerhub-username/aceest-fitness:v1.3`

### Image Features

- Multi-stage builds for optimization
- Health checks configured
- Non-root user (recommended for production)
- Minimal base image (python:3.11-slim)
- Production-ready with Gunicorn

## ☸️ Kubernetes Deployment

### Namespace

```bash
kubectl get namespace aceest-fitness
```

### Services

```bash
# Get service details
kubectl get svc -n aceest-fitness

# Get external IP (LoadBalancer)
kubectl get svc aceest-fitness-service -n aceest-fitness
```

### Pods

```bash
# List pods
kubectl get pods -n aceest-fitness

# View logs
kubectl logs -f deployment/aceest-fitness -n aceest-fitness

# Describe pod
kubectl describe pod <pod-name> -n aceest-fitness
```

### Rollback

```bash
# View rollout history
kubectl rollout history deployment/aceest-fitness -n aceest-fitness

# Rollback to previous version
kubectl rollout undo deployment/aceest-fitness -n aceest-fitness

# Rollback to specific revision
kubectl rollout undo deployment/aceest-fitness --to-revision=2 -n aceest-fitness
```

## 📊 Monitoring & Health Checks

### Health Endpoint

All versions include a `/health` endpoint:

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.3"
}
```

### Kubernetes Health Checks

- **Liveness Probe**: Restarts container if unhealthy
- **Readiness Probe**: Removes from service if not ready
- **Startup Probe**: Allows slow-starting containers

### Monitoring

- Application logs: `kubectl logs`
- Resource usage: `kubectl top pods`
- Events: `kubectl get events -n aceest-fitness`

## 🔐 Security Considerations

1. **Secrets Management**: Use Kubernetes secrets (not hardcoded)
2. **Image Security**: Scan images for vulnerabilities
3. **Network Policies**: Implement network segmentation
4. **RBAC**: Configure proper role-based access control
5. **TLS/SSL**: Enable HTTPS in production
6. **Secret Rotation**: Regularly rotate secrets

## 📝 Code Quality

### SonarQube Metrics

- Code coverage: >80%
- Duplicated lines: <3%
- Maintainability rating: A
- Reliability rating: A
- Security rating: A

### Quality Gates

- All tests must pass
- Coverage threshold: 80%
- No critical bugs
- No security vulnerabilities

## 🐛 Troubleshooting

### Common Issues

1. **Docker build fails**:
   - Check Docker daemon is running
   - Verify Dockerfile syntax
   - Check base image availability

2. **Kubernetes deployment fails**:
   - Verify cluster connectivity: `kubectl cluster-info`
   - Check image pull secrets
   - Review pod events: `kubectl describe pod`

3. **Jenkins pipeline fails**:
   - Check credentials configuration
   - Verify plugin installations
   - Review pipeline logs

4. **Tests fail**:
   - Ensure dependencies installed
   - Check Python version compatibility
   - Verify test data

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [SonarQube Documentation](https://docs.sonarqube.org/)

## 👥 Contributors

DevOps Assignment - ACEest Fitness & Gym

## 📄 License

This project is created for educational purposes as part of DevOps assignment.

## 🔗 Repository Links

- **GitHub Repository**: [Your Repository URL]
- **Docker Hub**: [Your Docker Hub Repository]
- **Jenkins**: [Your Jenkins URL]
- **SonarQube**: [Your SonarQube URL]
- **Kubernetes Cluster**: [Your Cluster Endpoint]

---

**Note**: Replace all placeholder values (your-dockerhub-username, repository URLs, etc.) with your actual values before deployment.

