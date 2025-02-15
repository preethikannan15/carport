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
                    sudo rm -rf /var/lib/dpkg/lock
                    sudo rm -rf /var/lib/dpkg/lock-frontend
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
                    echo "Updating system packages..."
                    sudo apt-get update -y
                    sudo apt-get upgrade -y
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
                    sudo systemctl enable apache2
                    sudo systemctl enable mysql
                    '''
                }
            }
        }

        stage('Start Services') {
            steps {
                script {
                    sh '''
                    echo "Starting Apache and MySQL..."
                    sudo systemctl start apache2
                    sudo systemctl start mysql
                    sudo systemctl restart apache2
                    sudo systemctl restart mysql
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                    echo "Cloning Car Rental Portal repository..."
                    sudo rm -rf /var/www/html/carport
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
                    sudo mysql -e "CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin123';"
                    sudo mysql -e "GRANT ALL PRIVILEGES ON carrental.* TO 'admin'@'localhost';"
                    sudo mysql -e "FLUSH PRIVILEGES;"
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
            sh 'sudo journalctl -xeu apache2 --no-pager || true'
            sh 'sudo journalctl -xeu mysql --no-pager || true'
        }
    }
}
