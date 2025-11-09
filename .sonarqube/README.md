# SonarQube Configuration

This directory contains SonarQube-specific configuration files.

## Setup Instructions

### 1. Install SonarQube Server
- Download from: https://www.sonarqube.org/downloads/
- Or use Docker: `docker run -d -p 9000:9000 sonarqube:latest`

### 2. Create Project in SonarQube
1. Login to SonarQube (default: admin/admin)
2. Create new project: `aceest-fitness`
3. Generate authentication token
4. Save token for Jenkins/GitHub Actions

### 3. Configure Jenkins
1. Install SonarQube Scanner plugin
2. Configure SonarQube server in Jenkins:
   - Manage Jenkins → Configure System → SonarQube servers
   - Add SonarQube installation
   - Name: `SonarQube`
   - Server URL: Your SonarQube URL
   - Server authentication token: Your token

3. Add credentials in Jenkins:
   - Manage Jenkins → Manage Credentials
   - Add Secret text
   - ID: `sonar-token`
   - Secret: Your SonarQube token

### 4. Run Analysis

#### Via Jenkins
- The Jenkinsfile already includes SonarQube analysis stage
- Pipeline will run automatically on code push

#### Via Command Line
```bash
# Install SonarQube Scanner
# Download from: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/

# Run analysis
sonar-scanner \
  -Dsonar.projectKey=aceest-fitness \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token
```

#### Via GitHub Actions
- Already configured in `.github/workflows/ci-cd.yml`
- Requires secrets: `SONAR_TOKEN` and `SONAR_HOST_URL`

## Configuration Files

- `sonar-project.properties` - Main SonarQube configuration
- `sonar-scanner.properties` - Scanner-specific settings
- `.sonarqube/` - SonarQube cache and analysis results

## Quality Gates

The project uses default SonarQube quality gates with:
- Minimum coverage: 80%
- No critical bugs
- No security vulnerabilities
- Maintainability rating: A

## Reports

After analysis, view reports at:
- SonarQube Dashboard: http://your-sonarqube-url/dashboard?id=aceest-fitness
- Coverage reports: `htmlcov/index.html`
- Test results: `test-results.xml`

