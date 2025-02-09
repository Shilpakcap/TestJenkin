pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                bat 'TD-37.py'  // If it's a Python script
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                bat 'TD-37.py'  // Runs test script, check logs
            }
        }
    }
}
