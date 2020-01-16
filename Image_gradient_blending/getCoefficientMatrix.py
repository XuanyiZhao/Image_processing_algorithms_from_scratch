'''
  File name: getCoefficientMatrix.py
  Author: Xuanyi Zhao
  Date created: 09/28/2019
'''

import numpy as np


def getCoefficientMatrix(indexes):
	# Enter Your Code Here
	N = indexes.max()
	indexes_pad = np.pad(indexes, 1, 'constant', constant_values=0)
	coeffA = np.zeros((N, N))
	for i in range(1, N+1):
		r, c = np.where(indexes_pad == i)
		r = r[0]
		c = c[0]
		coeffA[i-1, i-1] = 4
		up = indexes_pad[r-1, c]
		down = indexes_pad[r+1, c]
		left = indexes_pad[r, c-1]
		right = indexes_pad[r, c+1]
		if up != 0:
			coeffA[i-1, up-1] = -1
		if down != 0:
			coeffA[i-1, down-1] = -1
		if left != 0:
			coeffA[i-1, left-1] = -1
		if right != 0:
			coeffA[i-1, right-1] = -1

	print('Finish getting coefficient matrix')
	return coeffA

