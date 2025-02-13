pipeline {
    agent any

    stages {
        stage('Fix DPKG & Install Dependencies') {
            steps {
                script {
                    sh '''
                    echo "🔹 Fixing DPKG Issues..."
                    sudo dpkg --configure -a || true
                    sudo apt-get update
                    sudo apt-get install -f -y
                    '''
                }
            }
        }

        stage('Install Required Packages') {
            steps {
                script {
                    sh '''
                    echo "🔹 Installing Required Packages..."
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip git
                    '''
                }
            }
        }

        stage('Fix MySQL & Restart') {
            steps {
                script {
                    sh '''
                    echo "🔹 Checking MySQL Installation..."
                    sudo systemctl enable mysql
                    sudo systemctl restart mysql || sudo systemctl start mysql
                    sleep 5

                    echo "🔹 Checking MySQL Status..."
                    if ! sudo systemctl is-active --quiet mysql; then
                        echo "❌ MySQL Failed! Checking logs..."
                        sudo journalctl -xeu mysql --no-pager || sudo cat /var/log/mysql/error.log
                        exit 1
                    fi
                    echo "✅ MySQL is Running Successfully!"
                    '''
                }
            }
        }

        stage('Clone Repository & Extract Files') {
            steps {
                script {
                    sh '''
                    echo "🔹 Cloning Repository..."
                    sudo rm -rf /var/www/html/*
                    git clone https://github.com/https://github.com/preethikannan15/carport.git /var/www/html/
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
                    echo "🔹 Creating & Importing Database..."
                    sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS carrental;"
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
                    echo "🔹 Restarting Apache & MySQL..."
                    sudo systemctl restart apache2
                    sudo systemctl restart mysql
                    sudo chown -R www-data:www-data /var/www/html/
                    sudo chmod -R 755 /var/www/html/
                    echo "✅ Services Restarted Successfully!"
                    '''
                }
            }
        }

        stage('Deployment Complete') {
            steps {
                script {
                    echo "🚀 Deployment Successful! Visit http://your-server-ip to access the Car Rental Portal."
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
