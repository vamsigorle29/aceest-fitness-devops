pipeline {
    agent any
    
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
        DOCKER_IMAGE_NAME = 'aceest-fitness'
        DOCKER_HUB_REPO = 'your-dockerhub-username/aceest-fitness'
        KUBECONFIG = credentials('kubeconfig')
        SONAR_TOKEN = credentials('sonar-token')
        APP_VERSION = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                sh '''
                    python -m venv venv
                    source venv/bin/activate || . venv/Scripts/activate
                    pip install -r requirements.txt
                    pytest --cov=. --cov-report=xml --cov-report=html --junitxml=test-results.xml -v
                '''
            }
            post {
                always {
                    publishTestResults testResultsPattern: 'test-results.xml'
                    publishHTML([
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Code Quality - SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=aceest-fitness \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_TOKEN} \
                            -Dsonar.python.version=3.11 \
                            -Dsonar.coverage.exclusions=**/tests/**,**/venv/**,**/__pycache__/**
                    '''
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build Docker Images') {
            parallel {
                stage('Build Base Image') {
                    steps {
                        sh '''
                            docker build -t ${DOCKER_HUB_REPO}:latest -t ${DOCKER_HUB_REPO}:${APP_VERSION} -f Dockerfile .
                        '''
                    }
                }
                stage('Build v1.1 Image') {
                    steps {
                        sh '''
                            docker build -t ${DOCKER_HUB_REPO}:v1.1 -t ${DOCKER_HUB_REPO}:v1.1-${APP_VERSION} -f Dockerfile.v1.1 .
                        '''
                    }
                }
                stage('Build v1.2 Image') {
                    steps {
                        sh '''
                            docker build -t ${DOCKER_HUB_REPO}:v1.2 -t ${DOCKER_HUB_REPO}:v1.2-${APP_VERSION} -f Dockerfile.v1.2 .
                        '''
                    }
                }
                stage('Build v1.3 Image') {
                    steps {
                        sh '''
                            docker build -t ${DOCKER_HUB_REPO}:v1.3 -t ${DOCKER_HUB_REPO}:v1.3-${APP_VERSION} -f Dockerfile.v1.3 .
                        '''
                    }
                }
            }
        }
        
        stage('Test Docker Images') {
            steps {
                sh '''
                    docker run -d --name test-app -p 5000:5000 ${DOCKER_HUB_REPO}:latest
                    sleep 10
                    curl -f http://localhost:5000/health || exit 1
                    docker stop test-app && docker rm test-app
                '''
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo ${DOCKER_HUB_CREDENTIALS_PSW} | docker login -u ${DOCKER_HUB_CREDENTIALS_USR} --password-stdin
                    docker push ${DOCKER_HUB_REPO}:latest
                    docker push ${DOCKER_HUB_REPO}:${APP_VERSION}
                    docker push ${DOCKER_HUB_REPO}:v1.1
                    docker push ${DOCKER_HUB_REPO}:v1.1-${APP_VERSION}
                    docker push ${DOCKER_HUB_REPO}:v1.2
                    docker push ${DOCKER_HUB_REPO}:v1.2-${APP_VERSION}
                    docker push ${DOCKER_HUB_REPO}:v1.3
                    docker push ${DOCKER_HUB_REPO}:v1.3-${APP_VERSION}
                '''
            }
        }
        
        stage('Deploy to Kubernetes') {
            when {
                branch 'main' || branch 'master'
            }
            steps {
                sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/configmap.yaml
                    kubectl apply -f k8s/rolling-update-deployment.yaml
                    kubectl rollout status deployment/aceest-fitness -n aceest-fitness --timeout=5m
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
            sh '''
                echo "Build ${APP_VERSION} completed successfully"
            '''
        }
        failure {
            echo 'Pipeline failed!'
            emailext (
                subject: "Pipeline Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Check console output at ${env.BUILD_URL}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}

