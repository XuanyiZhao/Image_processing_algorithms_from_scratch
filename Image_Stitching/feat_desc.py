'''
  File name: feat_desc.py
  Author: Xuanyi Zhao & Po-Yuan Wang
  Date created: 11/10/2019
'''

'''
  File clarification:
    Extracting Feature Descriptor for each feature point. You should use the subsampled image around each point feature, 
    just extract axis-aligned 8x8 patches. Note that it’s extremely important to sample these patches from the larger 40x40 
    window to have a nice big blurred descriptor. 
    - Input img: H × W matrix representing the gray scale input image.
    - Input x: N × 1 vector representing the column coordinates of corners.
    - Input y: N × 1 vector representing the row coordinates of corners.
    - Outpuy descs: 64 × N matrix, with column i being the 64 dimensional descriptor (8 × 8 grid linearized) computed at location (xi , yi) in img.
'''
import cv2
import numpy as np
from scipy import ndimage

# def feat_desc(img, x, y):
def feat_desc(img, kp):
    # Your Code Here

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # sift = cv2.xfeatures2d.SIFT_create()
    # kp = sift.detect(gray, None)
    #
    # x_r, x_c = x.shape
    # descs = np.zeros((64, x_r), dtype=int)
    # img = np.pad(img, ((20, 20), (20, 20), (0, 0)), 'symmetric')
    # for i in range(x_r):
    #     patch1 = img[y[i, 0]+1:y[i, 0]+41, x[i, 0]+1:x[i, 0]+41]
    #     patch1 = ndimage.filters.gaussian_filter(patch1, sigma=1)
    #     print(patch1.shape)
    #     patch2 = patch1[0:40:5, 0:40:5]
    #     print(patch2.shape)
    #     patch2 = patch2.reshape((64, 3))
    #     patch2 = (patch2 - patch2.mean()) / patch2.std()
    #     descs[:, i] = patch2

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp, descs = sift.compute(gray, kp)

    return kp, descs
