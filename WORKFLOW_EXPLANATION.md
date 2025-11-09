# GitHub Actions Workflow - Single Comprehensive Pipeline

## ✅ Consolidated into ONE Workflow

All CI/CD functionality is now in **ONE file**: `.github/workflows/main.yml`

**Before**: 4 separate workflows (triggering 4 times on each push)  
**After**: 1 comprehensive workflow (runs once, covers everything)

---

## 📋 What the Single Workflow Does

### Job 1: File Structure Validation ✅
- Validates all required files exist
- Checks application files (app.py, app_v1.1.py, app_v1.2.py, app_v1.3.py)
- Checks Docker files (4 Dockerfiles)
- Checks Kubernetes manifests (8 YAML files)
- Checks test files
- Checks CI/CD configuration files
- Checks documentation

### Job 2: Code Quality Check ✅
- Linting with flake8
- Code formatting check with black
- Non-blocking (warnings only)

### Job 3: Unit Tests & Coverage ✅
- Tests all application imports
- Runs all 18 unit tests
- Generates coverage reports (XML, HTML, terminal)
- Checks coverage threshold (>85%)
- Uploads coverage HTML as artifact

### Job 4: Docker Build & Test ✅
- Builds all 4 Docker images in parallel
- Tests each image (health check)
- Pushes to Docker Hub (on main branch only)
- Tags images with version and commit SHA

### Job 5: Kubernetes Validation ✅
- Validates all Kubernetes YAML files
- Checks for placeholder values
- Ensures manifests are syntactically correct

### Job 6: SonarQube Analysis ✅ (Optional)
- Runs SonarQube scan
- Only runs if SONAR_TOKEN is configured
- Non-blocking

### Job 7: Integration Test ✅
- Starts application
- Tests all API endpoints
- Verifies end-to-end functionality

### Job 8: Pipeline Summary ✅
- Generates summary report
- Shows status of all jobs
- Uploads summary as artifact

---

## 🎯 Benefits of Single Workflow

1. **One Run Per Push**: Only triggers once instead of 4 times
2. **Faster**: Jobs run in parallel where possible
3. **Clearer**: All checks in one place
4. **Easier to Maintain**: One file to update
5. **Better Dependencies**: Jobs depend on each other logically
6. **Complete Coverage**: Everything runs in one pipeline

---

## 🔄 Workflow Execution Flow

```
Push to GitHub
    ↓
Job 1: Validate Files (runs immediately)
    ↓
Job 2: Code Quality (parallel)
Job 3: Unit Tests (parallel)
    ↓
Job 4: Docker Build (waits for Job 3)
    ↓
Job 5: Kubernetes Validation (waits for Job 1)
Job 6: SonarQube (waits for Job 3, optional)
Job 7: Integration Test (waits for Jobs 3 & 4)
    ↓
Job 8: Summary (waits for all, shows results)
```

---

## ⚙️ Configuration

### Required Secrets (Optional but Recommended):
- `DOCKER_HUB_USERNAME` - For pushing Docker images
- `DOCKER_HUB_TOKEN` - Docker Hub access token
- `SONAR_TOKEN` - SonarQube authentication token
- `SONAR_HOST_URL` - SonarQube server URL

### Triggers:
- **Push** to main/master/develop branches
- **Pull Request** to main/master
- **Manual** trigger (workflow_dispatch)

---

## 📊 Expected Results

When you push code, you'll see:
- ✅ File validation passes
- ✅ Code quality checks (warnings only)
- ✅ All 18 tests pass
- ✅ Coverage >85%
- ✅ All 4 Docker images build
- ✅ Kubernetes manifests valid
- ✅ Integration tests pass
- ✅ Summary report generated

---

## 🎉 Result

**One workflow file** that covers **all assignment requirements**:
- ✅ File validation
- ✅ Code quality
- ✅ Unit testing
- ✅ Docker builds
- ✅ Kubernetes validation
- ✅ SonarQube (optional)
- ✅ Integration testing
- ✅ Summary report

**No more multiple workflow triggers!** 🚀

