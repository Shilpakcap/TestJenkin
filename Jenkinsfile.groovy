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
                //sh 'chmod +x script.sh'  // Enable execute permission for Linux/Mac
                //sh './script.sh'  // Run the script (for Linux/Mac)
                bat 'script.bat'  // Uncomment for Windows batch script
            }
        }
    }
}
