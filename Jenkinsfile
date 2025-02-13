pipeline {
    agent any

    stages {
        stage('Fix Dpkg Issues & Clean System') {
            steps {
                script {
                    sh '''
                    echo "🔹 Fixing dpkg & apt locks..."
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

        stage('Remove Old MySQL & Install Fresh') {
            steps {
                script {
                    sh '''
                    echo "🔹 Removing any existing MySQL..."
                    sudo systemctl stop mysql || true
                    sudo apt-get remove --purge -y mysql-server mysql-client mysql-common
                    sudo rm -rf /var/lib/mysql /etc/mysql
                    sudo apt-get autoremove -y
                    sudo apt-get autoclean -y

                    echo "🔹 Installing MySQL non-interactively..."
                    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server mysql-client
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
                        sudo journalctl -xeu mysql --no-pager || sudo cat /var/log/mysql/error.log
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
                    echo "🔹 Creating database..."
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
