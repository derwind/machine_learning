#! /usr/bin/env python
# -*- coding: utf-8 -*-

# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_transforms/py_fourier_transform/py_fourier_transform.html

import sys, os
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread(sys.argv[1], 0)
# FFT
f = np.fft.fft2(img)
f = np.fft.fftshift(f)
raw_mag = np.abs(f)

magnitude_spectrum = raw_mag
power_spectrum = raw_mag * raw_mag

plt.subplot(121), plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()
