pipeline {
    agent any
    environment {
        DB_NAME = "carrental"
        DB_USER = "root"
        DB_PASS = "root"
        PROJECT_DIR = "/var/www/html/car-rental"
    }
    stages {
        stage('Update & Fix Server') {
            steps {
                script {
                    sh '''
                    echo "🔧 Fixing broken packages..."
                    sudo dpkg --configure -a || true
                    sudo apt-get install -f -y || true
                    sudo apt-get update -y
                    '''
                }
            }
        }

        stage('Install Required Packages') {
            steps {
                script {
                    sh '''
                    echo "📦 Installing Apache, MySQL, PHP..."
                    sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql unzip git
                    sudo systemctl enable apache2 mysql
                    '''
                }
            }
        }

        stage('Start & Check Services') {
            steps {
                script {
                    sh '''
                    echo "🚀 Restarting Apache & MySQL..."
                    sudo systemctl restart apache2 mysql
                    sleep 5
                    sudo systemctl status apache2 mysql --no-pager
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    sh '''
                    echo "📥 Cloning repository..."
                    sudo rm -rf ${PROJECT_DIR}
                    sudo git clone https://github.com/preethikannan15/carport.git ${PROJECT_DIR}
                    '''
                }
            }
        }

        stage('Extract Project') {
            steps {
                script {
                    sh '''
                    echo "📂 Extracting project files..."
                    cd ${PROJECT_DIR}
                    unzip -o Car-Rental-Portal-Using-PHP-and-MySQL-V-3.0.zip
                    sudo chown -R www-data:www-data ${PROJECT_DIR}
                    '''
                }
            }
        }

        stage('Setup MySQL Database') {
            steps {
                script {
                    sh '''
                    echo "💾 Creating database & importing SQL..."
                    sudo mysql -e "DROP DATABASE IF EXISTS ${DB_NAME}; CREATE DATABASE ${DB_NAME};"
                    sudo mysql ${DB_NAME} < ${PROJECT_DIR}/carrental.sql
                    '''
                }
            }
        }

        stage('Restart Services') {
            steps {
                script {
                    sh '''
                    echo "🔄 Restarting services..."
                    sudo systemctl restart apache2 mysql
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh '''
                    echo "✅ Checking Apache & MySQL Status..."
                    sudo systemctl status apache2 mysql --no-pager
                    echo "🌍 Visit http://<YOUR_SERVER_IP> to check the portal!"
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo "❌ Deployment failed! Check logs for details."
        }
    }
}
