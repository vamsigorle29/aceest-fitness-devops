# Jenkins Testing Guide

## 🎯 How to Test Jenkins Pipeline

This guide explains how to test and validate the Jenkins CI/CD pipeline for the ACEest Fitness project.

---

## 📋 Prerequisites

Before testing Jenkins, ensure you have:

1. **Jenkins Server** installed and running
2. **Required Plugins** installed:
   - Pipeline
   - Docker Pipeline
   - SonarQube Scanner
   - HTML Publisher
   - JUnit
   - Blue Ocean (optional, for better UI)
3. **Docker** installed on Jenkins server
4. **Git** installed on Jenkins server
5. **Python 3.11+** available on Jenkins server

---

## 🔧 Step 1: Configure Jenkins

### 1.1 Install Required Plugins

1. Go to **Jenkins Dashboard** → **Manage Jenkins** → **Manage Plugins**
2. Install the following plugins:
   - **Pipeline**
   - **Docker Pipeline**
   - **SonarQube Scanner**
   - **HTML Publisher**
   - **JUnit**
   - **Blue Ocean** (recommended)

### 1.2 Configure Credentials

Go to **Manage Jenkins** → **Manage Credentials** → **System** → **Global credentials**

Add the following credentials:

#### Docker Hub Credentials
- **Kind**: Username with password
- **ID**: `docker-hub-credentials`
- **Username**: Your Docker Hub username
- **Password**: Your Docker Hub password/token

#### Kubernetes Config
- **Kind**: Secret file
- **ID**: `kubeconfig`
- **File**: Upload your `~/.kube/config` file

#### SonarQube Token
- **Kind**: Secret text
- **ID**: `sonar-token`
- **Secret**: Your SonarQube authentication token

### 1.3 Configure SonarQube Server

1. Go to **Manage Jenkins** → **Configure System**
2. Under **SonarQube servers**, click **Add SonarQube**
3. **Name**: `SonarQube`
4. **Server URL**: Your SonarQube server URL (e.g., `https://sonarqube.example.com`)
5. **Server authentication token**: Select the `sonar-token` credential

---

## 🚀 Step 2: Create Jenkins Pipeline

### 2.1 Create New Pipeline Job

1. Go to **Jenkins Dashboard** → **New Item**
2. **Item name**: `aceest-fitness-pipeline`
3. **Type**: Select **Pipeline**
4. Click **OK**

### 2.2 Configure Pipeline

1. **Description**: "ACEest Fitness CI/CD Pipeline"
2. **Pipeline** → **Definition**: Select **Pipeline script from SCM**
3. **SCM**: Select **Git**
4. **Repository URL**: `https://github.com/vamsigorle29/aceest-fitness-devops.git`
5. **Credentials**: (Add if repository is private)
6. **Branches to build**: `*/main` or `*/master`
7. **Script Path**: `Jenkinsfile`
8. Click **Save**

---

## ✅ Step 3: Test Jenkins Pipeline

### 3.1 Manual Trigger

1. Go to the pipeline job: `aceest-fitness-pipeline`
2. Click **Build Now**
3. Monitor the build progress

### 3.2 View Build Progress

**Classic View:**
- Click on the build number
- View **Console Output** for real-time logs
- Check **Stage View** for stage-by-stage progress

**Blue Ocean View (Recommended):**
- Click **Open Blue Ocean** from the pipeline page
- Visual representation of pipeline stages
- Click on each stage to see detailed logs

### 3.3 Expected Pipeline Stages

The pipeline should execute these stages in order:

1. ✅ **Checkout** - Clones repository
2. ✅ **Unit Tests** - Runs pytest with coverage
3. ✅ **Code Quality - SonarQube** - Runs SonarQube analysis
4. ✅ **Quality Gate** - Waits for SonarQube quality gate
5. ✅ **Build Docker Images** - Builds 4 images in parallel:
   - Base image (latest)
   - v1.1
   - v1.2
   - v1.3
6. ✅ **Test Docker Images** - Tests the base image
7. ✅ **Push to Docker Hub** - Pushes all images
8. ✅ **Deploy to Kubernetes** - Deploys to K8s (only on main/master branch)

---

## 🔍 Step 4: Validate Pipeline Results

### 4.1 Check Build Status

**Success Indicators:**
- All stages show green (✅)
- Build status: **SUCCESS**
- No errors in console output

**Failure Indicators:**
- Red stage indicates failure
- Check console output for error details
- Fix issues and rebuild

### 4.2 Verify Artifacts

After successful build, verify:

1. **Test Results**:
   - Go to build → **Test Result**
   - Should show all tests passed
   - Coverage should be >85%

2. **Coverage Report**:
   - Go to build → **Coverage Report** (HTML Publisher)
   - View HTML coverage report
   - Check coverage percentage

