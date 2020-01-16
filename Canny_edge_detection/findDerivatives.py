'''
  File name: findDerivatives.py
  Author:
  Date created:
'''

'''
  File clarification:
    Compute gradient information of the input grayscale image
    - Input I_gray: H x W matrix as image
    - Output Mag: H x W matrix represents the magnitude of derivatives
    - Output Magx: H x W matrix represents the magnitude of derivatives along x-axis
    - Output Magy: H x W matrix represents the magnitude of derivatives along y-axis
    - Output Ori: H x W matrix represents the orientation of derivatives
'''

import numpy as np
from scipy import signal

def findDerivatives(I_gray):
    # TODO: your code here
    # Gaussian filter definition
    # G = np.array([[2, 4, 5, 4, 2],
    #               [4, 9, 12, 9, 4],
    #               [5, 12, 15, 12, 5],
    #               [4, 9, 12, 9, 4],
    #               [2, 4, 5, 4, 2]])
    # G = 1/159 * G

    # dx, dy = np.gradient(G, axis = (1,0))
    dx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    dy = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    Magx = signal.convolve2d(I_gray, dx, 'same')
    Magy = signal.convolve2d(I_gray, dy, 'same')
    Mag = np.sqrt(Magx * Magx + Magy * Magy)
    Ori = np.arctan2(Magy, Magx)

    return Mag, Magx, Magy, Ori




