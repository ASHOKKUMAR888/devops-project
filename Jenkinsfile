pipeline {

    agent {
        label 'linux'
    }

    environment {
        APP_NAME = "devops-app"
        IMAGE_TAG = "latest"
        APP_PATH = "/home/ashokkumarbr/devops-project/app"
        K8S_PATH = "/home/ashokkumarbr/devops-project/k8s"
        KIND_NODE = "devops-control-plane"
    }

    stages {

        stage('Test Jenkins Agent') {
            steps {
                echo "Jenkins agent is working!"

                sh '''
                hostname
                whoami
                '''
            }
        }


        stage('Check Tools') {
            steps {
                sh '''
                echo "Checking Docker"
                docker --version

                echo "Checking Kubernetes"
                kubectl version --client

                echo "Checking Ansible"
                ansible --version
                '''
            }
        }


        stage('Check Kubernetes Cluster') {
            steps {
                sh '''
                echo "Checking Kubernetes Nodes"
                kubectl get nodes
                '''
            }
        }


        stage('Application Test') {
            steps {
                sh '''
                cd ${APP_PATH}

                echo "Application files:"
                ls -la

                echo "Python version:"
                python3 --version
                '''
            }
        }


        stage('Build Docker Image') {
            steps {
                sh '''
                cd ${APP_PATH}

                echo "Building Docker Image"

                docker build \
                -t ${APP_NAME}:${IMAGE_TAG} .

                echo "Docker Images"

                docker images | grep ${APP_NAME}
                '''
            }
        }


        stage('Load Image Into Kubernetes') {
            steps {
                sh '''
                echo "Saving Docker Image"

                docker save ${APP_NAME}:${IMAGE_TAG} \
                -o ${APP_NAME}.tar


                echo "Loading image into Kind Kubernetes"

                docker exec -i ${KIND_NODE} \
                ctr -n k8s.io images import \
                < ${APP_NAME}.tar


                echo "Checking image inside Kind"

                docker exec ${KIND_NODE} \
                ctr -n k8s.io images ls | grep ${APP_NAME}
                '''
            }
        }


        stage('Deploy To Kubernetes') {
            steps {
                sh '''
                cd ${K8S_PATH}


                echo "Applying Kubernetes files"

                kubectl apply -f app-deployment.yaml
                kubectl apply -f app-service.yaml


                echo "Updating Deployment Image"

                kubectl set image deployment/${APP_NAME} \
                ${APP_NAME}=${APP_NAME}:${IMAGE_TAG}


                echo "Waiting for Rollout"

                kubectl rollout status deployment/${APP_NAME} \
                --timeout=180s
                '''
            }
        }


        stage('Application Verification') {
            steps {
                sh '''
                echo "Checking Pods"

                kubectl get pods


                echo "Checking Services"

                kubectl get svc
                '''
            }
        }
    }


    post {

        success {
            echo "Deployment Successful 🚀"
        }


        failure {
            echo "Deployment Failed ❌"

            sh '''
            kubectl get pods
            kubectl describe pods
            '''
        }


        always {
            echo "Pipeline Completed"
        }
    }
}
