'''
  File name: ransac_est_homography.py
  Author: Po-Yuan Wang & Xuanyi Zhao
  Date created: 11/10/2019
'''

'''
  File clarification:
    Use a robust method (RANSAC) to compute a homography. Use 4-point RANSAC as 
    described in class to compute a robust homography estimate:
    - Input x1, y1, x2, y2: N × 1 vectors representing the correspondences feature coordinates in the first and second image. 
                            It means the point (x1_i , y1_i) in the first image are matched to (x2_i , y2_i) in the second image.
    - Input thresh: the threshold on distance used to determine if transformed points agree.
    - Outpuy H: 3 × 3 matrix representing the homograph matrix computed in final step of RANSAC.
    - Output inlier_ind: N × 1 vector representing if the correspondence is inlier or not. 1 means inlier, 0 means outlier.
'''
from est_homography import est_homography
import numpy as np

def ransac_est_homography(x1, y1, x2, y2, thresh):
    cnt = 0
    x1_len = len(x1)

    for i in range(5000):
        idx = np.random.permutation(x1_len)
        idx = idx[0:4]
        H = est_homography(x1[idx], y1[idx], x2[idx], y2[idx])
        coord = np.dot(H, np.vstack((x1,
                                     y1,
                                     np.ones((1, x1_len)))))
        coord = coord[:2] / coord[2, :]
        V = np.vstack((x2,
                       y2))
        err = np.sqrt(np.sum(np.power((V - coord), 2), axis=0))
        index = np.argwhere(err < thresh)
        cnt2 = np.size(err[err < thresh])
        if cnt2 > cnt:
            cnt = cnt2
            inlier_ind = index
            H1 = H
    return H1, inlier_ind


