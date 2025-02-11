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

        stage('Install & Start MySQL') {
            steps {
                script {
                    sh '''
                    echo "🔹 Setting Non-Interactive Mode..."
                    sudo echo 'mysql-server mysql-server/root_password password root' | sudo debconf-set-selections
                    sudo echo 'mysql-server mysql-server/root_password_again password root' | sudo debconf-set-selections

                    echo "🔹 Installing MySQL Server..."
                    sudo apt-get install -yq mysql-server --no-install-recommends || (echo "❌ MySQL Installation Failed!" && exit 1)

                    echo "🔹 Checking MySQL Configuration..."
                    if [ ! -f /etc/mysql/mysql.conf.d/mysqld.cnf ]; then
                        echo "⚠️ MySQL configuration file missing!"
                        exit 1
                    fi

                    echo "🔹 Ensuring MySQL Starts..."
                    sudo systemctl enable mysql
                    sudo systemctl restart mysql
                    sleep 5

                    echo "🔹 Checking MySQL Status..."
                    if ! sudo systemctl is-active --quiet mysql; then
                        echo "❌ MySQL is NOT running! Check logs: sudo journalctl -u mysql --no-pager"
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
                    sudo apt-get install -y git
                    git clone https://github.com/https://github.com/preethikannan15/carport.git /var/www/html/car-rental
                    cd /var/www/html/car-rental
                    unzip Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html/
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "🔹 Setting Up MySQL Database..."
                    sudo mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS carrental;"
                    sudo mysql -u root -proot carrental < /var/www/html/car-rental/carrental.sql
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
                sudo journalctl -u mysql --no-pager
                '''
            }
        }
    }
}
