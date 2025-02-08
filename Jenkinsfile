pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/preethikannan15/carport.git'
            }
        }

        stage('Extract Files') {
            steps {
                sh '''
                sudo apt update && sudo apt install unzip -y || sudo yum install unzip -y
                sudo mkdir -p /var/www/html/
                sudo unzip -o Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/
                '''
            }
        }

        stage('Setup Database') {
            steps {
                sh '''
                sudo apt install mysql-client -y || sudo yum install mysql -y
                mysql -u root -pubuntu -e "CREATE DATABASE IF NOT EXISTS carrental;"
                mysql -u root -pubuntu carrental < /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL\ File/carrental.sql
                '''
            }
        }

        stage('Configure Apache') {
            steps {
                sh '''
                sudo systemctl restart apache2 || sudo systemctl restart httpd
                '''
            }
        }
    }
}
