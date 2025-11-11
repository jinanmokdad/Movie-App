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
                minikube status -p %MINIKUBE_PROFILE% || minikube start -p %MINIKUBE_PROFILE% --driver=docker
                '''
            }
        }

        stage('Build in Minikube Docker') {
            steps {
                bat '''
                echo Setting Docker environment to Minikube...
                call minikube -p %MINIKUBE_PROFILE% docker-env --shell=cmd > docker_env.bat
                call docker_env.bat

                echo Building Docker image inside Minikube...
                docker build -t my-django-app:latest .
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                bat '''
                echo Deploying Django app to Minikube...
                minikube -p %MINIKUBE_PROFILE% kubectl apply -f deployment.yaml --validate=false
                minikube -p %MINIKUBE_PROFILE% kubectl apply -f service.yaml --validate=false

                minikube -p %MINIKUBE_PROFILE% kubectl rollout restart deployment django-deployment

                echo Waiting for deployment rollout...
                minikube -p %MINIKUBE_PROFILE% kubectl rollout status deployment django-deployment
                '''
            }
        }

        stage('Get Service URL') {
            steps {
                bat '''
                echo Getting Minikube service URL...

                REM Get the NodePort of the service
                for /f "tokens=*" %%i in ('minikube -p %MINIKUBE_PROFILE% kubectl -- get service django-service --output=jsonpath^="{.spec.ports[0].nodePort}"') do set NODE_PORT=%%i

                REM Get Minikube IP
                for /f "tokens=*" %%i in ('minikube -p %MINIKUBE_PROFILE% ip') do set MINIKUBE_IP=%%i

                REM Construct full URL
                set SERVICE_URL=http://%MINIKUBE_IP%:%NODE_PORT%
                echo  Django app is running at %SERVICE_URL%

                for /f "tokens=*" %%i in ('minikube -p %MINIKUBE_PROFILE% service django-service --url --format="{{.URL}}"') do set SERVICE_URL=%%i
                echo  Django app is running at %SERVICE_URL%

                REM Get the host-accessible URL for the service
                for /f "tokens=*" %%i in ('minikube -p %MINIKUBE_PROFILE% service django-service --url --format="{{.URL}}"') do set SERVICE_URL=%%i
                echo  Django app is running at %SERVICE_URL%

                

                '''
            }
        }

    }
}
