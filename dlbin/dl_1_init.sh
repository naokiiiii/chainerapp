#!/bin/bash
#
# Deep Learning Init
#

CURRENT=$(cd $(dirname $0) && pwd)
. $CURRENT/dl_0_env.sh

cd $PYTHON_DIR
echo "[START] make_train_data"
python ./make_train_data.py $DATA_DIR
echo "[START] compute_mean"
python ./compute_mean.py -o $DATA_DIR/mean.npy $DATA_DIR/train.txt
echo "[START] crop"
python ./crop.py $DATA_DIR/images $DATA_DIR/images
