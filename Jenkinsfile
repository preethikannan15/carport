pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'your-github-credentials', url: 'https://github.com/preethikannan15/carport.git'
            }
        }

        stage('Extract Files') {
            steps {
                script {
                    sh '''
                    set -e
                    sudo apt-get update
                    sudo apt-get install -y unzip
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
            export DEBIAN_FRONTEND=noninteractive
            
            # Update and install MySQL
            sudo apt-get update
            sudo apt-get install -y mysql-server mysql-client || sudo apt-get -f install -y
            
            # Ensure MySQL is running
            sudo systemctl restart mysql
            sudo systemctl enable mysql

            # Create database
            sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS carrental;"
            
            # Import SQL file
            sudo mysql -u root carrental < "/var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/SQL File/carrental.sql"
            '''
        }
    }
}


        stage('Configure Apache') {
            steps {
                script {
                    sh '''
                    set -e
                    sudo apt-get install -y apache2
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
            echo "Deployment completed successfully!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
  
