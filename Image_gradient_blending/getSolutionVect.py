'''
  File name: getSolutionVect.py
  Author: Xuanyi Zhao
  Date created: 09/28/2019
'''

import numpy as np


def getSolutionVect(indexes, source, target, offsetX, offsetY):
	# Enter Your Code Here
	N = indexes.max()

	up = 0
	down = 0
	left = 0
	right = 0

	SolVectorb = np.zeros((N))
	source = np.pad(source, 1, 'constant', constant_values=0)
	target = np.pad(target, 1, 'constant', constant_values=0)
	indexes_pad = np.pad(indexes, 1, 'constant', constant_values=0)

	for i in range(1, N+1):
		r, c = np.where(indexes_pad == i)
		if indexes_pad[r-1, c] == 0:
			up = target[r-1, c]
		if indexes_pad[r+1, c] == 0:
			down = target[r+1, c]
		if indexes_pad[r, c-1] == 0:
			left = target[r, c-1]
		if indexes_pad[r, c+1] == 0:
			right = target[r, c+1]
		r2 = r - offsetY
		c2 = c - offsetX

		SolVectorb[i-1] = 4 * source[r2, c2] - source[r2 - 1, c2] - source[r2 + 1, c2] - source[r2, c2-1] - source[r2, c2+1] \
		                    + up + down + left + right

		# reset up, down, left and right
		up = 0
		down = 0
		left = 0
		right = 0

	return SolVectorb
