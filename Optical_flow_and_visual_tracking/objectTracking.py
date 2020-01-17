import cv2
import numpy as np
from getFeatures import getFeatures
from estimateAllTranslation import estimateAllTranslation
from applyGeometricTransformation import applyGeometricTransformation


def objectTracking(rawVideo, level):

    if level == 0:
        iter = 370
        file_name='easy.avi'
    elif level == 1:
        iter = 430
        file_name='medium.avi'

    frame = np.empty(iter, dtype=object)
    frames = np.empty(iter, dtype=object)
    bbox = np.empty(iter, dtype=object)
    for i in range(iter):
        _, frame[i] = rawVideo.read()

    if level == 0:
        bbox[0] = np.empty((3, 4, 2), dtype=float)
        bbox[0][0, :, :] = np.array([[308, 200], [384, 200], [308, 255], [384, 255]]).astype(float)
        bbox[0][1, :, :] = np.array([[231, 132], [272, 132], [231, 165], [272, 165]]).astype(float)
        bbox[0][2, :, :] = np.array([[272, 88], [303, 88], [272, 112], [303, 112]]).astype(float)

    elif level == 1:
        bbox[0] = np.array([[[486, 200], [527, 200],
                             [486, 270], [527, 270]]]).astype(float)
    
    out = cv2.VideoWriter(filename=file_name,
                          apiPreference=0,
                          fourcc=cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                          fps=20.0,
                          frameSize=(frame[0].shape[1], frame[0].shape[0]))

    startXs, startYs = getFeatures(img=cv2.cvtColor(src=frame[0],
                                                    code=cv2.COLOR_RGB2GRAY),
                                   bbox=bbox[0])
    for i in range(1, iter):
        newXs, newYs = estimateAllTranslation(startXs, startYs, frame[i-1], frame[i])
        Xs, Ys, newbbox = applyGeometricTransformation(startXs, startYs, newXs, newYs, bbox[i-1])
        print(i)
        startXs = Xs
        startYs = Ys
        bbox[i] = newbbox

        remaining_features = np.sum(startXs != -1)
        if remaining_features < 15:
            startXs, startYs = getFeatures(img=cv2.cvtColor(src=frame[i],
                                                            code=cv2.COLOR_RGB2GRAY),
                                           bbox=bbox[i])

        frames[i] = frame[i].copy()
        if level == 1:
            x_l, y_l, width, height = cv2.boundingRect(points=bbox[i][0, :, :].astype(int))
            # draw rectangle
            frames[i] = cv2.rectangle(img=frames[i],
                                      pt1=(x_l, y_l),
                                      pt2=(x_l + width, y_l + height),
                                      color=(0, 255, 0),  # Green Rectangle
                                      thickness=2)

            # draw feature points
            for j in range(startXs.shape[0]):
                center_x = int(startXs[j, 0])
                center_y = int(startYs[j, 0])
                frames[i] = cv2.circle(img=frames[i],
                                       center=(center_x, center_y),
                                       radius=3,
                                       color=(0, 255, 255),  # Yellow Points
                                       thickness=-1)
        elif level == 0:
            for j in range(3):
                x_l, y_l, width, height = cv2.boundingRect(points=bbox[i][j, :, :].astype(int))
                # draw rectangle
                frames[i] = cv2.rectangle(img=frames[i], pt1=(x_l, y_l), pt2=(x_l + width, y_l + height),
                                          color=(0, 255, 0),  # Green Rectangle
                                          thickness=2)

                # draw feature points
                for k in range(startXs.shape[0]):
                    center_x = int(startXs[k, j])
                    center_y = int(startYs[k, j])
                    frames[i] = cv2.circle(img=frames[i], center=(center_x, center_y), radius=3, color=(0, 255, 255),
                                           # Yellow Points
                                           thickness=-1)

        cv2.imshow("real_time_playing", frames[i])
        cv2.waitKey(15)
        out.write(frames[i])
    
    out.release()
