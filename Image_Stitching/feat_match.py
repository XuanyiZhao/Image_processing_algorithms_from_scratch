'''
  File name: feat_match.py
  Author: Xuanyi Zhao & Po-Yuan Wang
  Date created: 11/10/2019
'''

'''
  File clarification:
    Matching feature descriptors between two images. You can use k-d tree to find the k nearest neighbour. 
    Remember to filter the correspondences using the ratio of the best and second-best match SSD. You can set the threshold to 0.6.
    - Input descs1: 64 × N1 matrix representing the corner descriptors of first image.
    - Input descs2: 64 × N2 matrix representing the corner descriptors of second image.
    - Outpuy match: N1 × 1 vector where match i points to the index of the descriptor in descs2 that matches with the
                    feature i in descriptor descs1. If no match is found, you should put match i = −1.
'''
import cv2

def feat_match(des1, des2, kp1, kp2):

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE,
                        trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    knn_matches = flann.knnMatch(des1, des2, k=2) 
    
    good = []
    for m,n in knn_matches:
        if m.distance < 0.6 * n.distance:
            good.append(m)
    for i in good:
        newkp1 = i.queryIdx
        newkp2 = i.trainIdx

    x1 = []
    x2 = []
    y1 = []
    y2 = []

    for i in newkp1:
      x1.append(kp1[i].pt[0])
      y1.append(kp1[i].pt[1])
    for i in newkp2:
      x2.append(kp2[i].pt[0])
      y2.append(kp2[i].pt[1])

    return newkp1, newkp2, good, x1, x2, y1, y2
