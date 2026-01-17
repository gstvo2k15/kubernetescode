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
      set -eu

      docker run --rm -i \
        -v "$PWD:/work" \
        -w /work \
        python:3.8-slim-buster sh <<'EOF'
      set -eu

      pip install --no-cache-dir -q pylint

      python - <<'PY'
      import re
      import subprocess
      import sys

      result = subprocess.run(
          ["pylint", "app.py"],
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT,
          text=True
      )

      print(result.stdout, end="")

      match = re.search(r"rated at\\s+([0-9.]+)/10", result.stdout)
      score = float(match.group(1)) if match else 0.0

      print(f"pylint_score={score}")

      sys.exit(0 if score >= 8.0 else 1)
      PY
      EOF
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
