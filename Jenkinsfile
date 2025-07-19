pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'yashtnaik/calotracker'
        IMAGE_TAG = 'v1'
        DOCKERHUB_CREDENTIALS = credentials('DockerHub') // DockerHub credentials ID
        GIT_CREDENTIALS = credentials('GitHub') // GitHub credentials ID
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yashtnaik/calotracker.git'
            }
        }

        stage('Build with Docker Compose') {
            steps {
                sh "sudo docker compose build"
                sh "sudo docker tag calotracker ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh """
                    echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                    docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                """
            }
        }

        stage('Update deployment.yaml') {
            steps {
                sh """
                    sed -i 's|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${IMAGE_TAG}|' manifest/deployment.yaml
                    git config user.name "jenkins"
                    git config user.email "jenkins@local"
                    git add manifest/deployment.yaml
                    git commit -m "Update image tag to ${IMAGE_TAG}"
                    git push https://${GIT_CREDENTIALS_USR}:${GIT_CREDENTIALS_PSW}@github.com/yashtnaik/calotracker.git HEAD:main
                """
            }
        }
    }
}
