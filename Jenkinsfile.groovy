pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Building the project...'
            }
        }
        stage('Run Script') {
            steps {
                                bat 'script.bat'  // Uncomment for Windows batch script
            }
        }
    }
}
