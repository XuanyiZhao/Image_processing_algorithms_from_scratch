'''
  File name: mymosaic.py
  Author: Po-Yuan Wang & Xuanyi Zhao
  Date created: 11/10/2019
'''

'''
  File clarification:
    Produce a mosaic by overlaying the pairwise aligned images to create the final mosaic image. If you want to implement
    imwarp (or similar function) by yourself, you should apply bilinear interpolation when you copy pixel values. 
    As a bonus, you can implement smooth image blending of the final mosaic.
    - Input img_input: M elements numpy array or list, each element is a input image.
    - Outpuy img_mosaic: H × W × 3 matrix representing the final mosaic image.
'''
import numpy as np
import cv2
from corner_detector import corner_detector
from feat_desc import feat_desc
from feat_match import feat_match
from anms import anms
from ransac_est_homography import ransac_est_homography
import matplotlib.pyplot as plt
from PIL import Image
from genEngMap import genEngMap
from cumMinEngVer import cumMinEngVer

    

def plotting_pic(img1,img2):

    dst1, kp1 = corner_detector(img1)
    dst2, kp2 = corner_detector(img2)

    kp1, descs1 = feat_desc(img1, kp1)
    kp2, descs2 = feat_desc(img2, kp2)

    new_kp1, new_kp2, good, x1, x2, y1, y2 = feat_match(descs1, descs2, kp1, kp2)

    H, inlier_ind = ransac_est_homography(np.array(x1),
                                          np.array(y1),
                                          np.array(x2),
                                          np.array(y2), 2)

    corner_detector_plot1 = cv2.drawKeypoints(image=img1,
                                              keypoints=kp1,
                                              outImage=np.array([]),
                                              color=(255, 0, 0))
    corner_detector_plot2 = cv2.drawKeypoints(image=img2,
                                              keypoints=kp2,
                                              outImage=np.array([]),
                                              color=(255, 0, 0))

    index = list((inlier_ind.T[0]))
    good2 = []
    for i in index:
        good2.append(good[i])
    good = good2

    post_ransac_matching_plot = cv2.drawMatches(img1=img1,
                                                keypoints1=kp1,
                                                img2=img2,
                                                keypoints2=kp2,
                                                matches1to2=good,
                                                outImg=np.array([]),
                                                matchColor=(255, 0, 0),
                                                singlePointColor=(0, 0, 255),
                                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    plt.figure(1);plt.imshow(corner_detector_plot1)
    plt.figure(2);plt.imshow(corner_detector_plot2)
    plt.figure(3);plt.imshow(post_ransac_matching_plot)
    plt.show()

    return H

def plot_anms(img1, img2):
    dst1, kp1 = corner_detector(img1)
    dst2, kp2 = corner_detector(img2)

    x1, y1, rmax1 = anms(dst1, 2000)
    x2, y2, rmax2 = anms(dst2, 2000)
    for i in range(len(x1)):
        img1[int(x1[i]), int(y1[i])] = [255, 0, 0]
    for j in range(len(x2)):
        img2[int(x2[j]), int(y2[j])] = [255, 0, 0]
    plt.figure(4);plt.imshow(img1)
    plt.figure(5);plt.imshow(img2)
    plt.show()

    return 1


def plot_fea_mat_for_sets_of_pictures(path, num):
    for i in range(1, num+1):
        left_img = np.array(Image.open(path + str(i) + '_left.jpg').convert('RGB'))
        right_img = np.array(Image.open(path + str(i) + '_right.jpg').convert('RGB'))
        h_tmp = plotting_pic(left_img, right_img)
        print("plotting anms")
        anms_value = plot_anms(left_img, right_img)

    print ('Finished plotting the feature matching of at least five distinct frames')


def mosaicing_left_middle(img1, img2, seamed_picture):
    dst1, kp1 = corner_detector(img1)
    dst2, kp2 = corner_detector(img2)

    kp1, descs1 = feat_desc(img1, kp1)
    kp2, descs2 = feat_desc(img2, kp2)

    new_kp1, new_kp2, good, x1, x2, y1, y2 = feat_match(descs1, descs2, kp1, kp2)

    H, inlier_ind = ransac_est_homography(np.array(x1),
                                          np.array(y1),
                                          np.array(x2),
                                          np.array(y2), 2)
    img1_r, img1_c, l1 = img1.shape
    img2_r, img2_c, l2 = img2.shape
    X = np.array([[0, 0, img2_c - 1, img2_c - 1],
                  [0, img2_r - 1, 0, img2_r - 1],
                   4 * [1]])
    inversed_H = np.linalg.inv(H)
    X_t = np.dot(inversed_H, X)
    X_t = X_t / X_t[2]
    
    minx = np.floor(np.min(X_t[0]))
    minx = minx.astype(int)
    miny = np.floor(np.min(X_t[1]))
    miny = miny.astype(int)
    maxx = np.ceil(np.max(X_t[0]))
    maxx = maxx.astype(int)
    maxy = np.ceil(np.max(X_t[1]))
    maxy = maxy.astype(int)
    
    offset1 = -1 * min(np.array([0, miny, minx], dtype=int))
    offset2 = max(np.array([maxy-img2_r, maxx-img2_c], dtype=int))

    mapping = np.zeros((offset1 + offset2 + img1_r, offset1 + offset2 + img1_c, 3))
    mapping[offset1:offset1 + img1_r, offset1:offset1 + img1_c, :] = img1
    
    T = np.array([[1, 0, offset1],
                  [0, 1, offset1],
                  [0, 0, 1]])
    H_t = np.dot(T, inversed_H)

    w_r, w_c, w_l = mapping.shape
    warped_img = cv2.warpPerspective(src=img2,
                                     M=H_t,
                                     dsize=(w_c, w_r))

    mapping[offset1:offset1 + img1_r, offset1:img1_c+offset1, :] = seamed_picture
    
    warped_gt_0 = (np.sum(warped_img, axis=2) > 0)
    mapping_gt_0 = (np.sum(mapping, axis=2) > 0)

    for r in range(w_r):
        for c in range(w_c):
            if mapping_gt_0[r, c] != 0 and warped_gt_0[r, c] != 0:
                mapping[r, c, :] = mapping[r, c, :]
            elif warped_gt_0[r, c] != 0:
                mapping[r, c,:] = warped_img[r,c,:]
    mapping_1 = np.zeros((offset1 + img1_r + offset2, offset1 + img1_c + offset2, 3), dtype=np.uint8)
    mapping_1[offset1:offset1 + img1_r, offset1:offset1 + img1_c, :] = img1
    
    warped_1_gt_0 = (np.sum(warped_img, axis=2) > 0)
    mapping_1_gt_0 = (np.sum(mapping_1, axis=2) > 0)

    for r in range(offset1 + img1_r + offset2):
        for c in range(offset1 + img1_c + offset2):
            if mapping_1_gt_0[r, c] and warped_1_gt_0[r, c]:
                mapping_1[r, c, :] = mapping_1[r, c, :]
            elif warped_1_gt_0[r, c]:
                mapping_1[r, c, :] = warped_img[r, c, :]
    return mapping, mapping_1


def mosaicing_right_middle(img1, img2, warped_picture):
    dst1, kp1 = corner_detector(img1)
    dst2, kp2 = corner_detector(img2)

    kp1, descs1 = feat_desc(img1, kp1)
    kp2, descs2 = feat_desc(img2, kp2)

    new_kp1, new_kp2, good, x1, x2, y1, y2 = feat_match(descs1, descs2, kp1, kp2)

    H, inlier_ind = ransac_est_homography(np.array(x1),
                                          np.array(y1),
                                          np.array(x2),
                                          np.array(y2), 2)
    img1_r, img1_c, l1 = img1.shape
    img2_r, img2_c, l2 = img2.shape

    X = np.array([[0, 0, img2_c - 1, img2_c - 1],
                  [0, img2_r - 1, 0, img2_r - 1],
                   4 * [1]])
    inversed_H = np.linalg.inv(H)
    X_t = np.dot(inversed_H, X)
    X_t = X_t / X_t[2]
    
    minx = np.floor(np.min(X_t[0]))
    minx = minx.astype(int)
    miny = np.floor(np.min(X_t[1]))
    miny = miny.astype(int)
    maxx = np.ceil(np.max(X_t[0]))
    maxx = maxx.astype(int)
    maxy = np.ceil(np.max(X_t[1]))
    maxy = maxy.astype(int)
    
    pad_1 = -1 * min(np.array([0, miny, minx], dtype=int))
    pad_2 = max(np.array([maxy-img2_r, maxx-img2_c], dtype=int))

    mapping = np.zeros((pad_1 + pad_2 + img1_r, pad_1 + pad_2 + img1_c, 3), dtype=int)
    mapping[pad_1:pad_1 + img1_r, pad_1:pad_1 + img1_c, :] = img1
    
    T = np.array([[1, 0, pad_1],[0, 1, pad_1],[0, 0, 1],])
    H_t = np.dot(T, inversed_H)

    w_r, w_c, w_l = mapping.shape
    warped_img = cv2.warpPerspective(src=img2,
                                     M=H_t,
                                     dsize=(w_c, w_r))

    mapping[pad_1:pad_1 + img1_r, pad_1:pad_1 + img1_c, :] = warped_picture
    
    warped_gt_0 = (np.sum(warped_img, axis=2) > 0)
    mapping_gt_0 = (np.sum(mapping, axis=2) > 0)
    
    for r in range(pad_1 + pad_2 + img1_r):
        for c in range(pad_1 + pad_2 + img1_c):
            if mapping_gt_0[r, c] and warped_gt_0[r, c]:
                mapping[r, c, :] = mapping[r, c, :]
            elif warped_gt_0[r, c]:
                mapping[r, c, :] = warped_img[r, c, :]
    return mapping


def seamblend(img, wa, dir):
    if dir == 1:
        img_pk = img[:, 0:wa]
    elif dir == 2:
        img_pk = img[:, wa:]

    e = genEngMap(img_pk)
    Mx, Table = cumMinEngVer(e)
    r, c = Mx.shape
    E = min(Mx[r-1])
    Idx = []
    for i in range(c):
        if Mx[r-1][i] == E:
            Idx.append([r-1, i])
            break
    temporary = Idx[0]

    for i in reversed(range(r)):
        if Table[i][temporary[1]] == -1:
            temporary = [i-1, temporary[1]-1]
            Idx.append(temporary)
        if Table[i][temporary[1]] == 0:
            temporary = [i-1, temporary[1]]
            Idx.append(temporary)
        if Table[i][temporary[1]] == 1:
            temporary = [i-1, temporary[1]+1]
            Idx.append(temporary)

    Idx = sorted(Idx)
    MSK = np.zeros([r, c])

    for i in range(r):
        for j in range(c):
            if dir == 1 and j > Idx[i][1]:
                MSK[i][j] = 1
            if dir == 1 and j < Idx[i][1]:
                MSK[i][j] = 1
                
    IPK = np.copy(img_pk)
    for i in range(3):
        IPK[:, :, i] = IPK[:, :, i] * MSK
    
    I = np.copy(img)
    if dir == 1:
        I[:, 0:wa] = IPK
    elif dir == 2:
        I[:, wa:] = IPK
    return I

