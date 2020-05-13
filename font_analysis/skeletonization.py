#! /usr/bin/env python
# -*- coding: utf-8 -*-

# http://opencvpython.blogspot.jp/2012/05/skeletonization-using-opencv-python.html

import sys, os
import cv2
import numpy as np

in_file  = sys.argv[1]
name, ext = os.path.splitext(in_file)
out_file = name + "_skeletonization" + ext

img = cv2.imread(in_file,0)
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)

ret,img = cv2.threshold(img,10,255,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
done = False

while( not done ):
    eroded = cv2.erode(img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(img,temp)
    skel = cv2.bitwise_or(skel,temp)
    img = eroded.copy()

    zeros = size - cv2.countNonZero(img)
    if zeros==size:
        done = True

cv2.imwrite(out_file, skel)
