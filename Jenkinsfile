pipeline {
    agent any

    environment {
        DEBIAN_FRONTEND = "noninteractive"
    }

    stages {
        stage('Update & Install Dependencies') {
            steps {
                script {
                    sh '''
                    echo "Updating system and installing required packages..."
                    sudo apt-get update -y
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip git
                    
                    echo "Enabling Apache and MySQL services..."
                    sudo systemctl enable --now apache2
                    sudo systemctl enable --now mysql
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                    echo "Cloning repository..."
                    sudo rm -rf /var/www/html/*
                    sudo git clone https://github.com/preethikannan15/carport.git /var/www/html
                    '''
                }
            }
        }

        stage('Extract Project') {
            steps {
                script {
                    sh '''
                    echo "Extracting project files..."
                    sudo unzip -o /var/www/html/Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip -d /var/www/html
                    sudo chown -R www-data:www-data /var/www/html
                    sudo chmod -R 755 /var/www/html
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "Restarting MySQL..."
                    sudo systemctl restart mysql

                    echo "Allowing MySQL some time to initialize..."
                    sleep 10

                    echo "Setting up MySQL root password..."
                    sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;"

                    echo "Creating and importing the database..."
                    sudo mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS carrental;"
                    sudo mysql -u root -proot carrental < /var/www/html/carrental.sql
                    '''
                }
            }
        }

        stage('Restart Services') {
            steps {
                script {
                    sh '''
                    echo "Restarting Apache and MySQL services..."
                    sudo systemctl restart apache2
                    sudo systemctl restart mysql
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh '''
                    echo "Verifying deployment..."
                    sleep 5
                    curl -I http://localhost | grep "200 OK"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful! You can now access the portal via the server's IP."
        }
        failure {
            echo "❌ Deployment failed! Gathering logs for debugging..."
            sh 'sudo journalctl -xeu apache2 --no-pager'
            sh 'sudo journalctl -xeu mysql --no-pager'
        }
    }
}
