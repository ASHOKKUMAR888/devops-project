pipeline {

    agent {
        label 'linux'
    }


    environment {

        APP_NAME = "devops-app"

        IMAGE_TAG = "${BUILD_NUMBER}"

        APP_PATH = "app"

        K8S_PATH = "k8s"

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

                echo "Application files"

                ls -la

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
                -o image.tar



                echo "Importing Image Into Kind"



                docker exec -i ${KIND_NODE} \
                ctr -n k8s.io images import - < image.tar



                echo "Checking Image"



                docker exec ${KIND_NODE} \
                ctr -n k8s.io images ls | grep ${APP_NAME}

                '''
            }
        }





        stage('Deploy To Kubernetes') {

            steps {

                sh '''

                cd ${K8S_PATH}



                echo "Applying Kubernetes YAML"



                kubectl apply -f app-deployment.yaml

                kubectl apply -f app-service.yaml




                echo "Updating Deployment Image"



                kubectl set image deployment/${APP_NAME} \
                ${APP_NAME}=${APP_NAME}:${IMAGE_TAG}




                echo "Waiting For Rollout"



                kubectl rollout status deployment/${APP_NAME} \
                --timeout=180s


                '''
            }
        }





        stage('Application Verification') {

            steps {

                sh '''

                echo "Pods"

                kubectl get pods



                echo "Services"

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

            '''

        }



        always {

            echo "Pipeline Completed"

        }

    }

}
