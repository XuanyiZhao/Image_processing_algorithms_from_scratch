'''
  File name: seamlessCloningPoisson.py
  Author: Xuanyi Zhao
  Date created: 09/28/2019
'''

from scipy import sparse
import numpy as np

from getIndexes import getIndexes
from getCoefficientMatrix import getCoefficientMatrix
from getSolutionVect import getSolutionVect
from reconstructImg import reconstructImg

def seamlessCloningPoisson(sourceImg, targetImg, mask, offsetX, offsetY):
	# Enter Your Code Here
	r_source = sourceImg[:, :, 0]
	g_source = sourceImg[:, :, 1]
	b_source = sourceImg[:, :, 2]
	r_target = targetImg[:, :, 0]
	g_target = targetImg[:, :, 1]
	b_target = targetImg[:, :, 2]
	targetH, targetW, z = targetImg.shape
	indexes = getIndexes(mask, targetH, targetW, offsetX, offsetY)
	coeffA = getCoefficientMatrix(indexes)

	r_b = getSolutionVect(indexes, r_source, r_target, offsetX, offsetY)
	g_b = getSolutionVect(indexes, g_source, g_target, offsetX, offsetY)
	b_b = getSolutionVect(indexes, b_source, b_target, offsetX, offsetY)


	red = sparse.linalg.spsolve(coeffA, r_b)
	green = sparse.linalg.spsolve(coeffA, g_b)
	blue = sparse.linalg.spsolve(coeffA, b_b)

	red = np.clip(red, 0, 255)
	green = np.clip(green, 0, 255)
	blue = np.clip(blue, 0, 255)

	resultImg = reconstructImg(indexes, red, green, blue, targetImg)

	print('Finish seamless cloning poisson')
	return resultImg


