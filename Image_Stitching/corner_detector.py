'''
  File name: corner_detector.py
  Author: Xuanyi Zhao & Po-Yuan Wang
  Date created: 11/10/2019
'''

'''
  File clarification:
    Detects corner features in an image. You can probably find free “harris” corner detector on-line, 
    and you are allowed to use them.
    - Input img: H × W matrix representing the gray scale input image.
    - Output cimg: H × W matrix representing the corner metric matrix.
'''
import cv2
import numpy as np
    
def corner_detector(img):
    # Your Code Here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = np.float32(gray)
    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray, None)

    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    return dst, kp
