import sys
import commands
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--source_dir', '-s')
parser.add_argument('--target_dir', '-o')
parser.add_argument('--labels', '-l', default='train.txt')
parser.add_argument('--train', '-t', default='train.txt')
parser.add_argument('--test', '-e', default='test.txt')
args = parser.parse_args()

def cmd(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.wait()
	stdout, stderr = p.communicate()
	return stdout.rstrip()

#labels
dirs = cmd("ls %s" % args.source_dir)
labels = dirs.splitlines()

#make directries
cmd(args.target_dir)

#copy images and make train.txt
imageDir = args.target_dir
train = open(args.train, 'w')
test = open(args.test,'w')
labelsTxt = open(args.labels,'w')

classNo=0
cnt = 0
#label = labels[classNo]
for label in labels:
	workdir = "%s/%s" % (args.source_dir, label)
	imageFiles = cmd("ls %s/*.jpg" % workdir)
	images = imageFiles.splitlines()

	labelsTxt.write(label+"\n")
	startCnt=cnt
	length = len(images)

	for image in images:
		imagepath = "%s/image%07d.jpg" % (imageDir, cnt)
		#cmd("cp "+workdir+"/"+image+" "+imagepath)
		cmd("cp %s %s" % (image, imagepath))
		#print "cp "+image+" "+imagepath
		if cnt-startCnt < length*0.75:
			train.write("%s %d\n" % (imagepath, classNo))
		else:
			test.write("%s %d\n" % (imagepath, classNo))
		print imagepath
		cnt += 1

	classNo += 1

train.close()
test.close()
labelsTxt.close()
