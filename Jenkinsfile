pipeline {
    agent any

    environment {
        IMAGE_NAME = "yashtnaik/calotracker"
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'GitHub', url: 'https://github.com/yashtnaik/calotracker.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    def tag = "Jenkins"
                    sh "docker tag calotracker_web ${env.IMAGE_NAME}:${tag}"
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'DockerHub', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh '''
                        echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Docker image pushed successfully to DockerHub."
        }
        failure {
            echo "❌ Pipeline failed."
        }
    }
}
