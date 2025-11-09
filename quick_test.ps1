# Quick Test Script for ACEest Fitness Application (PowerShell)
# This script runs basic tests to verify everything is working

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "ACEest Fitness - Quick Test Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$script:PASSED = 0
$script:FAILED = 0

function Test-File {
    param($FilePath, $Description)
    
    if (Test-Path $FilePath) {
        Write-Host "✓ PASSED: $Description" -ForegroundColor Green
        $script:PASSED++
        return $true
    } else {
        Write-Host "✗ FAILED: $Description" -ForegroundColor Red
        $script:FAILED++
        return $false
    }
}

function Test-Command {
    param($Command, $Description)
    
    try {
        $null = Get-Command $Command -ErrorAction Stop
        Write-Host "✓ PASSED: $Description" -ForegroundColor Green
        $script:PASSED++
        return $true
    } catch {
        Write-Host "✗ FAILED: $Description" -ForegroundColor Red
        $script:FAILED++
        return $false
    }
}

# Define functions before using them

Write-Host "Phase 1: Python Environment" -ForegroundColor Yellow
Write-Host "---------------------------" -ForegroundColor Yellow

Test-Command "python" "Python installed"
Test-Command "pip" "pip installed"

if (Test-Path "venv") {
    Write-Host "✓ PASSED: Virtual environment exists" -ForegroundColor Green
    $script:PASSED++
} else {
    Write-Host "⚠ WARNING: Virtual environment not found (run: python -m venv venv)" -ForegroundColor Yellow
}

Test-File "requirements.txt" "requirements.txt exists"

Write-Host ""
Write-Host "Phase 2: Application Files" -ForegroundColor Yellow
Write-Host "---------------------------" -ForegroundColor Yellow

@("app.py", "app_v1.1.py", "app_v1.2.py", "app_v1.3.py") | ForEach-Object {
    Test-File $_ "$_ exists"
}

Write-Host ""
Write-Host "Phase 3: Test Files" -ForegroundColor Yellow
Write-Host "-------------------" -ForegroundColor Yellow

@("tests/test_app.py", "tests/test_app_v1.1.py", "tests/test_app_v1.3.py") | ForEach-Object {
    Test-File $_ "$_ exists"
}

Write-Host ""
Write-Host "Phase 4: Docker Files" -ForegroundColor Yellow
Write-Host "---------------------" -ForegroundColor Yellow

@("Dockerfile", "Dockerfile.v1.1", "Dockerfile.v1.2", "Dockerfile.v1.3") | ForEach-Object {
    Test-File $_ "$_ exists"
}

Test-Command "docker" "Docker installed"

Write-Host ""
Write-Host "Phase 5: Kubernetes Files" -ForegroundColor Yellow
Write-Host "------------------------" -ForegroundColor Yellow

$K8S_FILES = @(
    "k8s/namespace.yaml",
    "k8s/configmap.yaml",
    "k8s/secret.yaml",
    "k8s/rolling-update-deployment.yaml",
    "k8s/blue-green-deployment.yaml",
    "k8s/canary-deployment.yaml",
    "k8s/shadow-deployment.yaml",
    "k8s/ab-testing-deployment.yaml"
)

$K8S_FILES | ForEach-Object {
    Test-File $_ "$_ exists"
}

Test-Command "kubectl" "kubectl installed"

Write-Host ""
Write-Host "Phase 6: CI/CD Files" -ForegroundColor Yellow
Write-Host "-------------------" -ForegroundColor Yellow

Test-File "Jenkinsfile" "Jenkinsfile exists"
Test-File "sonar-project.properties" "sonar-project.properties exists"

Write-Host ""
Write-Host "Phase 7: Documentation" -ForegroundColor Yellow
Write-Host "---------------------" -ForegroundColor Yellow

@("README.md", "ASSIGNMENT_REPORT.md", "DEPLOYMENT_GUIDE.md", "TESTING_GUIDE.md") | ForEach-Object {
    Test-File $_ "$_ exists"
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Passed: $script:PASSED" -ForegroundColor Green
Write-Host "Failed: $script:FAILED" -ForegroundColor Red
Write-Host ""

if ($script:FAILED -eq 0) {
    Write-Host "✓ All file checks passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Run: pytest --cov=. --cov-report=html"
    Write-Host "2. Build Docker images"
    Write-Host "3. Test Jenkins pipeline"
    Write-Host "4. Deploy to Kubernetes"
    exit 0
} else {
    Write-Host "✗ Some checks failed. Please fix the issues above." -ForegroundColor Red
    exit 1
}

