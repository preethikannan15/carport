pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: '9e1e0fb1-cf03-45ff-b9f8-225ab7f3feab', url: 'https://github.com/preethikannan15/carport.git'
            }
        }

        stage('Extract Files') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "jenkins" | sudo -S apt-get update
                    echo "jenkins" | sudo -S apt-get install -y unzip
                    sudo mkdir -p /var/www/html/
                    sudo unzip -o Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/
                    '''
                }
            }
        }

        stage('Install MySQL & Import Database') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "jenkins" | sudo -S apt-get install -y mysql-server mysql-client
                    echo "jenkins" | sudo -S systemctl start mysql
                    echo "jenkins" | sudo -S systemctl enable mysql
                    sleep 10  # Wait for MySQL to fully start

                    # Secure MySQL installation (disable root password prompt)
                    sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';"
                    sudo mysql -e "FLUSH PRIVILEGES;"

                    # Create database and import SQL file
                    mysql -u root -e "CREATE DATABASE IF NOT EXISTS carrental;"
                    mysql -u root carrental < "/var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL File/carrental.sql"
                    '''
                }
            }
        }

        stage('Install Apache & Configure Permissions') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "jenkins" | sudo -S apt-get install -y apache2 php libapache2-mod-php php-mysql
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
            echo "✅ Deployment completed successfully!"
            script {
                sh '''
                echo "🌐 Access your portal at: http://$(curl -s ifconfig.me)"
                '''
            }
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
