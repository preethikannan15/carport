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
stage('Extract Files') {
    steps {
        script {
            sh '''
            set -e
            export DEBIAN_FRONTEND=noninteractive
            
            # Fix dpkg issues if needed
            sudo dpkg --configure -a || echo "No dpkg issues found."

            # Update package list
            sudo apt-get update

            # Install required packages
            sudo apt-get install -y unzip || sudo apt-get -f install -y

            # Extract the zip file
            unzip -o Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/
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
  
