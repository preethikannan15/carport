pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                    echo "🔧 Fixing package manager issues..."
                    sudo rm -rf /var/lib/dpkg/lock /var/lib/dpkg/lock-frontend
                    sudo dpkg --configure -a || true
                    sudo apt-get update -y

                    echo "📦 Installing required packages..."
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip git || exit 1

                    echo "🔄 Restarting services..."
                    sudo systemctl enable apache2 mysql
                    sudo systemctl restart apache2 mysql
                    '''
                }
            }
        }

        stage('Verify MySQL') {
            steps {
                script {
                    sh '''
                    echo "✅ Checking MySQL status..."
                    sudo systemctl status mysql || (echo "❌ MySQL failed to start!" && exit 1)

                    echo "🔄 Ensuring MySQL is running..."
                    if ! pgrep mysql > /dev/null; then
                        echo "❌ MySQL is not running! Restarting..."
                        sudo systemctl restart mysql
                        sleep 5
                        sudo systemctl status mysql || exit 1
                    fi
                    '''
                }
            }
        }

        stage('Create Database') {
            steps {
                script {
                    sh '''
                    echo "🗄️ Creating database..."
                    sudo mysql -e "DROP DATABASE IF EXISTS carrental;"
                    sudo mysql -e "CREATE DATABASE carrental;"
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
                    sudo git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git /var/www/html/ || exit 1
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

        stage('Import Database') {
            steps {
                script {
                    sh '''
                    echo "📥 Importing database..."
                    sudo mysql carrental < /var/www/html/carrental.sql || exit 1
                    '''
                }
            }
        }

        stage('Set Permissions & Restart Services') {
            steps {
                script {
                    sh '''
                    echo "🔧 Setting permissions..."
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
