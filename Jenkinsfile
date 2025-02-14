pipeline {
    agent any

    stages {
        stage('Fix dpkg & Install Dependencies') {
            steps {
                script {
                    sh '''
                    echo "🔧 Fixing dpkg issues..."
                    sudo dpkg --configure -a || true
                    sudo apt-get update -y
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip curl git || exit 1
                    
                    echo "🔄 Enabling and Restarting Services..."
                    sudo systemctl enable apache2 mysql
                    sudo systemctl restart apache2 mysql
                    '''
                }
            }
        }

        stage('Verify Apache & MySQL') {
            steps {
                script {
                    sh '''
                    echo "✅ Checking Apache and MySQL status..."
                    sudo systemctl is-active --quiet apache2 || (echo "❌ Apache failed to start!" && exit 1)
                    sudo systemctl is-active --quiet mysql || (echo "❌ MySQL failed to start!" && exit 1)
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                    echo "🌍 Cloning repository..."
                    sudo rm -rf /var/www/html/*
                    sudo git clone https://github.com/preethikannan15/carport.git /var/www/html/ || exit 1
                    '''
                }
            }
        }

        stage('Extract & Move Project') {
            steps {
                script {
                    sh '''
                    echo "📦 Extracting and moving project files..."
                    cd /var/www/html/
                    sudo unzip Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip || exit 1
                    sudo mv Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/* .
                    sudo rm -rf Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "🗄️ Setting up MySQL database..."
                    sudo systemctl restart mysql
                    sleep 5  # Ensure MySQL is fully up

                    sudo mysql -u root -e "DROP DATABASE IF EXISTS carrental;" || exit 1
                    sudo mysql -u root -e "CREATE DATABASE carrental;" || exit 1
                    sudo mysql -u root carrental < /var/www/html/carrental.sql || exit 1
                    '''
                }
            }
        }

        stage('Set Permissions & Restart Services') {
            steps {
                script {
                    sh '''
                    echo "🔧 Setting permissions and restarting services..."
                    sudo chown -R www-data:www-data /var/www/html/
                    sudo chmod -R 755 /var/www/html/
                    sudo systemctl restart apache2 mysql || exit 1
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh '''
                    echo "✅ Verifying deployment..."
                    curl -Is http://localhost | head -n 1 || exit 1
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "🚀 Deployment Successful!"
        }
        failure {
            echo "❌ Deployment Failed! Checking logs..."
            sh "sudo journalctl -xeu apache2 --no-pager || true"
            sh "sudo journalctl -xeu mysql --no-pager || true"
        }
    }
}
