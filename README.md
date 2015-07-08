chainerapp
=====================
## Requiements

- Docker (>=1.6)
- mac os?

## How to use

####Fork & Clone
- https://github.com/<GIT_ID>/chainer.git
- https://github.com/<GIT_ID>//chainerapp.git
-> ex. GIT_HOME=/Users/<OS_ID>/git

####Build DockerImage
$ docker build -t t4j/chainerapp-test:0.1 /Users/<OS_ID>/git/chainerapp/.

####Start Container
docker run --name chainerapp-test-up -i -t -d -p 8080:8080 ¥
  -v /Users/<OS_ID>/git/serverapp:/opt/t4j/serverapp ¥
  -v /Users/<OS_ID>/git/chainer:/opt/t4j/chainer ¥
  t4j/chainerapp-test:0.1

####Test
$ docker exec -it chainerapp-test-up XXXX

####Login Container
$ docker exec -it chainerapp-test-up bash

####top & delete Container
$ docker stop chainerapp-test-up
$ docker rm chainerapp-test-up
