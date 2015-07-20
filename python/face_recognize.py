# -*- coding: utf-8 -*-
import os
import sys
import commands
import subprocess
import numpy as np
import cv2

cascade_path = '/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml'

# image_path = sys.argv[1]
color = (255, 255, 255) #白

def cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    return stdout.rstrip()

def recognize_face(image_file, source_dir, target_dir):
    #ファイル読み込み
    image = cv2.imread("%s/%s"%(source_dir, image_file))
    print "%s/%s"%(source_dir, image_file)
    #グレースケール変換
    image_gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    #カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    #物体認識（顔認識）の実行
    facerect = cascade.detectMultiScale(
                image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
    if len(facerect) <= 0:
        # cv2.imwrite("%s/%s"%(target_dir, image_file), image)
        print "can't recognize"
        return

    for rect in facerect:
        #cv2.imwrite('demo.jpg', image[rect])
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]

        # img[y: y + h, x: x + w]
        cv2.imwrite("%s/%s"%(target_dir, image_file), image[y:y+h, x:x+w])

def search_recursive(source_dir, target_dir):
    #subdir
    dirs = cmd("ls %s" % source_dir)
    sub_dirs = dirs.splitlines()
    for sub in sub_dirs:
        cmd("mkdir -p %s/%s" % (target_dir, sub))
        recognize_faces("%s/%s" % (source_dir, sub), "%s/%s" % (target_dir, sub))

def recognize_faces(source_dir, target_dir):

    for image_file in os.listdir(source_dir):
        if image_file == '.DS_Store': #escape invisible file of Mac
            continue
        # print image_file
        recognize_face(image_file, source_dir, target_dir)

if __name__ == "__main__":
    search_recursive(sys.argv[1], sys.argv[2])


