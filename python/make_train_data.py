import sys
import commands
import subprocess

def cmd(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.wait()
	stdout, stderr = p.communicate()
	return stdout.rstrip()

#labels
data_dir = sys.argv[1]
dirs = cmd("ls %s/mstimages" % data_dir)
labels = dirs.splitlines()

#make directries
cmd("mkdir %s/images" % data_dir)

#copy images and make train.txt
imageDir = "%s/images" % data_dir
train = open("%s/train.txt" % data_dir,'w')
test = open("%s/test.txt" % data_dir,'w')
labelsTxt = open("%s/labels.txt" % data_dir,'w')

classNo=0
cnt = 0
#label = labels[classNo]
for label in labels:
	workdir = "%s/mstimages/%s" % (data_dir, label)
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
