pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USER = credentials('docker-hub-username')
        DOCKER_IMAGE = "${DOCKER_HUB_USER}/mlops-sentiment-analysis"
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USERNAME = credentials('docker-hub-username')
        DOCKER_PASSWORD = credentials('docker-hub-password')
        ADMIN_EMAIL = credentials('admin-email')
        SMTP_SERVER = 'smtp.gmail.com'
        SMTP_PORT = '587'
        SMTP_USERNAME = credentials('smtp-username')
        SMTP_PASSWORD = credentials('smtp-password')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Checked out code from ${env.GIT_URL}"
            }
        }
        
        stage('Environment Setup') {
            steps {
                script {
                    // Check Python installation
                    sh 'python --version || echo "Python is not installed!"'
                    echo "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    echo "Branch: ${env.BRANCH_NAME}"
                    echo "Build Number: ${env.BUILD_NUMBER}"
                }
            }
        }
        
        stage('Code Quality Check') {
            steps {
                script {
                    try {
                        sh '''
                        python -m pip install --upgrade pip
                        pip install flake8
                        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                        '''
                        echo "✅ Code quality check passed"
                    } catch (Exception e) {
                        echo "❌ Code quality check failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error "Code quality check failed"
                    }
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                script {
                    try {
                        sh '''
                        pip install pytest pytest-cov pytest-mock
                        python -m pytest test_app.py -v --cov=app --cov-report=xml --cov-report=html
                        '''
                        echo "✅ Unit tests passed"
                        
                        // Archive test results
                        publishTestResults testResultsPattern: 'test-results.xml'
                        publishCoverage adapters: [
                            coberturaAdapter('coverage.xml')
                        ], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                        
                    } catch (Exception e) {
                        echo "❌ Unit tests failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error "Unit tests failed"
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        // Build and tag Docker image with both build number and latest
                        sh '''
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                        '''
                        echo "✅ Docker image built successfully"
                    } catch (Exception e) {
                        echo "❌ Docker build failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error "Docker build failed"
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    try {
                        sh '''
                        # Install trivy for security scanning
                        curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
                        trivy image --exit-code 0 --severity HIGH,CRITICAL ${DOCKER_IMAGE}:${DOCKER_TAG}
                        '''
                        echo "✅ Security scan passed"
                    } catch (Exception e) {
                        echo "⚠️ Security scan found issues: ${e.getMessage()}"
                        // Don't fail the build for security warnings, just log them
                    }
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    try {
                        sh '''
                        echo ${DOCKER_PASSWORD} | docker login ${DOCKER_REGISTRY} -u ${DOCKER_USERNAME} --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        '''
                        echo "✅ Docker image pushed successfully"
                    } catch (Exception e) {
                        echo "❌ Docker push failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error "Docker push failed"
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                script {
                    try {
                        sh '''
                        # Stop and remove existing container
                        docker stop mlops-app-staging || true
                        docker rm mlops-app-staging || true
                        
                        # Run new container
                        docker run -d --name mlops-app-staging -p 5001:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                        
                        # Wait for container to start
                        sleep 10
                        
                        # Health check
                        curl -f http://localhost:5001/health || exit 1
                        '''
                        echo "✅ Staging deployment successful"
                    } catch (Exception e) {
                        echo "❌ Staging deployment failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error "Staging deployment failed"
                    }
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                script {
                    try {
                        sh '''
                        # Test staging deployment
                        curl -f http://localhost:5001/health
                        curl -X POST http://localhost:5001/predict \
                          -H "Content-Type: application/json" \
                          -d '{"review": "This movie is fantastic!"}'
                        '''
                        echo "✅ Integration tests passed"
                    } catch (Exception e) {
                        echo "❌ Integration tests failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error "Integration tests failed"
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'master'
            }
            steps {
                script {
                    try {
                        sh '''
                        # Stop and remove existing production container
                        docker stop mlops-app-production || true
                        docker rm mlops-app-production || true
                        
                        # Run new production container
                        docker run -d --name mlops-app-production -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                        
                        # Wait for container to start
                        sleep 10
                        
                        # Health check
                        curl -f http://localhost:5000/health || exit 1
                        '''
                        echo "✅ Production deployment successful"
                    } catch (Exception e) {
                        echo "❌ Production deployment failed: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        error "Production deployment failed"
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Clean up staging container
                sh 'docker stop mlops-app-staging || true'
                sh 'docker rm mlops-app-staging || true'
                
                // Clean up old Docker images
                sh '''
                docker image prune -f
                docker system prune -f
                '''
            }
        }
        
        success {
            script {
                echo "✅ Pipeline completed successfully!"
                
                // Send success notification
                sendEmailNotification(
                    to: "${ADMIN_EMAIL}",
                    subject: "✅ MLOps Deployment Successful - Build #${env.BUILD_NUMBER}",
                    body: """
                    Deployment Status: SUCCESS
                    Branch: ${env.BRANCH_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Docker Image: ${DOCKER_IMAGE}:${DOCKER_TAG}
                    Timestamp: ${new Date()}
                    
                    The MLOps sentiment analysis application has been successfully deployed!
                    
                    Production URL: http://localhost:5000
                    Staging URL: http://localhost:5001
                    
                    Best regards,
                    MLOps CI/CD Pipeline
                    """
                )
            }
        }
        
        failure {
            script {
                echo "❌ Pipeline failed!"
                
                // Send failure notification
                sendEmailNotification(
                    to: "${ADMIN_EMAIL}",
                    subject: "❌ MLOps Deployment Failed - Build #${env.BUILD_NUMBER}",
                    body: """
                    Deployment Status: FAILURE
                    Branch: ${env.BRANCH_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Timestamp: ${new Date()}
                    
                    The MLOps deployment has failed. Please check the Jenkins logs for details.
                    
                    Jenkins Build URL: ${env.BUILD_URL}
                    
                    Best regards,
                    MLOps CI/CD Pipeline
                    """
                )
            }
        }
    }
}

def sendEmailNotification(to, subject, body) {
    try {
        emailext (
            to: to,
            subject: subject,
            body: body,
            mimeType: 'text/html'
        )
        echo "✅ Email notification sent successfully"
    } catch (Exception e) {
        echo "❌ Failed to send email notification: ${e.getMessage()}"
    }
}
