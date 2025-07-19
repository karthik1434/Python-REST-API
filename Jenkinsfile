pipeline {
    agent any

    triggers {
        // Poll SCM every 1 min for new commits
        pollSCM('* * * * *')
    }

    environment {
        DOCKER_IMAGE = "duggana1994/my-python-api-build-by-kenkins"
        DOCKER_TAG = "latest"
    }

    options {
        // Discard old builds to save space
        buildDiscarder(logRotator(numToKeepStr: '3'))
        // Fail if no output for 30 min
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {

        stage('Prepare Workspace') {
            steps {
                script {
                    echo "Cleaning workspace before checkout..."
                }
                cleanWs()  
            }
        }

        stage('Checkout') {
            steps {
                retry(3) { // ✅ retry checkout up to 3 times
                    git branch: 'main', url: 'https://github.com/karthik1434/Python-REST-API.git'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                sh 'docker push ${DOCKER_IMAGE}:${DOCKER_TAG}'
            }
        }
    }

    post {
        success {
            echo "✅ Build & Push completed successfully!"
        }
        failure {
            echo "❌ Build failed! Check logs."
        }
        always {
            echo "Cleaning up after build..."
            cleanWs()
        }
    }
}
