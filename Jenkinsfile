pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                    sudo apt-get update -y
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip
                    sudo systemctl enable apache2
                    sudo systemctl enable mysql
                    sudo systemctl restart apache2
                    sudo systemctl restart mysql
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                    sudo rm -rf /var/www/html/*
                    git clone https://github.com/preethikannan15/carport.git /tmp/carport
                    '''
                }
            }
        }

        stage('Extract & Move Project') {
            steps {
                script {
                    sh '''
                    sudo unzip /tmp/carport/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /tmp/carport/
                    sudo mv /tmp/carport/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/* /var/www/html/
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
                    sudo mysql -e "CREATE DATABASE IF NOT EXISTS carrental;"
                    sudo mysql carrental < /var/www/html/carrental.sql
                    sudo systemctl restart mysql
                    '''
                }
            }
        }

        stage('Restart & Verify') {
            steps {
                script {
                    sh '''
                    sudo systemctl restart apache2
                    curl -I http://localhost || echo "Deployment Failed!"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment Successful! Access the site via server IP."
        }
        failure {
            echo "❌ Deployment Failed! Check logs."
            sh 'sudo journalctl -xeu apache2 --no-pager || true'
            sh 'sudo journalctl -xeu mysql --no-pager || true'
        }
    }
}
