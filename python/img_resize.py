# -*- coding: utf-8 -*-
import os
import sys
import cv2
import numpy as np

def resize_images(source_dir, target_dir):
    for image_file in os.listdir(source_dir):
        if image_file == '.DS_Store': #escape invisible file of Mac
            continue
        print "%s/%s"%(source_dir,image_file)
        src_image = cv2.imread("%s/%s"%(source_dir,image_file))
        dst_image = cv2.resize(src_image,(256,256))
        cv2.imwrite(target_dir+"/"+image_file, dst_image)

if __name__ == "__main__":
    resize_images(sys.argv[1], sys.argv[2])