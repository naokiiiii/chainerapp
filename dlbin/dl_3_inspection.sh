#!/bin/bash
#
# Deep Learning Inspection
#
CURRENT=$(cd $(dirname $0) && pwd)
. $CURRENT/dl_0_env.sh

cd $PYTHON_DIR
python ./crop.py $DATA_DIR/tmpimages $DATA_DIR/tmpimages
python ./inspection.py --model=$DATA_DIR/model/model --label=$DATA_DIR/labels.txt --mean=$DATA_DIR/mean.npy $1
