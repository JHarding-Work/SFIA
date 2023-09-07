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
            stage('Deploy Development Server'){
                steps{
                    sh 'sudo docker-compose down'
                    sh 'ls /home/jenkins'
                    sh 'ls /home/jenkins/.jenkins'
                    sh 'ls /home/jenkins/.jenkins/workspace'
                    sh "sudo docker-compose --env-file $SECRETS_FILE up -d"
                }
            }
        }
}