#!/usr/bin/env python
"""Example code of learning a large scale convnet from ILSVRC2012 dataset.

Prerequisite: To run this example, crop the center of ILSVRC2012 training and
validation images and scale them to 256x256, and make two lists of space-
separated CSV whose first column is full path to image and second column is
zero-origin label (this format is same as that used by Caffe's ImageDataLayer).

"""
from __future__ import print_function
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


class Inspection():
	
	cropwidth = None
	model = None
	mean_image = None

	DATA_PATH = '/var/opt/t4j/chainer-data/'

	def read_image(self, path, center=False, flip=False):
		image = np.asarray(Image.open(path)).transpose(2, 0, 1)
		if center:
			top = left = cropwidth / 2
		else:
			top = random.randint(0, self.cropwidth - 1)
			left = random.randint(0, self.cropwidth - 1)
		bottom = self.model.insize + top
		right = self.model.insize + left
		image = image[:, top:bottom, left:right].astype(np.float32)
		image -= self.mean_image[:, top:bottom, left:right]
		image /= 255
		if flip and random.randint(0, 1) == 0:
			return image[:, :, ::-1]
		else:
			return image

	def execute(self, imgfile, modelfile=DATA_PATH+'model/model', labelsfile=DATA_PATH+'labels.txt',meanfile=DATA_PATH+'mean.npy'):
		self.mean_image = pickle.load(open(meanfile, 'rb'))

		self.model = pickle.load(open(modelfile, 'rb'))
		self.model.to_cpu()

		self.cropwidth = 256 - self.model.insize

		img = self.read_image(imgfile)
		x = np.ndarray((1, 3, self.model.insize, self.model.insize), dtype=np.float32)
		x[0]=img

		x=cuda.to_cpu(x)
		score = self.model.predict(x)
		score=cuda.to_cpu(score.data)

		categories = np.loadtxt(open(labelsfile, 'rb'), str, delimiter="\t")
		top_k = 20
		prediction = zip(categories, score[0].tolist())
		prediction.sort(cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)
		return prediction
		#for rank, (score, name) in enumerate(prediction[:top_k], start=1):
		#	print('#%d | %s | %4.1f%%' % (rank, name, score * 100))
