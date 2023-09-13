pipeline{
        agent any
        environment{
            SECRETS_FILE=credentials('SECRETS_FILE')
        }
        stages{
            stage('Installation'){
                steps{
                    sh 'sudo apt install -y python3'
                    sh 'sudo apt install -y python3-pip'
                    sh 'pip install -r requirements.txt'
                }
            }
            stage('Run tests'){
                steps{
                    sh 'python3 -m pytest --cov app --cov-report html'
                }
            }
            stage('Build Application'){
                steps{
                    script{
                        image = docker.build("hubaccount12546/sfia")
                    }
                }
            }
            stage('Tag & Push Image'){
                steps{
                    script{
                        docker.withRegistry('https://registry.hub.docker.com', 'DOCKER_HUB_CREDENTIALS'){
                            image.push("latest")
                        }
                    }
                }
            }
            stage('Deploy Server'){
                steps{
                    sh 'docker-compose down'
                    sh 'docker-compose --env-file $SECRETS_FILE up -d'
                }
            }
        }
}