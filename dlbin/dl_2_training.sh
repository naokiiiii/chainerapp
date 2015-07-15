#!/bin/bash
#
# Deep Learning Training
#
CURRENT=$(cd $(dirname $0) && pwd)
. $CURRENT/dl_0_env.sh

cd $PYTHON_DIR
python ./nurse_train.py -m $DATA_DIR/mean.npy -o $DATA_DIR/model \
        -g -1 -E $DL_HISTORY $DATA_DIR/train.txt $DATA_DIR/test.txt

