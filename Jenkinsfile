pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Shilpakcap/TestJenkin.git'
                script {
                    echo "Workspace Directory: ${WORKSPACE}"
                    bat 'dir'  // Lists all files and folders in the workspace
                }
            }
        }
        stage('Run TD-37') {
            steps {
                script {
                    dir("${WORKSPACE}") {
                        bat 'dir'  // Lists files to check if TD-37.py is present
                        
                    }
                }
            }
        }
    }
}
