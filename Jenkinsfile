pipeline {
    agent any

    stages {
        stage('Fix Dpkg Issues & Update System') {
            steps {
                script {
                    sh '''
                    echo "🔹 Fixing dpkg issues..."
                    sudo rm -rf /var/lib/dpkg/lock /var/lib/dpkg/lock-frontend
                    sudo rm -rf /var/lib/apt/lists/lock
                    sudo rm -rf /var/cache/apt/archives/lock
                    sudo dpkg --configure -a || true
                    sudo apt-get update
                    '''
                }
            }
        }

        stage('Fix Broken Packages') {
            steps {
                script {
                    sh '''
                    echo "🔹 Fixing broken package installations..."
                    sudo apt-get install -f -y || true
                    '''
                }
            }
        }

        stage('Install Apache, PHP, and MySQL') {
            steps {
                script {
                    sh '''
                    echo "🔹 Installing Apache, PHP, and MySQL..."
                    export DEBIAN_FRONTEND=noninteractive
                    sudo apt-get install -y apache2 mysql-server php php-mysql libapache2-mod-php unzip git
                    '''
                }
            }
        }

        stage('Start & Verify MySQL') {
            steps {
                script {
                    sh '''
                    echo "🔹 Starting MySQL..."
                    sudo systemctl enable mysql || true
                    sudo systemctl restart mysql || sudo systemctl start mysql
                    sleep 5

                    echo "🔹 Checking MySQL Status..."
                    if ! sudo systemctl is-active --quiet mysql; then
                        echo "❌ MySQL Failed! Checking logs..."
                        sudo journalctl -xeu mysql --no-pager || sudo cat /var/log/mysql/error.log
                        exit 1
                    fi
                    echo "✅ MySQL is Running!"
                    '''
                }
            }
        }

        stage('Clone & Extract Files') {
            steps {
                script {
                    sh '''
                    echo "🔹 Cloning repository..."
                    sudo rm -rf /var/www/html/*
                    git clone https://github.com/preethikannan15/carport.git /var/www/html/
                    cd /var/www/html/
                    unzip Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "🔹 Setting up database..."
                    sudo mysql -u root -e "DROP DATABASE IF EXISTS carrental;"
                    sudo mysql -u root -e "CREATE DATABASE carrental;"
                    sudo mysql -u root carrental < /var/www/html/carrental.sql
                    echo "✅ Database Imported Successfully!"
                    '''
                }
            }
        }

        stage('Restart Services & Set Permissions') {
            steps {
                script {
                    sh '''
                    echo "🔹 Restarting services..."
                    sudo systemctl restart apache2
                    sudo systemctl restart mysql
                    sudo chown -R www-data:www-data /var/www/html/
                    sudo chmod -R 755 /var/www/html/
                    echo "✅ Deployment Successful! Visit http://your-server-ip"
                    '''
                }
            }
        }
    }

    post {
        failure {
            script {
                sh '''
                echo "❌ Deployment Failed! Checking Logs..."
                sudo journalctl -xeu mysql --no-pager || sudo cat /var/log/mysql/error.log
                '''
            }
        }
    }
}
