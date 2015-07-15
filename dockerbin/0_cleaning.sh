#!/bin/bash
#
# docker cleannig
#

if [ "$GIT_HOME" = "" ]; then
    echo "GIT_HOME must be set. exit."
    exit 1
fi

docker rm `docker ps -a -q`

docker rmi $(docker images | awk '/^<none>/ { print $3 }')

exit 0