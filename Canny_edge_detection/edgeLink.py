'''
  File name: edgeLink.py
  Author:
  Date created:
'''

'''
  File clarification:
    Use hysteresis to link edges based on high and low magnitude thresholds
    - Input M: H x W logical map after non-max suppression
    - Input Mag: H x W matrix represents the magnitude of gradient
    - Input Ori: H x W matrix represents the orientation of gradient
    - Output E: H x W binary matrix represents the final canny edge detection map
'''
import numpy as np

def edgeLink(M, Mag, Ori):
    # TODO: your code here
    upper_thresh = 0.175 * Mag.max()
    lower_thresh = 0.035 * Mag.max()

    row, col = Ori.shape
    E = np.zeros((row, col))
    X = np.pad(Mag, 1, 'constant', constant_values=0)

    for i in range(row):
        for j in range(col):
            if M[i, j] == 1:
                if X[i+1, j+1] >= upper_thresh:
                    E[i, j] = 1
                elif X[i+1, j+1] < upper_thresh and X[i+1, j+1] >= lower_thresh:
                    if X[i, j+1] >= upper_thresh or X[i+2, j+1] >= upper_thresh or X[i+1, j] >= upper_thresh or X[i+1, j+2] >= upper_thresh:
                        E[i, j]= 1
                else:
                    E[i ,j] = 0
            else:
                E[i, j] = 0

    return E
