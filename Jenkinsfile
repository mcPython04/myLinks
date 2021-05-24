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
          sh 'curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
          sh 'chmod +x /usr/local/bin/docker-compose'
        }
      }

    stage('Testing') {
      steps {
        sh 'make test' 
      }
    }
  }
}
