pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Shilpakcap/TestJenkin.git'
                script {
                    echo "Workspace Directory: ${WORKSPACE}"
                    bat 'dir /s'  // List all files & subdirectories
                }
            }
        }
    }
}
