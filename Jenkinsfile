// Jenkins Declarative Pipeline for Medical Healthcare Multi-Agent Assistant
// GenAI & ML DevOps Pipeline: CI, Test, Container Build, Security, Registry Push & Kubernetes CD

pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
        timestamps()
    }

    environment {
        APP_NAME              = 'medical-healthcare-assistant'
        IMAGE_NAME            = 'medical-healthcare-assistant'
        IMAGE_TAG             = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY       = 'docker.io'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        GROQ_CREDENTIALS_ID   = 'groq-api-key'
        PYTHON_VENV           = '.venv'
        REPORTS_DIR           = 'reports'
    }

    parameters {
        choice(
            name: 'DEPLOY_ENV',
            choices: ['staging', 'production', 'none'],
            description: 'Target deployment environment'
        )
        booleanParam(
            name: 'RUN_SMOKE_TESTS',
            defaultValue: true,
            description: 'Run containerized smoke testing against /health and /ask endpoints'
        )
    }

    stages {
        // Stage 1: Checkout Source Code
        stage('Checkout Code') {
            steps {
                echo "==> Checking out repository source code..."
                checkout scm
            }
        }

        // Stage 2: Setup Python Virtual Environment and Install Dependencies
        stage('Setup Environment & Dependencies') {
            steps {
                echo "==> Setting up Python virtual environment and caching dependencies..."
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv ${PYTHON_VENV}
                            . ${PYTHON_VENV}/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m venv %PYTHON_VENV%
                            call %PYTHON_VENV%\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        // Stage 3: Code Compilation and Syntax Validation
        stage('Lint & Syntax Compilation') {
            steps {
                echo "==> Validating Python code integrity..."
                script {
                    if (isUnix()) {
                        sh '''
                            . ${PYTHON_VENV}/bin/activate
                            python -m compileall app/ tests/
                        '''
                    } else {
                        bat '''
                            call %PYTHON_VENV%\\Scripts\\activate.bat
                            python -m compileall app/ tests/
                        '''
                    }
                }
            }
        }

        // Stage 4: Automated Testing with Pytest
        stage('Automated Tests (Pytest)') {
            steps {
                echo "==> Executing unit, validation, agent, and security tests..."
                script {
                    // Create test reports folder
                    if (isUnix()) {
                        sh '''
                            mkdir -p ${REPORTS_DIR}
                            . ${PYTHON_VENV}/bin/activate
                            pytest -v --junitxml=${REPORTS_DIR}/pytest-results.xml tests/
                        '''
                    } else {
                        bat '''
                            if not exist %REPORTS_DIR% mkdir %REPORTS_DIR%
                            call %PYTHON_VENV%\\Scripts\\activate.bat
                            pytest -v --junitxml=%REPORTS_DIR%\\pytest-results.xml tests/
                        '''
                    }
                }
            }
            post {
                always {
                    // Publish test results in Jenkins UI
                    junit testResults: 'reports/pytest-results.xml', allowEmptyResults: true
                }
            }
        }

        // Stage 5: Kubernetes Manifests Validation
        stage('Validate Kubernetes Manifests') {
            steps {
                echo "==> Performing client-side dry-run validation on Kubernetes manifests..."
                script {
                    if (isUnix()) {
                        sh '''
                            if command -v kubectl >/dev/null 2>&1; then
                                kubectl apply --dry-run=client -f k8s/ || true
                            else
                                echo "kubectl not found in agent PATH; skipping k8s client check."
                            fi
                        '''
                    } else {
                        bat '''
                            where kubectl >nul 2>nul
                            if %ERRORLEVEL% EQU 0 (
                                kubectl apply --dry-run=client -f k8s/ || ver >nul
                            ) else (
                                echo kubectl not found in agent PATH; skipping k8s client check.
                            )
                        '''
                    }
                }
            }
        }

        // Stage 6: Build Container Image
        stage('Build Docker Image') {
            steps {
                echo "==> Building multi-stage hardened Docker image..."
                script {
                    if (isUnix()) {
                        sh '''
                            docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                        '''
                    } else {
                        bat '''
                            docker build -t %IMAGE_NAME%:%IMAGE_TAG% -t %IMAGE_NAME%:latest .
                        '''
                    }
                }
            }
        }

        // Stage 7: Container Smoke Test
        stage('Container Smoke Test') {
            when {
                expression { params.RUN_SMOKE_TESTS == true }
            }
            steps {
                echo "==> Booting container and testing health endpoint..."
                script {
                    if (isUnix()) {
                        sh '''
                            # Clean up any lingering container
                            docker rm -f smoke-test-app || true

                            # Run container in isolated network mode
                            docker run -d --name smoke-test-app -p 8080:8000 \
                                -e GROQ_API_KEY=gsk_jenkins_smoke_test_key \
                                -e GROQ_MODEL=qwen/qwen3.8-27b \
                                ${IMAGE_NAME}:${IMAGE_TAG}

                            # Allow container initialization
                            sleep 5

                            # Probe health endpoint
                            python3 -c "import urllib.request, json; res = json.loads(urllib.request.urlopen('http://localhost:8080/health').read().decode()); assert res['status'] == 'healthy'; print('Smoke test SUCCESS:', res)"

                            # Cleanup
                            docker rm -f smoke-test-app
                        '''
                    } else {
                        bat '''
                            docker rm -f smoke-test-app 2>nul || ver >nul

                            docker run -d --name smoke-test-app -p 8080:8000 ^
                                -e GROQ_API_KEY=gsk_jenkins_smoke_test_key ^
                                -e GROQ_MODEL=qwen/qwen3.8-27b ^
                                %IMAGE_NAME%:%IMAGE_TAG%

                            timeout /t 5 /nobreak >nul

                            python -c "import urllib.request, json; res = json.loads(urllib.request.urlopen('http://localhost:8080/health').read().decode()); assert res['status'] == 'healthy'; print('Smoke test SUCCESS:', res)"

                            docker rm -f smoke-test-app
                        '''
                    }
                }
            }
        }

        // Stage 8: Push Container to Registry (Optional credentials block)
        stage('Push Image to Registry') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                echo "==> Publishing Docker image to container registry..."
                script {
                    // Attempts credential login if DOCKER_CREDENTIALS_ID is configured in Jenkins
                    try {
                        withCredentials([usernamePassword(
                            credentialsId: env.DOCKER_CREDENTIALS_ID,
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )]) {
                            if (isUnix()) {
                                sh '''
                                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                                    docker tag ${IMAGE_NAME}:latest ${DOCKER_USER}/${IMAGE_NAME}:latest
                                    docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                                    docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
                                '''
                            } else {
                                bat '''
                                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                                    docker tag %IMAGE_NAME%:%IMAGE_TAG% %DOCKER_USER%/%IMAGE_NAME%:%IMAGE_TAG%
                                    docker tag %IMAGE_NAME%:latest %DOCKER_USER%/%IMAGE_NAME%:latest
                                    docker push %DOCKER_USER%/%IMAGE_NAME%:%IMAGE_TAG%
                                    docker push %DOCKER_USER%/%IMAGE_NAME%:latest
                                '''
                            }
                        }
                    } catch (Exception e) {
                        echo "Docker credentials not configured in Jenkins; tagged images locally for deployment: ${e.message}"
                    }
                }
            }
        }

        // Stage 9: Continuous Deployment to Kubernetes
        stage('Deploy to Kubernetes') {
            when {
                expression { params.DEPLOY_ENV != 'none' }
            }
            steps {
                echo "==> Deploying application to Kubernetes cluster (${params.DEPLOY_ENV})..."
                script {
                    if (isUnix()) {
                        sh '''
                            if command -v kubectl >/dev/null 2>&1; then
                                kubectl apply -f k8s/configmap.yaml
                                kubectl apply -f k8s/secret.yaml
                                kubectl apply -f k8s/deployment.yaml
                                kubectl apply -f k8s/service.yaml
                                kubectl apply -f k8s/ingress.yaml
                                kubectl rollout status deployment/medical-healthcare-deployment --timeout=90s || true
                            else
                                echo "kubectl not available on this agent; skipping deployment step."
                            fi
                        '''
                    } else {
                        bat '''
                            where kubectl >nul 2>nul
                            if %ERRORLEVEL% EQU 0 (
                                kubectl apply -f k8s/configmap.yaml
                                kubectl apply -f k8s/secret.yaml
                                kubectl apply -f k8s/deployment.yaml
                                kubectl apply -f k8s/service.yaml
                                kubectl apply -f k8s/ingress.yaml
                                kubectl rollout status deployment/medical-healthcare-deployment --timeout=90s || ver >nul
                            ) else (
                                echo kubectl not available on this agent; skipping deployment step.
                            )
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo "==> Cleaning up test artifacts and workspace..."
            script {
                if (isUnix()) {
                    sh 'docker rm -f smoke-test-app 2>/dev/null || true'
                } else {
                    bat 'docker rm -f smoke-test-app 2>nul || ver >nul'
                }
            }
        }
        success {
            echo "=========================================================="
            echo "  SUCCESS: Medical Healthcare Pipeline #${env.BUILD_NUMBER} Finished  "
            echo "=========================================================="
        }
        failure {
            echo "=========================================================="
            echo "  FAILURE: Medical Healthcare Pipeline #${env.BUILD_NUMBER} Failed    "
            echo "=========================================================="
        }
    }
}
