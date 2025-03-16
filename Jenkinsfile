pipeline{
    agent any

    stages{
        stage('cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github to Jenkins'
                    checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/jothsnapraveena/MLOPS_Hotel_Reservation']])
                }
            }
        }
    }
}