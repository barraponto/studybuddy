pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/barraponto/studybuddy.git']])
            }
        }
        stage('Build') {
            steps {
                script {
                    image = docker.build "ludologico/studybuddy:latest"
                }
            }
        }
        stage('Publish') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-token') {
                        image.push("latest")
                    }
                }
            }
        }
    }
}
