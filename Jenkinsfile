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
          sh 'python --version'
        }
      }

    stage('Testing') {
      steps {
        sh 'pip3 install django'
        sh 'pip3 install django-registration'
        sh 'pip3 install Pillow'
        sh 'pip3 install requests'
        sh 'pip3 install pytest-django'
        sh 'pip3 install pytest-cov'
        sh 'pytest'
      }
    }

  }
}