node {
  def app
  def imageRepo = "gstvo2k15/test"
  def imageTag  = "${env.BUILD_NUMBER}"

  stage('Clone repository') {
    checkout scm
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
    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
      sh '''
        set -e
        echo "$DH_TOKEN" | docker login -u "$DH_USER" --password-stdin https://index.docker.io/v1/
        docker push ${imageRepo}:${imageTag}
        docker tag  ${imageRepo}:${imageTag} ${imageRepo}:latest
        docker push ${imageRepo}:latest
      '''
    }
  }

  stage('Trigger ManifestUpdate') {
    build job: 'updatemanifest',
          parameters: [string(name: 'DOCKERTAG', value: "${imageTag}")],
          wait: false,
          propagate: false
  }
}
