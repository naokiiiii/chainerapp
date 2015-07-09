import cPickle
import random
import argparse
import numpy as np
from chainer import cuda, Variable, FunctionSet, optimizers
import chainer.optimizers
import chainer.functions as F

# model difinition
model = FunctionSet(conv1=F.Convolution2D(3,32,3),
	bn1 = F.BatchNormalization(32),
	conv2=F.Convolution2D(32,64,3,pad=1),
	bn2 = F.BatchNormalization(64),
	conv3=F.Convolution2D(64,64,3,pad=1),
	fl4=F.Linear(1024, 256),
	fl5=F.Linear(256, 10))

def forward(x_data, y_data, train=True):
	x, t = Variable(x_data, volatile=not train), Variable(y_data, volatile=not train)
	h = F.max_pooling_2d(F.relu(model.bn1(model.conv1(x))), 2)
	h = F.max_pooling_2d(F.relu(model.bn2(model.conv2(h))), 2)
	h = F.max_pooling_2d(F.relu(model.conv3(h)), 2)
	h = F.dropout(F.relu(model.fl4(h)),train=train)
	y = model.fl5(h)

	return F.softmax_cross_entropy(y, t), F.accuracy(y, t)

# load image
def unpickle(file):
	fo = open(file, 'rb')
	dict = cPickle.load(fo)
	fo.close()
	
	return dict

# save learned NN parameter
def saveNetworkParameter(model):
	f = open('learnedNN.txt', 'w')
	cPickle.dump(model, f)
	f.close()
	
		
x_train = None
y_train = []

for i in xrange(1,2):
	data_dictionary = unpickle("cifar-10-batches-py/data_batch_%d" % i)
	
	if x_train == None:
		x_train = data_dictionary['data']
	else:
		x_train = np.vstack((x_train, data_dictionary['data']))
	
	y_train = y_train + data_dictionary['labels']

test_data_dictionary = unpickle("cifar-10-batches-py/test_batch")
x_test = test_data_dictionary['data']
x_test = x_test.reshape(len(x_test),3,32,32)
y_train = np.array(y_train)
x_train = x_train.reshape((len(x_train),3, 32, 32))
y_test = np.array(test_data_dictionary['labels'])

N = len(x_train)
N_test = len(x_test)

# sample param
N = 200
N_test = 50 

# parameter
n_epoch = 10 
batchsize = 100


gpu_flag = False
optimizer = optimizers.Adam()
optimizer.setup(model.collect_parameters())

for epoch in xrange(1, n_epoch+1):
	print 'epoch', epoch

	# training
	perm = np.random.permutation(N)
	sum_accuracy = 0
	sum_loss = 0
	for i in xrange(0, N, batchsize):
		x_batch = x_train[perm[i:i+batchsize]]
		y_batch = y_train[perm[i:i+batchsize]]
		if gpu_flag is True:
			x_batch = cuda.to_gpu(x_batch)
			y_batch = cuda.to_gpu(y_batch)

		optimizer.zero_grads()
		loss, acc = forward(x_batch, y_batch)
		loss.backward()
		optimizer.update()

		sum_loss     += float(cuda.to_cpu(loss.data)) * batchsize
		sum_accuracy += float(cuda.to_cpu(acc.data)) * batchsize
	print 'train mean loss={}, accuracy={}'.format(
		sum_loss / N, sum_accuracy / N)

	# evaluation
	sum_accuracy = 0
	sum_loss     = 0
	for i in xrange(0, N_test, batchsize):
		x_batch = x_test[i:i+batchsize]
		y_batch = y_test[i:i+batchsize]
		if gpu_flag is True:
			x_batch = cuda.to_gpu(x_batch)
			y_batch = cuda.to_gpu(y_batch)

		loss, acc = forward(x_batch, y_batch, train=False)

		sum_loss     += float(cuda.to_cpu(loss.data)) * batchsize
		sum_accuracy += float(cuda.to_cpu(acc.data)) * batchsize

	print 'test  mean loss={}, accuracy={}'.format(
		sum_loss / N_test, sum_accuracy / N_test)

	saveNetworkParameter(model)
