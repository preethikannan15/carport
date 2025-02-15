pipeline {
    agent any

    environment {
        DEBIAN_FRONTEND = "noninteractive"
    }

    stages {
        stage('Fix dpkg Issues') {
            steps {
                script {
                    sh '''
                    echo "Fixing dpkg lock issues..."
                    sudo dpkg --configure -a || true
                    sudo apt-get install -f -y || true
                    '''
                }
            }
        }

        stage('Update System') {
            steps {
                script {
                    sh '''
                    echo "Updating packages..."
                    sudo apt-get update -y
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                    echo "Installing Apache, MySQL, PHP..."
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip git || true
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                    echo "Cloning Car Rental Portal repository..."
                    git clone https://github.com/preethikannan15/carport.git /var/www/html/carport || true
                    '''
                }
            }
        }

        stage('Extract Project') {
            steps {
                script {
                    sh '''
                    echo "Extracting Car Rental Portal..."
                    sudo unzip /var/www/html/carport/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/ || true
                    sudo chmod -R 755 /var/www/html
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "Setting up MySQL database..."
                    sudo mysql -e "CREATE DATABASE IF NOT EXISTS carrental;"
                    sudo mysql carrental < /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/carrental.sql
                    '''
                }
            }
        }

        stage('Restart Services') {
            steps {
                script {
                    sh '''
                    echo "Restarting Apache and MySQL..."
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
                    echo "Verifying deployment..."
                    curl -Is http://localhost | head -n 1
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed! Gathering logs..."
            sh 'sudo journalctl -xeu apache2 --no-pager'
            sh 'sudo journalctl -xeu mysql --no-pager'
        }
    }
}
