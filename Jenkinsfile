pipeline{
    agent any
    environment {
        VENV_DIR = 'venv'
    }

    stages{
        stage('cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github to Jenkins'
                    checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/jothsnapraveena/MLOPS_Hotel_Reservation']])
                }
            }
        stage('Setting up Virtual Environment and Installing dependies'){
            steps{
                script{
                    echo 'Setting up Virtual Environment and Installing dependies'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --pugrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}