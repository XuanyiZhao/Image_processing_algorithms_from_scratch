'''
  File name: nonMaxSup.py
  Author:
  Date created:
'''

'''
  File clarification:
    Find local maximum edge pixel using NMS along the line of the gradient
    - Input Mag: H x W matrix represents the magnitude of derivatives
    - Input Ori: H x W matrix represents the orientation of derivatives
    - Output M: H x W binary matrix represents the edge map after non-maximum suppression
'''
import numpy as np

def nonMaxSup(Mag, Ori):
    # TODO: your code here
    angle = Ori
    angle[angle < 0] = np.pi + angle[angle < 0]
    angle[angle > 7 * np.pi / 8] = np.pi - angle[angle > 7 * np.pi / 8]
    angle[np.logical_and(angle >= 0, angle < np.pi / 8)] = 0
    angle[np.logical_and(angle >= np.pi / 8, angle < 3 * np.pi / 8)] = np.pi / 4
    angle[np.logical_and(angle >= 3 * np.pi / 8, angle < 5 * np.pi / 8)] = np.pi / 2
    angle[np.logical_and(angle >= 5 * np.pi / 8, angle <= 7 * np.pi / 8)] = 3 * np.pi / 4

    row, col = Mag.shape
    M = np.ones((row, col))

    G = np.pad(Mag, 1, 'constant', constant_values=0)

    for i in range(row):
        for j in range(col):
            if angle[i, j] == 0:
                if G[i+1, j+1] < G[i+1, j+2] or G[i+1, j+1] < G[i+1, j]:
                    M[i, j] = 0
            if angle[i, j] == np.pi / 4:
                if G[i+1, j+1] < G[i, j+2] or G[i+1, j+1] < G[i+2, j]:
                    M[i, j] = 0
            elif angle[i, j] == np.pi / 2:
                if G[i+1, j+1] < G[i, j+1] or G[i+1, j+1] < G[i+2, j+1]:
                    M[i, j] = 0
            elif angle[i ,j] == 3 * np.pi / 4:
                if G[i+1, j+1] < G[i, j] or G[i+1, j+1] < G[i+2, j+2]:
                    M[i, j] = 0

    return M
