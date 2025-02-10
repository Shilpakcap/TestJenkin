pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Shilpakcap/TestJenkin.git'
		bat 'where python'  // Check Python location

            }
        }
        stage('Run TD-37') {
            steps {
                script {
                    // Ensure we're in the Jenkins workspace
                    dir("${WORKSPACE}") {
                        bat 'python TD-37.py'  // Run the script in the workspace
                    }
                }
            }
        }
    }
}
