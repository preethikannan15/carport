pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                    sudo apt-get update
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip
                    sudo systemctl enable apache2
                    sudo systemctl enable mysql
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
                    '''
                }
            }
        }

        stage('Set Permissions & Restart Services') {
            steps {
                script {
                    sh '''
                    sudo chmod -R 755 /var/www/html/
                    sudo chown -R www-data:www-data /var/www/html/
                    sudo systemctl restart apache2
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
            echo "✅ Deployment Successful!"
        }
        failure {
            echo "❌ Deployment Failed! Checking logs..."
            sh "sudo journalctl -xeu apache2 --no-pager"
            sh "sudo journalctl -xeu mysql --no-pager"
        }
    }
}
