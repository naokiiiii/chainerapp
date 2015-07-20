#!/bin/bash
#
# Deep Learning Init
#

CURRENT=$(cd $(dirname $0) && pwd)
. $CURRENT/dl_0_env.sh

cd $PYTHON_DIR
rm $DATA_DIR/mean.npy > /dev/null 2>&1
rm $DATA_DIR/train.txt > /dev/null 2>&1
rm $DATA_DIR/test.txt > /dev/null 2>&1
rm $DATA_DIR/labels.txt > /dev/null 2>&1
rm -fr $DATA_DIR/images/* > /dev/null 2>&1
rm -fr $DATA_DIR/tmpimages/* > /dev/null 2>&1
echo "[START] fase_recognize"
# mv $DATA_DIR/images/* $DATA_DIR/tmpimages
cp -r $DATA_DIR/mstimages/* $DATA_DIR/tmpimages/
python ./face_recognize.py $DATA_DIR/tmpimages $DATA_DIR/images
rm -fr $DATA_DIR/tmpimages/* > /dev/null 2>&1
mv $DATA_DIR/images/* $DATA_DIR/tmpimages


echo "[START] make_train_data"
python ./make_train_data.py -s $DATA_DIR/tmpimages \
        -o $DATA_DIR/images -t $DATA_DIR/train.txt -e $DATA_DIR/test.txt \
        -l $DATA_DIR/labels.txt
rm -fr $DATA_DIR/tmpimages/* > /dev/null 2>&1

echo "[START] resize"
mv $DATA_DIR/images/* $DATA_DIR/tmpimages
python ./img_resize.py $DATA_DIR/tmpimages $DATA_DIR/images
rm -fr $DATA_DIR/tmpimages/* > /dev/null 2>&1

echo "[START] compute_mean"
python ./compute_mean.py -o $DATA_DIR/mean.npy $DATA_DIR/train.txt > /tmp/test2.txt
