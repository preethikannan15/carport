pipeline {
    agent any

    stages {
        stage('Fix MySQL Issues') {
            steps {
                script {
                    sh '''
                    echo "🔹 Fixing MySQL Issues..."
                    sudo rm -rf /var/lib/dpkg/lock*
                    sudo rm -rf /var/lib/apt/lists/lock
                    sudo rm -rf /var/cache/apt/archives/lock
                    sudo apt-get update
                    sudo apt-get install -f -y
                    sudo dpkg --configure -a
                    '''
                }
            }
        }

        stage('Start & Verify MySQL') {
            steps {
                script {
                    sh '''
                    echo "🔹 Restarting MySQL..."
                    sudo systemctl enable mysql
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
                    echo "✅ Services Restarted!"
                    '''
                }
            }
        }

        stage('Deployment Complete') {
            steps {
                script {
                    echo "🚀 Deployment Successful! Visit http://your-server-ip"
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
