pipeline {
    agent any

    environment {
        DB_NAME = "carrental"
        DB_USER = "root"
        DB_PASSWORD = "ubuntu"
        WEB_DIR = "/var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0"
        SQL_FILE = "/var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL File/carrental.sql"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'your-github-credentials', url: 'https://github.com/preethikannan15/carport.git'
            }
        }

        stage('Extract Files') {
            steps {
                script {
                    sh '''
                    set -e
                    sudo apt-get update
                    sudo apt-get install -y unzip
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
                    export DEBIAN_FRONTEND=noninteractive
                    sudo apt-get update
                    sudo apt-get install -y mysql-server mysql-client
                    
                    # Start and enable MySQL
                    sudo systemctl start mysql
                    sudo systemctl enable mysql

                    # Create database and import data
                    echo "CREATE DATABASE IF NOT EXISTS ${DB_NAME};" | mysql -u ${DB_USER} -p${DB_PASSWORD} -h 127.0.0.1
                    mysql -u ${DB_USER} -p${DB_PASSWORD} -h 127.0.0.1 ${DB_NAME} < "${SQL_FILE}"
                    '''
                }
            }
        }

        stage('Configure Apache') {
            steps {
                script {
                    sh '''
                    set -e
                    sudo apt-get install -y apache2 php libapache2-mod-php php-mysql
                    sudo chown -R www-data:www-data ${WEB_DIR}
                    sudo chmod -R 755 ${WEB_DIR}
                    sudo systemctl restart apache2
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo "🚀 Deployment completed successfully!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
