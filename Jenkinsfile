pipeline {
    agent any

    environment {
        DEBIAN_FRONTEND = "noninteractive"  // Prevents interactive debconf issues
    }

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
                    
                    # Fix dpkg errors before installation
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
                    
                    # Restart MySQL properly
                    echo "jenkins" | sudo -S systemctl restart mysql
                    echo "jenkins" | sudo -S systemctl enable mysql
                    sleep 10  # Wait for MySQL to start

                    # Create and import database
                    echo "Creating Database..."
                    mysql -u root -e "CREATE DATABASE IF NOT EXISTS carrental;"

                    echo "Importing SQL File..."
                    mysql -u root carrental < "/var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL File/carrental.sql"

                    echo "Database Setup Complete!"
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
            echo "🌐 Access your portal at: http://$(curl -s ifconfig.me)"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
