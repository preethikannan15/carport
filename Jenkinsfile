pipeline {
    agent any

    stages {
        stage('Fix dpkg Issues') {
            steps {
                script {
                    sh '''
                    echo "jenkins" | sudo -S dpkg --configure -a || true
                    echo "jenkins" | sudo -S apt-get update --fix-missing
                    '''
                }
            }
        }

        stage('Install Dependencies & Extract Files') {
            steps {
                script {
                    sh '''
                    echo "jenkins" | sudo -S apt-get install -y unzip apache2 php libapache2-mod-php php-mysql mysql-server mysql-client
                    sudo mkdir -p /var/www/html/
                    sudo unzip -o Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/
                    '''
                }
            }
        }

        stage('Start MySQL & Import Database') {
            steps {
                script {
                    sh '''
                    echo "jenkins" | sudo -S systemctl start mysql
                    echo "jenkins" | sudo -S systemctl enable mysql
                    sleep 5

                    sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';"
                    sudo mysql -e "FLUSH PRIVILEGES;"
                    mysql -u root -e "CREATE DATABASE IF NOT EXISTS carrental;"
                    mysql -u root carrental < "/var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL File/carrental.sql"
                    '''
                }
            }
        }

        stage('Restart Apache & Permissions') {
            steps {
                script {
                    sh '''
                    sudo chown -R www-data:www-data /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    sudo chmod -R 755 /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    sudo systemctl restart apache2
                    sudo systemctl enable apache2
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment Successful!"
            script {
                sh '''
                echo "🌐 Access your portal at: http://$(curl -s ifconfig.me)"
                '''
            }
        }
        failure {
            echo "❌ Deployment Failed!"
        }
    }
}
