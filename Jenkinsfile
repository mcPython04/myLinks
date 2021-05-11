pipeline {
  agent {
    docker {
      image 'python:3.8'
      args '-u root --cap-add NET_ADMIN'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh 'python --version '
      }
    }

  }
}