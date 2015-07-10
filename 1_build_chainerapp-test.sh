#!/bin/bash
#
# docker build chainerapp-test
#
cp Dockerfile_chainerapp-test Dockerfile
docker build -t t4j/chainerapp-test:latest .

rm -f Dockerfile
