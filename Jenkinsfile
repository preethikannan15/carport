pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                    echo "Installing Dependencies..."
                    sudo apt-get update
                    sudo apt-get install -y apache2 mysql-server php php-mysql unzip
                    sudo systemctl enable apache2 mysql
                    sudo systemctl start apache2 mysql
                    '''
                }
            }
        }

        stage('Clone Repository & Extract Files') {
            steps {
                script {
                    sh '''
                    echo "Cloning repository and extracting files..."
                    rm -rf /var/www/html/*
                    git clone https://github.com/preethikannan15/carport.git /tmp/carport
                    unzip /tmp/carport/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/
                    sudo chown -R www-data:www-data /var/www/html/
                    sudo chmod -R 755 /var/www/html/
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "Setting up MySQL Database..."
                    sudo mysql -e "DROP DATABASE IF EXISTS carrental; CREATE DATABASE carrental;"
                    sudo mysql carrental < /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/carrental.sql
                    echo "Database imported successfully!"
                    '''
                }
            }
        }

        stage('Restart Services & Configure Permissions') {
            steps {
                script {
                    sh '''
                    echo "Restarting services and configuring permissions..."
                    sudo systemctl restart apache2 mysql
                    sudo chmod -R 777 /var/www/html/
                    '''
                }
            }
        }

        stage('Deployment Complete') {
            steps {
                script {
                    echo "✅ Deployment Successful!"
                    sh '''
                    echo "🌐 Access your portal at: http://$(hostname -I | awk '{print $1}')"
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo "❌ Deployment Failed!"
        }
    }
}
