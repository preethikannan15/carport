pipeline {
    agent any

    stages {
        stage('Install Apache, MySQL, PHP') {
            steps {
                script {
                    sh '''
                    sudo apt-get update -y
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip
                    sudo systemctl enable apache2 mysql
                    sudo systemctl restart apache2 mysql
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                    sudo rm -rf /var/www/html/*
                    sudo git clone https://github.com/preethikannan15/carport.git /var/www/html/
                    '''
                }
            }
        }

        stage('Extract & Move Project') {
            steps {
                script {
                    sh '''
                    cd /var/www/html/
                    sudo unzip Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip
                    sudo mv Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/* .
                    sudo rm -rf Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    sudo systemctl restart mysql
                    echo "Creating database..."
                    sudo mysql -u root -e "DROP DATABASE IF EXISTS carrental;"
                    sudo mysql -u root -e "CREATE DATABASE carrental;"
                    echo "Importing database..."
                    sudo mysql -u root carrental < /var/www/html/carrental.sql
                    '''
                }
            }
        }

        stage('Set Permissions & Restart Services') {
            steps {
                script {
                    sh '''
                    sudo chown -R www-data:www-data /var/www/html/
                    sudo chmod -R 755 /var/www/html/
                    sudo systemctl restart apache2 mysql
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh '''
                    curl -Is http://localhost | head -n 1
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
            sh "sudo journalctl -xeu apache2 --no-pager || true"
            sh "sudo journalctl -xeu mysql --no-pager || true"
        }
    }
}
