import numpy as np
import cv2


def getFeatures(img, bbox):
    # (INPUT) img: H x W matrix representing grayscale image
    # (INPUT) bbox: F x 4 x 2 matrix representing coordinates of F objects 
    # (OUTPUT) x: N × F matrix representing the N row features coordinates of F objects
    # (OUTPUT) y: N × F matrix representing the N col features coordinates of F objects

    F = bbox.shape[0]
    N = 20
    x = np.zeros([N, F], dtype=np.int)
    y = np.zeros([N, F], dtype=np.int)
    
    for i in range(F):
        x1, y1 = bbox[i, 0, :]
        x2, y2 = bbox[i, 1, :]
        x3, y3 = bbox[i, 2, :]
        x4, y4 = bbox[i, 3, :]
        x1 = int(x1); x2 = int(x2); x3 = int(x3); x4 = int(x4)
        y1 = int(y1); y2 = int(y2); y3 = int(y3); y4 = int(y4)

        minX = np.min([x1, x2, x3, x4])
        maxX = np.max([x1, x2, x3, x4])
        minY = np.min([y1, y2, y3, y4])
        maxY = np.max([y1, y2, y3, y4])
        window = img[minY:maxY, minX:maxX]

        corners = cv2.goodFeaturesToTrack(image=window,
                                          maxCorners=20,
                                          qualityLevel=0.02,
                                          minDistance=2)
        if corners.all() == None:
            corners = np.int0(corners)
        xi = []
        yi = []

        for j in corners:
            xi.append(j[0][0])
            yi.append(j[0][1])
        xi = xi + minX
        yi = yi + minY

        for j in range(len(xi)):
            d = np.sqrt((bbox[i, :, 0]-xi[j])**2 + (bbox[i, :, 1]-yi[j])**2)
            if np.min(d) < 2:
                xi[j] = 0
                yi[j] = 0

        order = np.argsort(xi, axis=0)
        order = order[::-1].squeeze()
        xi = xi[order]
        yi = yi[order]
        
        x[:len(xi), i] = xi
        y[:len(yi), i] = yi

    return x, y
