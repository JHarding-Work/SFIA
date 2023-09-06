pipeline{
        agent any
        stages{
            stage('Installation'){
                steps{
                    sh "sudo apt install -y python3"
                    sh "sudo apt install -y python3-pip"
                    sh "pip install -r requirements.txt"
                }
            }
            stage('Run tests'){
                steps{
                    sh "python3 -m pytest --cov app --cov-report html"
                }
            }
        }
}