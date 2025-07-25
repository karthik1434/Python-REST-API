pipeline {
  agent any

  triggers {
    pollSCM('* * * * *') // Poll SCM every minute
  }

  environment {
    DOCKER_IMAGE    = "duggana1994/my-python-api-build-by-jenkins"
    DOCKER_TAG      = "latest"
    CONTAINER_NAME  = "my-python-api"
    APP_PORT        = "5000"
    DEPLOYMENT      = "my-python-api" // Kubernetes deployment name
    IMAGE           = "${DOCKER_IMAGE}:${DOCKER_TAG}"
  }

  options {
    buildDiscarder(logRotator(numToKeepStr: '3'))
    timeout(time: 30, unit: 'MINUTES')
  }

  stages {
    stage('Prepare Workspace') {
      steps {
        cleanWs()
      }
    }

    stage('Checkout') {
      steps {
        retry(3) {
          git branch: 'main',
              url: 'https://github.com/karthik1434/Python-REST-API.git'
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t ${IMAGE} .'
      }
    }

    stage('Login to Docker Hub') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'dockerhub-creds',
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS'
        )]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
          '''
        }
      }
    }

    stage('Push Image to Docker Hub') {
      steps {
        sh 'docker push ${IMAGE}'
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withKubeConfig(credentialsId: 'minikube-kubeconfig') {
          sh """
            kubectl set image deployment/${DEPLOYMENT} \\
              ${CONTAINER_NAME}=${IMAGE} --record || \\
            kubectl apply -f k8s/deployment.yaml
          """
        }
      }
    }
  }

  post {
    success {
      echo "✅ Build, push, and deployment successful!"
    }
    failure {
      echo "❌ Build or deployment failed — check logs!"
    }
    always {
      cleanWs()
    }
  }
}
