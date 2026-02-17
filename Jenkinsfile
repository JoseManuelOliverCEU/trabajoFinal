pipeline {
  agent any

  environment {
    COMPOSE_PROJECT_NAME = "trabajofinal"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
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
        // Muestra estado (la health puede tardar unos segundos)
        sh 'docker-compose ps'
      }
    }

    stage('Run Tests') {
      steps {
        // Tests dentro del contenedor web (mismo entorno)
        sh 'docker-compose run --rm web pytest -q tests --cov=app --cov-report=term-missing'
      }
    }

    stage('Migrate + Seed') {
      steps {
        // Aplica migraciones y seed ANTES de desplegar
        sh 'docker-compose run --rm web flask --app wsgi:app db upgrade'
        sh 'docker-compose run --rm web flask --app wsgi:app seed'
      }
    }

    stage('Deploy (local)') {
      steps {
        // Levanta todo
        sh 'docker-compose up -d'
      }
    }
  }

  post {
    always {
      sh 'docker-compose ps'
      // Útil si algo falla:
      // sh 'docker-compose logs --no-color --tail=200'
    }
  }
}
