pipeline {
    agent any

    stages {
        stage('Fix Dpkg & APT Issues') {
            steps {
                script {
                    sh '''
                    echo "🔹 Fixing dpkg & APT locks..."
                    sudo rm -rf /var/lib/dpkg/lock /var/lib/dpkg/lock-frontend
                    sudo rm -rf /var/lib/apt/lists/lock
                    sudo rm -rf /var/cache/apt/archives/lock
                    sudo dpkg --configure -a || true
                    sudo apt-get update -y
                    sudo apt-get install -f -y
                    '''
                }
            }
        }

        stage('Remove & Clean MySQL') {
            steps {
                script {
                    sh '''
                    echo "🔹 Stopping MySQL (if running)..."
                    sudo systemctl stop mysql || true

                    echo "🔹 Removing MySQL Completely..."
                    sudo apt-get remove --purge -y mysql-server mysql-client mysql-common
                    sudo rm -rf /var/lib/mysql /etc/mysql
                    sudo apt-get autoremove -y
                    sudo apt-get autoclean -y
                    '''
                }
            }
        }

        stage('Fresh MySQL Install') {
            steps {
                script {
                    sh '''
                    echo "🔹 Installing MySQL non-interactively..."
                    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server mysql-client

                    echo "🔹 Securing MySQL (Setting root password)..."
                    sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;"

                    echo "✅ MySQL Installed Successfully!"
                    '''
                }
            }
        }

        stage('Start & Verify MySQL') {
            steps {
                script {
                    sh '''
                    echo "🔹 Restarting MySQL..."
                    sudo systemctl enable mysql || true
                    sudo systemctl restart mysql || sudo systemctl start mysql
                    sleep 5

                    echo "🔹 Checking MySQL Status..."
                    if ! sudo systemctl is-active --quiet mysql; then
                        echo "❌ MySQL Failed! Checking logs..."
                        sudo cat /var/log/mysql/error.log || sudo journalctl -xeu mysql --no-pager
                        exit 1
                    fi
                    echo "✅ MySQL is Running!"
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "🔹 Creating Database & Importing Data..."
                    sudo mysql -u root -proot -e "DROP DATABASE IF EXISTS carrental;"
                    sudo mysql -u root -proot -e "CREATE DATABASE carrental;"
                    sudo mysql -u root -proot carrental < /var/www/html/carrental.sql
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
