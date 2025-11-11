pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        KUBECONFIG = 'C:\\ProgramData\\Jenkins\\.kube\\config'
        MINIKUBE_PROFILE = 'minikube'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/jinanmokdad/Movie-App.git'
            }
        }

        stage('Ensure Minikube is Running') {
            steps {
                bat '''
                echo Checking Minikube status...
                minikube status || minikube start --driver=docker
                '''
            }
        }

        stage('Build in Minikube Docker') {
            steps {
                bat '''
                echo Setting Docker environment to Minikube...
                call minikube docker-env --shell=cmd > docker_env.bat
                call docker_env.bat
                echo Building Docker image inside Minikube...
                docker build -t mydjangoapp:latest .
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                bat '''
                echo Deploying Django app to Minikube...
                minikube -p %MINIKUBE_PROFILE% kubectl -- apply -f deployment.yaml --validate=false
                minikube -p %MINIKUBE_PROFILE% kubectl -- apply -f service.yaml --validate=false

                echo Checking rollout status...
                minikube -p %MINIKUBE_PROFILE% kubectl -- rollout status deployment django-deployment

                echo Getting service URL...
                minikube -p %MINIKUBE_PROFILE% service django-service --url
                '''
            }
        }
    }
}
