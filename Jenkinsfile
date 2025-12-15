pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = '1'
        MINIKUBE_URL = credentials('minikube-url')
    }

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
        stage('Deploy') {
            steps {
                script {
                    withCredentials(usernamePassword(credentialsId: 'argocd-admin', usernameVariable: 'ARGOCD_USERNAME', passwordVariable: 'ARGOCD_PASSWORD')) {
                        kubeconfig(credentialsId: 'kubeconfig', serverUrl: env.MINIKUBE_URL) {
                            sh '''
                            argocd login argocd.ludologico.com.br:8000 --insecure --username $ARGOCD_USERNAME --password $ARGOCD_PASSWORD
                            argocd app sync studybuddy
                            '''
                        }
                    }
                }
            }
        }
    }
}
