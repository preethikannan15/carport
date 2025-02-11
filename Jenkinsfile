pipeline {
    agent any

    stages {
       stage('Fix DPKG & Install MySQL') {
    steps {
        script {
            sh '''
            echo "🔹 Fixing DPKG Issues..."
            sudo dpkg --configure -a || true  
            sudo apt-get update
            sudo apt-get install -f -y

            echo "🔹 Setting Non-Interactive Mode..."
            export DEBIAN_FRONTEND=noninteractive

            echo "🔹 Installing MySQL Server..."
            sudo apt-get install -yq mysql-server --no-install-recommends || (echo "❌ MySQL Installation Failed!" && exit 1)

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
        stage('Verify MySQL & Restart if Needed') {
            steps {
                script {
                    sh '''
                    echo "🔹 Checking MySQL Status..."
                    if ! sudo systemctl is-active --quiet mysql; then
                        echo "⚠️ MySQL is not running. Attempting to start..."
                        sudo systemctl start mysql
                        sleep 10  # Wait for MySQL initialization
                        if ! sudo systemctl is-active --quiet mysql; then
                            echo "❌ MySQL failed to start!"
                            sudo journalctl -u mysql --no-pager | tail -n 20
                            exit 1
                        fi
                    fi
                    echo "✅ MySQL is running."
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
       
