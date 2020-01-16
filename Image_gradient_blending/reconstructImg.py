'''
  File name: reconstructImg.py
  Author: Xuanyi Zhao
  Date created: 09/28/2019
'''

import numpy as np

def reconstructImg(indexes, red, green, blue, targetImg):
    # Enter Your Code Here
    N = indexes.max()
    r_target = targetImg[:, :, 0]
    g_target = targetImg[:, :, 1]
    b_target = targetImg[:, :, 2]
    for i in range(1, N+1):
        r, c = np.where(indexes == i)
        r_target[r, c] = red[i-1]
        g_target[r, c] = green[i-1]
        b_target[r, c] = blue[i-1]

    resultImg = np.stack((r_target, g_target, b_target), axis=2)

    print ('Finish reconstructing image')
    return resultImg
