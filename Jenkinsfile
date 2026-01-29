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

    stage('Environment Setup') {
      steps {
        sh '''
          python3 --version || python --version
          python3 -m venv .venv || python -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt -r requirements-dev.txt
        '''
      }
    }

    stage('Code Quality Checks') {
      steps {
        sh '''
          . .venv/bin/activate
          echo "Running Black formatter check..."
          black --check .
          echo "Running Flake8 linter..."
          flake8 app tests
        '''
      }
    }

    stage('Testing') {
      steps {
        sh '''
          . .venv/bin/activate
          mkdir -p data
          touch data/current_inventory.txt
          echo "Running pytest with coverage..."
          pytest --cov=app --cov-report=term-missing --cov-report=xml --cov-report=html
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: 'coverage.xml,htmlcov/**', allowEmptyArchive: true, fingerprint: true
        }
      }
    }

    stage('Coverage Validation') {
      steps {
        sh '''
          . .venv/bin/activate
          python - << 'PY'
import xml.etree.ElementTree as ET
root = ET.parse('coverage.xml').getroot()
rate = float(root.attrib['line-rate']) * 100
min_cov = float('80')
print(f'Coverage: {rate:.2f}% (minimum required: {min_cov:.2f}%)')
if rate < min_cov:
    raise SystemExit('Coverage below threshold')
PY
        '''
      }
    }

    stage('Build (Smoke Check)') {
      steps {
        sh '''
          . .venv/bin/activate
          python -c "import app; print('Import successful')"
        '''
      }
    }
  }

  post {
    success {
      echo 'Pipeline completed successfully'
    }
    failure {
      echo 'Pipeline failed.'
    }
  }
}