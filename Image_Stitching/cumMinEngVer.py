'''
  File name: cumMinEngVer.py
  Author: Xuanyi Zhao & Po-Yuan Wang
  Date created: 11/10/2019
'''

'''
  File clarification:
    Computes the cumulative minimum energy over the vertical seam directions.
    
    - INPUT e: n × m matrix representing the energy map.
    - OUTPUT Mx: n × m matrix representing the cumulative minimum energy map along vertical direction.
    - OUTPUT Tbx: n × m matrix representing the backtrack table along vertical direction.
'''
# from tqdm import trange
import numpy as np
# from numba import jit

# @jit 
def cumMinEngVer(e):
  # Your Code Here 
    r, c = e.shape
    energy_map=e

    M = energy_map.copy()
    backtrack = np.zeros_like(M, dtype=np.int)
    Mx=np.zeros([r,c])
    Tbx=np.zeros([r,c])
    Mx[0]=e[0]

    for i in range(1, r):
        for j in range(0, c):
            if j == 0:
                idx = np.argmin(M[i-1, j:j + 2])
                backtrack[i, j] = idx + j
                min_energy = M[i-1, idx + j]
                ## new calc tbx
                Min=min(Mx[i-1][j],Mx[i-1][j+1])
                Mx[i][j]=Min+e[i][j]
                if Mx[i-1][j]==Min:
                    Tbx[i][j]=0
                else:
                    Tbx[i][j]=1
            elif j==c-1:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]
                ## new calc tbx
                Min=min(Mx[i-1][j-1],Mx[i-1][j])
                Mx[i][j]=Min+e[i][j]
                if Mx[i-1][j-1]==Min:
                    Tbx[i][j]=-1
                else:
                    Tbx[i][j]=0
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]
                ## new calc
                Min=min(Mx[i-1][j-1],Mx[i-1][j],Mx[i-1][j+1])
                Mx[i][j]=Min+e[i][j]
                if Mx[i-1][j-1]==Min:
                    Tbx[i][j]=-1
                elif Mx[i-1][j]==Min:
                    Tbx[i][j]=0
                else:
                    Tbx[i][j]=1

            M[i, j] += min_energy

    Mx=M

    return Mx, Tbx
