#!/bin/bash
#
# Deep Learning Init
#
python make_train_data.py mstimages
python compute_mean.py train.txt
python crop.py images images
