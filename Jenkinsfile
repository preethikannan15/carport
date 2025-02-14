pipeline {
    agent any

    environment {
        DEBIAN_FRONTEND = "noninteractive"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                    sudo apt-get update -y
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip git
                    
                    sudo systemctl enable --now apache2
                    sudo systemctl enable --now mysql
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                    sudo rm -rf /var/www/html/*
                    sudo git clone https://github.com/preethikannan15/carport.git /var/www/html
                    '''
                }
            }
        }

        stage('Extract Project') {
            steps {
                script {
                    sh '''
                    sudo unzip -o /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html
                    sudo chown -R www-data:www-data /var/www/html
                    sudo chmod -R 755 /var/www/html
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
                    '''
                }
            }
        }

        stage('Restart Services') {
            steps {
                script {
                    sh '''
                    sudo systemctl restart apache2
                    sudo systemctl restart mysql
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh '''
                    curl -I http://localhost | grep "200 OK"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful! Access your portal via the server's IP."
        }
        failure {
            echo "❌ Deployment failed! Check logs for errors."
            sh 'sudo journalctl -xeu apache2 --no-pager'
            sh 'sudo journalctl -xeu mysql --no-pager'
        }
    }
}
