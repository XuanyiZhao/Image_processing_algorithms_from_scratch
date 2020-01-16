'''
  File name: getIndexes.py
  Author: Xuanyi Zhao
  Date created: 09/28/2019
'''

import numpy as np

def getIndexes(mask, targetH, targetW, offsetX, offsetY):
    # Enter Your Code Here
    offsetX = int(offsetX)
    offsetY = int(offsetY)
    s1, s2 = mask.shape
    indexes = np.zeros((targetH, targetW), dtype='int')

    index = 1
    for i in range(offsetY, offsetY + s1):
        for j in range(offsetX, offsetX + s2):
            if mask[i-offsetY, j-offsetX] != 0:
                indexes[i, j] = index
                index += 1

    print ('Finish getting indexes')
    return indexes
