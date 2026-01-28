pipeline {
  agent any

  environment {
    VENV = ".venv"
    MIN_COV = "80"
  }

  stages {
    // Triggers
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    // Environment setup
    stage('Setup Environment') {
      steps {
        sh '''
          python3 --version
          python3 -m venv ${VENV}
          . ${VENV}/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt -r requirements-dev.txt

          mkdir -p data
          touch data/current_inventory.txt
        '''
      }
    }

    // Code quality checks
    stage('Code Quality') {
      steps {
        sh '''
          . ${VENV}/bin/activate

          echo "Running formatting check (Black)..."
          black --check .

          echo "Running lint (flake8)..."
          flake8 app tests
        '''
      }
    }

    // Testing
    stage('Tests + Coverage') {
      steps {
        sh '''
          . ${VENV}/bin/activate

          pytest --cov=app --cov-report=term-missing --cov-report=xml --cov-report=html

          python - << 'PY'
import xml.etree.ElementTree as ET
root = ET.parse("coverage.xml").getroot()
rate = float(root.attrib["line-rate"]) * 100
min_cov = float("${MIN_COV}")
print(f"Coverage: {rate:.2f}% (minimum required: {min_cov:.2f}%)")
if rate < min_cov:
    raise SystemExit("Coverage below threshold")
PY
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: 'coverage.xml, htmlcov/**', fingerprint: true
        }
      }
    }

    // Build process
    stage('Build (Smoke Check)') {
      steps {
        sh '''
          . ${VENV}/bin/activate
          echo "Smoke check: importing app..."
          python -c "import app; print('Import OK')"
        '''
      }
    }
  }
}
