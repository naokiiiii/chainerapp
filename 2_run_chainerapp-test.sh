#!/bin/bash
#
# docker run chainerapp-test
#
docker run --name chainerapp-test-up -i -t -d \
  -v $GIT_HOME/chainerapp:/opt/t4j/chainerapp \
  -v $GIT_HOME/chainer-data:/var/opt/t4j/chainer \
  t4j/chainerapp-test:latest
