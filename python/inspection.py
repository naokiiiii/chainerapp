#!/usr/bin/env python

from __future__ import print_function
import argparse
import datetime
import json
import multiprocessing
import random
import sys
import threading
import time

import numpy as np
from PIL import Image

import six
import six.moves.cPickle as pickle
from six.moves import queue

from chainer import cuda
from chainer import optimizers

import nin


parser = argparse.ArgumentParser(description='Image inspection using chainer')
parser.add_argument('image', help='Path to inspection image file')
parser.add_argument('--model','-m',default='model', help='Path to model file')
parser.add_argument('--labels','-l',default='labels.txt', help='Path to labels.txt file')
parser.add_argument('--mean', default='mean.npy', help='Path to the mean file (computed by compute_mean.py)')
args = parser.parse_args()

def read_image(path, center=False, flip=False):
  image = np.asarray(Image.open(path)).transpose(2, 0, 1)
  if center:
    top = left = cropwidth / 2
  else:
    top = random.randint(0, cropwidth - 1)
    left = random.randint(0, cropwidth - 1)
  bottom = model.insize + top
  right = model.insize + left
  image = image[:, top:bottom, left:right].astype(np.float32)
  image -= mean_image[:, top:bottom, left:right]
  image /= 255
  if flip and random.randint(0, 1) == 0:
    return image[:, :, ::-1]
  else:
    return image

mean_image = pickle.load(open(args.mean, 'rb'))

#cuda.init(0)


model = pickle.load(open(args.model,'rb'))
model.to_cpu()
cropwidth = 256 - model.insize

img = read_image(args.image)
x = np.ndarray((1, 3, model.insize, model.insize), dtype=np.float32)
x[0]=img

x=cuda.to_cpu(x)
score = model.predict(x)
score=cuda.to_cpu(score.data)

categories = np.loadtxt(open(args.labels, 'rb'), str, delimiter="\t")
print(type(score.data))
top_k = 20
prediction = zip(score[0].tolist(), categories)
prediction.sort(cmp=lambda x, y: cmp(x[0], y[0]), reverse=True)

for rank, (score, name) in enumerate(prediction[:top_k], start=1):
    print('#%d | %s | %4.1f%%' % (rank, name, score * 100))
