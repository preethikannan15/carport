pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: '7013989d-e8b0-4571-8336-15f6d89b0b9b', url: 'https://github.com/preethikannan15/carport.git', branch: 'main'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
            }
        }
    }
}
