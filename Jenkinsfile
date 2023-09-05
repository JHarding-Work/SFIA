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
                    sh "echo 'this will run the tests'"
                }
            }
        }
}