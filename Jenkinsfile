pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Clone the repository
                git branch: 'main', url: 'https://github.com/Shilpakcap/TestJenkin.git'
            }
        }
        stage('Run TD-37') {
            steps {
                script {
                    // Ensure the working directory is set to where TD-37.py is located
                    dir('path_to_your_script_directory') {
                        bat 'python TD-37.py'  // For Windows, 
                    }
                }
            }
        }
    }
}
