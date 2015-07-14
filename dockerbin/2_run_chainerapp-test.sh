#!/bin/bash
#
# docker run chainerapp-test
#
if [ "$GIT_HOME" = "" ]; then
    echo "GIT_HOME must be set. exit."
    exit 1
fi

if [ ! -e $GIT_HOME/chainer-data ]; then
    mkdir -p $GIT_HOME/chainer-data
fi

cd $GIT_HOME/chainer-data

[ -e mstimages ] || mkdir mstimages
[ -e images ] || mkdir images
[ -e model ] || mkdir model
[ -e tmpimages ] || mkdir tmpimages

docker run --name chainerapp-test-up -i -t -d \
  -v $GIT_HOME/chainerapp:/opt/t4j/chainerapp \
  -v $GIT_HOME/chainer-data:/var/opt/t4j/chainer-data \
  t4j/chainerapp-test:latest

exit 0