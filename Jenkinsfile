pipeline {
    agent any

    stages {
        stage('Fix DPKG & Install Dependencies') {
            steps {
                script {
                    sh '''
                    echo "🔹 Fixing DPKG Issues..."
                    sudo dpkg --configure -a || true  # Fix interrupted installation
                    sudo apt-get update

                    echo "🔹 Installing Apache, MySQL, PHP..."
                    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 mysql-server php php-mysql unzip

                    echo "🔹 Enabling & Restarting Services..."
                    sudo systemctl enable apache2 mysql
                    sudo systemctl restart apache2 mysql
                    '''
                }
            }
        }

        stage('Verify MySQL & Fix Errors') {
            steps {
                script {
                    sh '''
                    echo "🔹 Checking MySQL Status..."
                    if ! sudo systemctl is-active --quiet mysql; then
                        echo "⚠️ MySQL is not running. Attempting to start..."
                        sudo systemctl start mysql || (echo "❌ MySQL failed to start!" && exit 1)
                    fi
                    
                    echo "🔹 Checking MySQL Logs for Errors..."
                    sudo tail -n 20 /var/log/mysql/error.log || true
                    '''
                }
            }
        }

        stage('Clone Repository & Extract Files') {
            steps {
                script {
                    sh '''
                    echo "🔹 Cloning repository and extracting files..."
                    sudo rm -rf /var/www/html/*
                    git clone https://github.com/preethikannan15/carport.git /tmp/carport
                    unzip /tmp/carport/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/
                    sudo chown -R www-data:www-data /var/www/html/
                    sudo chmod -R 755 /var/www/html/
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "🔹 Creating MySQL Database & Importing Data..."
                    sudo mysql -e "DROP DATABASE IF EXISTS carrental; CREATE DATABASE carrental;"
                    sudo mysql carrental < /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0/carrental.sql
                    echo "✅ Database imported successfully!"
                    '''
                }
            }
        }

        stage('Restart Services & Set Permissions') {
            steps {
                script {
                    sh '''
                    echo "🔹 Restarting services and setting permissions..."
                    sudo systemctl restart apache2 mysql
                    sudo chmod -R 777 /var/www/html/
                    '''
                }
            }
        }

        stage('Deployment Complete') {
            steps {
                script {
                    echo "✅ Deployment Successful!"
                    sh '''
                    echo "🌐 Access your portal at: http://$(hostname -I | awk '{print $1}')"
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo "❌ Deployment Failed! Check MySQL logs: sudo journalctl -u mysql --no-pager"
        }
    }
}
