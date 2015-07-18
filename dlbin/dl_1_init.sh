#!/bin/bash
#
# Deep Learning Init
#

CURRENT=$(cd $(dirname $0) && pwd)
. $CURRENT/dl_0_env.sh

cd $PYTHON_DIR
echo "[START] make_train_data"
rm $DATA_DIR/mean.npy > /dev/null 2>&1
rm $DATA_DIR/train.txt > /dev/null 2>&1
rm $DATA_DIR/test.txt > /dev/null 2>&1
rm $DATA_DIR/labels.txt > /dev/null 2>&1
rm $DATA_DIR/images/* > /dev/null 2>&1
rm $DATA_DIR/tmpimages/* > /dev/null 2>&1
python ./make_train_data.py -s $DATA_DIR/mstimages \
        -o $DATA_DIR/images -t $DATA_DIR/train.txt -e $DATA_DIR/test.txt \
        -l $DATA_DIR/labels.txt
echo "[START] crop"
mv $DATA_DIR/images/* $DATA_DIR/tmpimages
python ./crop.py $DATA_DIR/tmpimages $DATA_DIR/images
echo "[START] compute_mean"
python ./compute_mean.py -o $DATA_DIR/mean.npy $DATA_DIR/train.txt > /tmp/test2.txt
