pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/preethikannan15/carport.git'  // Replace with your actual repo
            }
        }

        stage('Extract Files') {
            steps {
                sh 'unzip -o Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/'
                sh 'sudo chown -R www-data:www-data /var/www/html/'
                sh 'sudo chmod -R 755 /var/www/html/'
            }
        }

        stage('Setup Database') {
            steps {
                sh '''
                sudo mysql -e "CREATE DATABASE IF NOT EXISTS carrental;"
                sudo mysql carrental < /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL\\ File/carrental.sql
                '''
            }
        }

        stage('Configure Apache') {
            steps {
                sh '''
                echo "<VirtualHost *:80>
                DocumentRoot /var/www/html
                <Directory /var/www/html>
                    AllowOverride All
                    Require all granted
                </Directory>
                </VirtualHost>" | sudo tee /etc/apache2/sites-available/000-default.conf
                sudo systemctl restart apache2
                '''
            }
        }
    }
}
