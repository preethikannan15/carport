pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'a008eebd-aa08-4387-808f-66c4cd2d2b1c', url: 'https://github.com/preethikannan15/carport.git'
            }
        }

        stage('Extract Files') {
            steps {
                script {
                    sh '''
                    set -e
                    echo "jenkins" | sudo -S apt-get update
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
                    echo "jenkins" | sudo -S systemctl start mysql
                    echo "jenkins" | sudo -S systemctl enable mysql
                    sleep 10  # Allow MySQL to initialize
                    
                    # Check if MySQL is running before proceeding
                    if ! systemctl is-active --quiet mysql; then
                        echo "❌ MySQL failed to start!"
                        exit 1
                    fi
                    
                    # Create database and import data
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
                    
                    # Set permissions and restart Apache
                    sudo chown -R www-data:www-data /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    sudo chmod -R 755 /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    sudo systemctl restart apache2
                    
                    # Check if Apache is running
                    if ! systemctl is-active --quiet apache2; then
                        echo "❌ Apache failed to start!"
                        exit 1
                    fi
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
            echo "❌ Deployment failed! Check logs for errors."
        }
    }
}
