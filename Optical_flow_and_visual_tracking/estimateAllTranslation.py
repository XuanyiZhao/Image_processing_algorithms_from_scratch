import numpy as np
import cv2
from estimateFeatureTranslation import estimateFeatureTranslation


def estimateAllTranslation(startXs, startYs, img1, img2):
    grayimg = cv2.cvtColor(src=img1,
                           code=cv2.COLOR_RGB2GRAY)
    blurred_img = cv2.GaussianBlur(src=grayimg,
                                   ksize=(3, 3),
                                   sigmaX=0.5)
    Iy, Ix = np.gradient(blurred_img.astype(float))

    flatted_X = startXs.flatten('C')
    flatted_Y = startYs.flatten('C')
    newXs = -np.ones((flatted_X.shape), dtype=float)
    newYs = -np.ones((flatted_Y.shape), dtype=float)

    for i in range(len(flatted_X)):
        if flatted_X[i] != -1:
            newXs[i], newYs[i] = estimateFeatureTranslation(flatted_X[i], flatted_Y[i],
                                                            Ix,
                                                            Iy,
                                                            img1,
                                                            img2)
    newXs = newXs.reshape(startXs.shape)
    newYs = newYs.reshape(startYs.shape)
    return newXs, newYs
