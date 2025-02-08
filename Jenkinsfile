pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'b4e6f69a-632f-4e60-b4c1-1754bd6fdef7', url: 'https://github.com/preethikannan15/carport.git'
            }
        }

        stage('Extract Files') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "jenkins" | sudo -S apt-get update
                    echo "jenkins" | sudo -S apt-get install -y unzip
                    sudo mkdir -p /var/www/html/
                    sudo unzip -o Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/
                    '''
                }
            }
        }

        stage('Setup Database') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "jenkins" | sudo -S apt-get install -y mysql-client
                    mysql -u root -pubuntu -e "CREATE DATABASE IF NOT EXISTS carrental;"
                    mysql -u root -pubuntu carrental < "/var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL File/carrental.sql"
                    '''
                }
            }
        }

        stage('Configure Apache') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "jenkins" | sudo -S apt-get install -y apache2
                    sudo chown -R www-data:www-data /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    sudo chmod -R 755 /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    sudo systemctl restart apache2
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo "✅ Deployment completed successfully!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
