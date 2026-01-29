pipeline {
  agent any

  environment {
    MIN_COV = "80"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('CI in Docker (Python)') {
      steps {
        sh '''
          docker run --rm \
            -v "$PWD:/work" -w /work \
            python:3.11-slim bash -lc "
              python --version &&
              python -m venv .venv &&
              . .venv/bin/activate &&
              pip install --upgrade pip &&
              pip install -r requirements.txt -r requirements-dev.txt &&
              mkdir -p data && touch data/current_inventory.txt &&
              black --check . &&
              flake8 app tests &&
              pytest --cov=app --cov-report=term-missing --cov-report=xml --cov-report=html &&
              python - << 'PY'
import xml.etree.ElementTree as ET
root = ET.parse('coverage.xml').getroot()
rate = float(root.attrib['line-rate']) * 100
min_cov = float('${MIN_COV}')
print(f'Coverage: {rate:.2f}% (minimum required: {min_cov:.2f}%)')
if rate < min_cov:
    raise SystemExit('Coverage below threshold')
PY
            "
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: 'coverage.xml, htmlcov/**', fingerprint: true
        }
      }
    }

    stage('Build (Smoke Check)') {
      steps {
        sh '''
          docker run --rm \
            -v "$PWD:/work" -w /work \
            python:3.11-slim bash -lc "
              python -c \\"import app; print('Import OK')\\"
            "
        '''
      }
    }
  }
}
