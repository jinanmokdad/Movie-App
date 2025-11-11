pipeline {
    agent any
    triggers {
        pollSCM('H/2 * * * *')
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/jinanmokdad/Movie-App.git'
            }
        }
        stage('Build in Minikube Docker') {
            steps {
                bat '''
                call minikube docker-env --shell=cmd > docker_env.bat
                call docker_env.bat
                docker build -t mydjangoapp:latest .
                '''
            }
        }
        stage('Deploy to Minikube') {
            steps {
                bat '''
                minikube -p %MINIKUBE_PROFILE% kubectl -- apply -f deployment.yaml --validate=false
                minikube -p %MINIKUBE_PROFILE% kubectl -- apply -f service.yaml --validate=false
                minikube -p %MINIKUBE_PROFILE% kubectl -- rollout history deployment django-deployment
                minikube -p %MINIKUBE_PROFILE% kubectl -- rollout status deployment django-deployment
                '''
            }
        }
    }
}
