
pipeline {
  agent { label 'Jenkins' }
  environment {
   ANSIBLE_PRIVATE_KEY=credentials('maxm_we') 
  }
  stages {
    stage('Generate clients.json') {
      steps {
        //sh 'ansible-galaxy collection install -r requirements.yml'
        //sh 'touch clients.json'
        sh 'python3 boto3/client_accounts.py > clients_full.json'
        sh 'python3 boto3/client_accounts-name-only.py > clients.json'
      }
    }
  }
}
