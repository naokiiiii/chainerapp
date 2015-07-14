#!/bin/bash
#
# docker build chainerapp-test
#

if [ "$GIT_HOME" = "" ]; then
    echo "GIT_HOME must be set. exit."
    exit 1
fi

docker build --rm -t t4j/chainer:latest -f Dockerfiles/Dockerfile_chainer $GIT_HOME/chainerapp/Dockerfiles

docker build --rm -t t4j/chainerapp-test:latest -f Dockerfiles/Dockerfile_chainerapp-test $GIT_HOME/chainerapp/Dockerfiles

exit 0