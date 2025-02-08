pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/preethikannan15/carport.git'
            }
        }
        stage('Extract Files') {
            steps {
                sh '''
                sudo apt update && sudo apt install unzip mysql-client -y || sudo yum install unzip mysql -y
                sudo mkdir -p /var/www/html/
                sudo unzip Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/
                '''
            }
        }
        stage('Setup Database') {
            steps {
                sh '''
                mysql -u root -p'ubuntu' -e "CREATE DATABASE IF NOT EXISTS carrental;"
                mysql -u root -p'ubuntu' carrental < /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL\ File/carrental.sql
                '''
            }
        }
        stage('Configure Apache') {
            steps {
                sh '''
                sudo chown -R www-data:www-data /var/www/html/
                sudo chmod -R 755 /var/www/html/
                sudo systemctl restart apache2
                '''
            }
        }
    }
}

