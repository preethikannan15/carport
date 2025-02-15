pipeline {
    agent any

    environment {
        DEBIAN_FRONTEND = "noninteractive"
        HEARTBEAT_CHECK_INTERVAL = "86400"
    }

    stages {
        stage('Fix dpkg Issues') {
            steps {
                script {
                    sh '''
                    echo "🔧 Fixing dpkg lock issues..."
                    sudo rm -rf /var/lib/dpkg/lock /var/lib/dpkg/lock-frontend
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
                    echo "🔄 Updating system packages..."
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
                    echo "📦 Installing Apache, MySQL, PHP..."
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip git
                    sudo systemctl enable apache2
                    sudo systemctl enable mysql
                    '''
                }
            }
        }

        stage('Check Service Status') {
            steps {
                script {
                    sh '''
                    echo "🛠 Checking if Apache and MySQL are installed correctly..."
                    apache2 -v || { echo "❌ Apache is not installed properly!"; exit 1; }
                    mysql --version || { echo "❌ MySQL is not installed properly!"; exit 1; }
                    '''
                }
            }
        }

        stage('Start Services') {
            steps {
                script {
                    sh '''
                    echo "🚀 Starting Apache and MySQL..."
                    sudo systemctl restart apache2 || { echo "❌ Apache failed to start!"; exit 1; }
                    sudo systemctl restart mysql || { echo "❌ MySQL failed to start!"; exit 1; }
                    sleep 5
                    sudo systemctl status apache2 || { echo "⚠️ Apache service status check failed!"; exit 1; }
                    sudo systemctl status mysql || { echo "⚠️ MySQL service status check failed!"; exit 1; }
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                    echo "📂 Cloning Car Rental Portal repository..."
                    sudo rm -rf /var/www/html/carport
                    git clone https://github.com/preethikannan15/carport.git /var/www/html/carport || { echo "⚠️ Git clone failed!"; exit 1; }
                    '''
                }
            }
        }

        stage('Extract Project') {
            steps {
                script {
                    sh '''
                    echo "🗄 Extracting Car Rental Portal..."
                    sudo unzip /var/www/html/carport/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/ || { echo "⚠️ Extraction failed!"; exit 1; }
                    sudo chmod -R 755 /var/www/html
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "🛠 Setting up MySQL database..."
                    sudo mysql -e "CREATE DATABASE IF NOT EXISTS carrental;" || { echo "❌ MySQL Database creation failed!"; exit 1; }
                    sudo mysql -e "CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin123';" || { echo "❌ MySQL User creation failed!"; exit 1; }
                    sudo mysql -e "GRANT ALL PRIVILEGES ON carrental.* TO 'admin'@'localhost';" || { echo "❌ MySQL Granting privileges failed!"; exit 1; }
                    sudo mysql -e "FLUSH PRIVILEGES;" || { echo "❌ MySQL flush privileges failed!"; exit 1; }
                    sudo mysql carrental < /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/carrental.sql || { echo "⚠️ MySQL Import failed!"; exit 1; }
                    '''
                }
            }
        }

        stage('Restart Services') {
            steps {
                script {
                    sh '''
                    echo "🔄 Restarting Apache and MySQL..."
                    sudo systemctl restart apache2 || { echo "❌ Apache restart failed!"; exit 1; }
                    sudo systemctl restart mysql || { echo "❌ MySQL restart failed!"; exit 1; }
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh '''
                    echo "🔍 Verifying deployment..."
                    curl -Is http://localhost | head -n 1 || { echo "❌ Deployment verification failed!"; exit 1; }
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "📜 Gathering logs..."
            sh 'sudo journalctl -xeu apache2 --no-pager || true'
            sh 'sudo journalctl -xeu mysql --no-pager || true'
        }

        success {
            echo "✅ Deployment successful!"
        }

        failure {
            echo "❌ Deployment failed! Check logs above."
        }
    }
}
