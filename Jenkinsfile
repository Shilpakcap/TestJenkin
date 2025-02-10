pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Shilpakcap/TestJenkin.git'
            }
        }
        stage('Run TD-37') {
            steps {
                script {
                    dir("${WORKSPACE}") {  // Ensures we are in the right directory
                        bat 'python TD-37.py'  // Uses system-installed Python
                    }
                }
            }
        }
    }
}
