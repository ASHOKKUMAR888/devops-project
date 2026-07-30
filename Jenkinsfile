pipeline {

    agent {
        label 'ubuntu'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Getting application code'
            }
        }


        stage('Test Application') {
            steps {
                sh '''
                cd app
                python3 -m pip install -r requirements.txt --break-system-packages
                python3 app.py &
                sleep 5
                curl localhost:5000
                '''
            }
        }


        stage('Build Docker Image') {
            steps {
                sh '''
                cd app
                docker build -t devops-app:v2 .
                '''
            }
        }


        stage('Deploy Kubernetes') {
            steps {
                sh '''
                kubectl apply -f k8s/
                '''
            }
        }


        stage('Verify Deployment') {
            steps {
                sh '''
                kubectl get pods
                kubectl get services
                '''
            }
        }

    }
}
