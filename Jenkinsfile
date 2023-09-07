pipeline{
        agent any
        environment{
            SECRET_KEY=credentials('SECRET_KEY')
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
                    sh 'sudo docker-compose up -d'
                }
            }
        }
}