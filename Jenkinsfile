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
<<<<<<< HEAD
        sh 'python --version'
=======
        sh '''python --version 
'''
      }
    }

    stage('Testing') {
      steps {
        sh '''pip install django
python3 manage.py test
'''
>>>>>>> dd5e9a9ad1e581defb93df1e599a3b4c668f80cb
      }
    }

  }
}