3. **SonarQube Report**:
   - Link to SonarQube dashboard
   - Quality gate status
   - Code quality metrics

4. **Docker Images**:
   - Check Docker Hub: `https://hub.docker.com/r/your-username/aceest-fitness`
   - Verify all tags are present:
     - `latest`
     - `v1.1`, `v1.2`, `v1.3`
     - Build number tags

5. **Kubernetes Deployment** (if on main/master):
   ```bash
   kubectl get pods -n aceest-fitness
   kubectl get svc -n aceest-fitness
   ```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Pipeline Fails at Checkout
**Error**: `Repository not found` or `Permission denied`

**Solution**:
- Verify repository URL is correct
- Add GitHub credentials if repository is private
- Check Jenkins has network access to GitHub

#### 2. Unit Tests Fail
**Error**: `ModuleNotFoundError` or test failures

**Solution**:
- Ensure Python 3.11+ is installed
- Check `requirements.txt` is present
- Verify test files are in `tests/` directory
- Check pytest is installed

#### 3. Docker Build Fails
**Error**: `Cannot connect to Docker daemon`

**Solution**:
- Ensure Docker is installed on Jenkins server
- Add Jenkins user to docker group: `sudo usermod -aG docker jenkins`
- Restart Jenkins: `sudo systemctl restart jenkins`
- Verify Docker is running: `docker ps`

#### 4. SonarQube Analysis Fails
**Error**: `Unable to connect to SonarQube server`

**Solution**:
- Verify SonarQube server URL is correct
- Check SonarQube token is valid
- Ensure SonarQube server is accessible from Jenkins
- Verify SonarQube server is configured in Jenkins

#### 5. Docker Push Fails
**Error**: `denied: requested access to the resource is denied`

**Solution**:
- Verify Docker Hub credentials are correct
- Check Docker Hub username in `Jenkinsfile` matches credentials
- Ensure Docker Hub token has push permissions
- Try logging in manually: `docker login`

#### 6. Kubernetes Deployment Fails
**Error**: `Unable to connect to the server`

**Solution**:
- Verify kubeconfig file is correct
- Check Kubernetes cluster is accessible
- Ensure kubectl is installed on Jenkins server
- Verify namespace exists: `kubectl get namespaces`

---

## 📊 Step 5: Validate Pipeline in GitHub Actions

The GitHub Actions workflow now includes Jenkinsfile validation:

1. **File Structure Check**: Validates Jenkinsfile exists
2. **Syntax Validation**: Checks for basic Groovy syntax
3. **Stage Validation**: Verifies required stages are present
4. **Placeholder Check**: Warns about placeholder values

**View Results:**
- Go to GitHub → **Actions** tab
- Click on latest workflow run
- Check **Jenkinsfile Validation** job

---

## 🎯 Success Criteria

Your Jenkins pipeline is working correctly if:

- ✅ All stages complete successfully
- ✅ All tests pass (18 tests)
- ✅ Coverage >85%
- ✅ SonarQube quality gate passes
- ✅ All 4 Docker images build successfully
- ✅ Docker images are pushed to Docker Hub
- ✅ Kubernetes deployment succeeds (on main/master)
- ✅ No errors in console output
- ✅ Build artifacts are generated

---

## 📝 Testing Checklist

Use this checklist to verify Jenkins setup:

- [ ] Jenkins server is running
- [ ] All required plugins are installed
- [ ] Docker Hub credentials configured
- [ ] SonarQube server configured
- [ ] Kubernetes credentials configured
- [ ] Pipeline job created
- [ ] Pipeline triggers successfully
- [ ] All stages complete
- [ ] Tests pass
- [ ] Coverage report generated
- [ ] Docker images built
- [ ] Images pushed to Docker Hub
- [ ] Kubernetes deployment works (if applicable)

---

## 🔗 Additional Resources

- **Jenkins Documentation**: https://www.jenkins.io/doc/
- **Pipeline Syntax**: https://www.jenkins.io/doc/book/pipeline/syntax/
- **Blue Ocean**: https://www.jenkins.io/doc/book/blueocean/
- **Docker Pipeline Plugin**: https://plugins.jenkins.io/docker-workflow/

---

## 💡 Tips

1. **Use Blue Ocean** for better visualization
2. **Enable Pipeline Logging** for debugging
3. **Test on a branch first** before main/master
4. **Monitor resource usage** (CPU, memory, disk)
5. **Set up email notifications** for build failures
6. **Use Jenkinsfile validation** in GitHub Actions before pushing

---

## ✅ Summary

Jenkins testing involves:
1. Setting up Jenkins server and plugins
2. Configuring credentials
3. Creating pipeline job
4. Running and monitoring builds
5. Validating results and artifacts

The pipeline is validated automatically in GitHub Actions, but full testing requires a running Jenkins server.

