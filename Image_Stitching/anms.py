'''
  File name: anms.py
  Author: Xuanyi Zhao & Po-Yuan Wang
  Date created: 11/10/2019
'''

'''
  File clarification:
    Implement Adaptive Non-Maximal Suppression. The goal is to create an uniformly distributed 
    points given the number of feature desired:
    - Input cimg: H × W matrix representing the corner metric matrix.
    - Input max_pts: the number of corners desired.
    - Outpuy x: N × 1 vector representing the column coordinates of corners.
    - Output y: N × 1 vector representing the row coordinates of corners.
    - Output rmax: suppression radius used to get max pts corners.
'''
import numpy as np

def anms(cimg, max_pts):
    # Your Code Here
    cimg = cimg.T
    r, c = cimg.shape
    low = min(r, c)
    mapping = np.zeros((r, c))

    dst_max = cimg.max() * 0.01
    x_point = []
    y_point = []
    for i in range(r):
        for j in range(c):
            if cimg[i, j] > dst_max:
                x_point.append(i)
                y_point.append(j)

    for k in range(len(x_point)):
        i = x_point[k]
        j = y_point[k]
        for radius in range(1, low+1):
            if cimg[i, j] == 0:
                mapping[i, j] = 1
                break
            if (np.sum(cimg[max(0, i-radius):min(r, i+radius+1), max(0, j-radius)] > cimg[i, j]) >= 1) \
                or (np.sum(cimg[max(0, i-radius):min(r, i+radius+1), min(c-1, j+radius)] > cimg[i, j]) >= 1) \
                or (np.sum(cimg[max(0, i-radius), max(0, j-radius):min(c, j+radius+1)] > cimg[i, j]) >= 1) \
                or (np.sum(cimg[min(r-1, i+radius), max(0, j-radius):min(c, j+radius+1)] > cimg[i, j]) >= 1):
                mapping[i, j] = radius
                break
    mapping_1d = np.reshape(mapping, (r * c, 1))
    mapping_1d_sorted = np.sort(mapping_1d, axis=0)
    mapping_1d_sorted_idx = np.argsort(mapping_1d, axis=0)
    rmax = mapping_1d_sorted[-max_pts]
    idx = mapping_1d_sorted_idx[-max_pts:]
    y = np.remainder(idx-1, r).astype(int)
    x = np.floor((idx-1)/r).astype(int)

    return x, y, rmax
    