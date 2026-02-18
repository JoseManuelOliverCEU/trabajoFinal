pipeline {
  agent any

  environment {
    COMPOSE_PROJECT_NAME = "trabajofinal"
  }

  stage('Create .env (from Jenkins credentials)') {
    steps {
      withCredentials([
        string(credentialsId: 'mariadb-database', variable: 'DB_NAME'),
        string(credentialsId: 'mariadb-user', variable: 'DB_USER'),
        string(credentialsId: 'mariadb-password', variable: 'DB_PASS'),
        string(credentialsId: 'mariadb-root-password', variable: 'DB_ROOT_PASS')
      ]) {
        sh '''
          cat > .env <<EOF
          MARIADB_DATABASE=${DB_NAME}
          MARIADB_USER=${DB_USER}
          MARIADB_PASSWORD=${DB_PASS}
          MARIADB_ROOT_PASSWORD=${DB_ROOT_PASS}

          DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASS}@db:3306/${DB_NAME}
          API_BASE_URL=http://127.0.0.1:5000/api
          EOF
          echo ".env generated"
        '''
      }
    }
  }


    stage('Build') {
      steps {
        sh 'docker-compose build --no-cache'
      }
    }

    stage('Up DB') {
      steps {
        sh 'docker-compose up -d db'
        sh 'docker-compose ps'
      }
    }

    stage('Run Tests') {
      steps {
        // IMPORTANTE: apunta explícitamente a tests para que no salga "no tests ran"
        sh 'docker-compose run --rm web pytest -q tests --cov=app --cov-report=term-missing'
      }
    }

    stage('Migrate + Seed') {
      steps {
        sh 'docker-compose run --rm web flask --app wsgi:app db upgrade'
        sh 'docker-compose run --rm web flask --app wsgi:app seed'
      }
    }

    stage('Deploy (local)') {
      steps {
        sh 'docker-compose up -d'
      }
    }
  }

  post {
    always {
      sh 'docker-compose ps'
    }
  }
}
