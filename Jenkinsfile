node {
  def app

  stage('Clone repository') {
    checkout scm
  }

  stage('Build image') {
    app = docker.build("gstvo2k15/test:${env.BUILD_NUMBER}")
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
        docker push gstvo2k15/test:${BUILD_NUMBER}
        docker tag gstvo2k15/test:${BUILD_NUMBER} gstvo2k15/test:latest
        docker push gstvo2k15/test:latest
      '''
    }
  }

  stage('Trigger ManifestUpdate') {
    build job: 'updatemanifest',
          parameters: [string(name: 'DOCKERTAG', value: "${env.BUILD_NUMBER}")],
          wait: false,
          propagate: false
  }
}
