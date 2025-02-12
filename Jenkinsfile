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
                    dir("${WORKSPACE}") {
                        // Use the full path to Python
                        bat '"C:\\Users\\shilpkul\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" TD-37.py' 
                        
                    }
                }
            }
        }
    }
}
