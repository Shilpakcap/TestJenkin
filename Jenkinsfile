pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'TD-37.py'  // If it's a Python script
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'TD-37.py'  // Runs test script, check logs
            }
        }
    }
}
