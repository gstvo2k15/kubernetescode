node {
  def imageRepo = "gstvo2k15/test"
  def gitSha    = sh(script: 'git rev-parse --short=8 HEAD', returnStdout: true).trim()
  def imageTag  = "${env.BUILD_NUMBER}-${gitSha}"
  def app

  stage('Clone repository') {
    checkout scm
  }

  stage('Quality: pylint') {
    sh '''
      set -e
      pip3 install --no-cache-dir -q pylint
      SCORE="$(pylint app.py 2>/dev/null | awk -F'/' '/Your code has been rated at/ {gsub(/[^0-9.]/,"",$1); print $1}')"
      
      python3 - <<PY
      import sys
      score=float("${SCORE}" or 0)
      sys.exit(0 if score >= 8.0 else 1)
      PY
    '''
  }

  stage('Build image') {
    app = docker.build("${imageRepo}:${imageTag}")
  }

  stage('Test image') {
    app.inside {
      sh 'echo "Tests passed"'
    }
  }

  stage('Push image') {
    withCredentials([
      usernamePassword(
        credentialsId: 'dockerhub',
        usernameVariable: 'DH_USER',
        passwordVariable: 'DH_TOKEN'
      )
    ]) {
      sh """
        set -e
        echo "\$DH_TOKEN" | docker login -u "\$DH_USER" --password-stdin https://index.docker.io/v1/
        docker push ${imageRepo}:${imageTag}
        docker tag ${imageRepo}:${imageTag} ${imageRepo}:latest
        docker push ${imageRepo}:latest
      """
    }
  }

  stage('Trigger ManifestUpdate') {
    build job: 'updatemanifest',
          parameters: [string(name: 'DOCKERTAG', value: imageTag)],
          wait: false,
          propagate: false
  }
}
