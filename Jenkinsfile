pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: '94cf9629-e7de-4dc1-9be6-8f3c17b759ab', url: 'https://github.com/preethikannan15/carport.git'
            }
        }

        stage('Extract Files') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "jenkins" | sudo -S apt-get update
                    
                    # Fix any interrupted dpkg process before installation
                    sudo dpkg --configure -a || true
                    sudo apt-get install -f || true
                    
                    echo "jenkins" | sudo -S apt-get install -y unzip
                    
                    # Ensure directory exists and extract files
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
                    echo "jenkins" | sudo -S apt-get install -y mysql-server mysql-client
                    
                    # Ensure MySQL is running
                    echo "jenkins" | sudo -S systemctl start mysql || sudo systemctl restart mysql
                    echo "jenkins" | sudo -S systemctl enable mysql
                    sleep 10  # Give MySQL time to start

                    # Create and import database
                    mysql -u root -e "CREATE DATABASE IF NOT EXISTS carrental;"
                    mysql -u root carrental < "/var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL File/carrental.sql"
                    '''
                }
            }
        }

        stage('Configure Apache') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "jenkins" | sudo -S apt-get install -y apache2
                    sudo chown -R www-data:www-data /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    sudo chmod -R 755 /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    sudo systemctl restart apache2
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo "✅ Deployment completed successfully!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
