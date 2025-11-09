# SonarQube Setup Guide

## ✅ SonarQube Configuration Status

Your project includes complete SonarQube configuration:

### Configuration Files
- ✅ `sonar-project.properties` - Main configuration file
- ✅ `sonar-scanner.properties` - Scanner configuration
- ✅ `.sonarqube/README.md` - Setup instructions

### Integration
- ✅ Jenkinsfile - SonarQube stage configured
- ✅ GitHub Actions - SonarQube analysis included
- ✅ Coverage integration - coverage.xml configured

---

## 📋 Quick Setup Steps

### Option 1: Using Docker (Recommended for Testing)

```bash
# Run SonarQube in Docker
docker run -d \
  --name sonarqube \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:latest

# Wait for SonarQube to start (check http://localhost:9000)
# Default credentials: admin/admin
```

### Option 2: Local Installation

1. Download SonarQube from: https://www.sonarqube.org/downloads/
2. Extract and run: `bin/[OS]/sonar.sh start`
3. Access: http://localhost:9000

---

## 🔧 Configuration Steps

### Step 1: Create Project in SonarQube

1. Login to SonarQube (http://localhost:9000)
2. Click "Create Project" → "Manually"
3. Project Key: `aceest-fitness`
4. Display Name: `ACEest Fitness & Gym Application`
5. Click "Set Up"

### Step 2: Generate Token

1. Go to: My Account → Security
2. Generate Token: `aceest-fitness-token`
3. Copy the token (you'll need it for Jenkins/GitHub Actions)

### Step 3: Configure Jenkins

1. **Install SonarQube Plugin**:
   - Manage Jenkins → Manage Plugins
   - Install "SonarQube Scanner"

2. **Configure SonarQube Server**:
   - Manage Jenkins → Configure System
   - SonarQube servers → Add SonarQube
   - Name: `SonarQube`
   - Server URL: `http://localhost:9000` (or your SonarQube URL)
   - Server authentication token: Click "Add" → Secret text
     - ID: `sonar-token`
     - Secret: Your SonarQube token

3. **Update Jenkinsfile** (if needed):
   - The Jenkinsfile already has SonarQube stage
   - Ensure `SONAR_HOST_URL` environment variable is set

### Step 4: Configure GitHub Actions (Optional)

Add secrets in GitHub repository:
- Settings → Secrets and variables → Actions
- Add secret: `SONAR_TOKEN` = Your SonarQube token
- Add secret: `SONAR_HOST_URL` = Your SonarQube URL

---

## 🧪 Test SonarQube Analysis

### Via Command Line

```bash
# Install SonarQube Scanner
# Download from: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/

# Run analysis
sonar-scanner \
  -Dsonar.projectKey=aceest-fitness \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token-here
```

### Via Jenkins

1. Push code to GitHub
2. Jenkins pipeline will automatically:
   - Run tests
   - Generate coverage
   - Run SonarQube analysis
   - Check quality gate

### Via GitHub Actions

1. Push code to GitHub
2. GitHub Actions will automatically run SonarQube analysis
3. View results in Actions tab

---

## 📊 View Results

After analysis, view results at:
- **SonarQube Dashboard**: http://your-sonarqube-url/dashboard?id=aceest-fitness
- **Coverage**: Shows code coverage percentage
- **Issues**: Lists bugs, vulnerabilities, code smells
- **Measures**: Code metrics and quality ratings

---

## ✅ Verification Checklist

- [ ] SonarQube server running
- [ ] Project created in SonarQube
- [ ] Token generated
- [ ] Jenkins configured with SonarQube
- [ ] Jenkins credentials added (`sonar-token`)
- [ ] GitHub Actions secrets added (if using)
- [ ] Analysis runs successfully
- [ ] Quality gate passes
- [ ] Reports accessible

---

## 🔍 Current Configuration

Your `sonar-project.properties` includes:

```properties
sonar.projectKey=aceest-fitness
sonar.projectName=ACEest Fitness & Gym Application
sonar.projectVersion=1.3
sonar.sources=.
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
sonar.qualitygate.wait=true
```

**Status**: ✅ **Configuration Complete**

---

## 📝 Notes

- SonarQube analysis is integrated in Jenkins pipeline
- Coverage reports are automatically generated
- Quality gates are enforced
- All configuration files are present

**Your SonarQube setup is complete!** 🎉

