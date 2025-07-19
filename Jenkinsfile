pipeline {
    agent any

    triggers {
        // Poll SCM every 1 min for new commits
        pollSCM('* * * * *')
    }

    environment {
        DOCKER_IMAGE = "duggana1994/my-python-api-build-by-kenkins"
        DOCKER_TAG = "latest"
        CONTAINER_NAME = "my-python-api"
        APP_PORT = "5000"   // Flask default port
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

        stage('Deploy Locally') {
            steps {
                script {
                    echo "🚀 Deploying container locally..."
                    
                    // Stop & remove old container if running
                    sh """
                        if [ \$(docker ps -q -f name=${CONTAINER_NAME}) ]; then
                            echo 'Stopping old container...'
                            docker stop ${CONTAINER_NAME}
                            docker rm ${CONTAINER_NAME}
                        fi
                    """

                    // Run the new container
                    sh """
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          -p 5000:5000 \
                          ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """

                    echo "✅ Application is running at http://localhost:5000"
                }
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
