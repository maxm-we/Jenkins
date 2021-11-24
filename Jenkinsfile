
pipeline {
  //agent { label 'Jenkins' }
  stages {
    stage('Generate clients.json') {
      steps {
        sh 'python3 boto3/client_accounts.py > /var/lib/jenkins/black_sun/clients_full.json'
        sh 'python3 boto3/client_accounts-name-only.py > /var/lib/jenkins/black_sun/clients.json'
      }
    }
  }
}
