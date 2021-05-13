pipeline {
    agent {
      docker {
        image 'python:3.8'
        args '-u root --cap-add NET_ADMIN'
      }
    }
    environment {
      DISABLE_AUTH = 'true'
      DB_ENGINE = 'sqlite'
    }

    stages {
      stage('Build') {
        steps {
          sh 'pip3 install -r requirements.txt'
        }
      }

    stage('Testing') {
      steps {
        sh 'pytest'
      }
    }

  }
}