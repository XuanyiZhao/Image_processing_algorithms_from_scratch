import numpy as np
import cv2


def interp2(v, xq, yq):
	if len(xq.shape) == 2 or len(yq.shape) == 2:
		dim_input = 2
		q_h = xq.shape[0]
		q_w = xq.shape[1]
		xq = xq.flatten()
		yq = yq.flatten()

	h = v.shape[0]
	w = v.shape[1]
	if xq.shape != yq.shape:
		raise ('query coordinates Xq Yq should have same shape')


	x_floor = np.floor(xq).astype(np.int32)
	y_floor = np.floor(yq).astype(np.int32)
	x_ceil = np.ceil(xq).astype(np.int32)
	y_ceil = np.ceil(yq).astype(np.int32)

	x_floor[x_floor<0] = 0
	y_floor[y_floor<0] = 0
	x_ceil[x_ceil<0] = 0
	y_ceil[y_ceil<0] = 0

	x_floor[x_floor>=w-1] = w-1
	y_floor[y_floor>=h-1] = h-1
	x_ceil[x_ceil>=w-1] = w-1
	y_ceil[y_ceil>=h-1] = h-1

	v1 = v[y_floor, x_floor]
	v2 = v[y_floor, x_ceil]
	v3 = v[y_ceil, x_floor]
	v4 = v[y_ceil, x_ceil]

	lh = yq - y_floor
	lw = xq - x_floor
	hh = 1 - lh
	hw = 1 - lw

	w1 = hh * hw
	w2 = hh * lw
	w3 = lh * hw
	w4 = lh * lw

	interp_val = v1 * w1 + w2 * v2 + w3 * v3 + w4 * v4

	if dim_input == 2:
		return interp_val.reshape(q_h,q_w)
	return interp_val

def estimateFeatureTranslation(startX, startY, Ix, Iy, img1, img2):
    L = 25

    newX, newY = startX, startY
    mX, mY = np.meshgrid(np.arange(L),
                         np.arange(L))
    grayimg1 = cv2.cvtColor(src=img1,
                            code=cv2.COLOR_RGB2GRAY)
    grayimg2 = cv2.cvtColor(src=img2,
                            code=cv2.COLOR_RGB2GRAY)
    flatted_mX = mX.flatten('C')
    flatted_mY = mY.flatten('C')
    new_flatted_mX = newX + flatted_mX - np.floor(L/2)
    new_flatted_mY = newY + flatted_mY - np.floor(L/2)
    new_flatted_mX = new_flatted_mX.reshape((1, -1))
    new_flatted_mY = new_flatted_mY.reshape((1, -1))
    flatted_all = np.concatenate((new_flatted_mX,
                                  new_flatted_mY), axis=0)

    V = interp2(grayimg1,
                flatted_all[0, :].reshape((1, -1)),
                flatted_all[1, :].reshape((1, -1)))
    V_x = interp2(Ix,
                  flatted_all[0, :].reshape((1, -1)),
                  flatted_all[1, :].reshape((1, -1)))
    V_y = interp2(Iy,
                  flatted_all[0, :].reshape((1, -1)),
                  flatted_all[1, :].reshape((1, -1)))

    I = np.concatenate((V_x,
                        V_y), axis=0)
    A = np.dot(I, I.T)

    loop = 0

    # threshold = 10
    threshold = 18

    # threshold = 20

    while loop < threshold:

        tmp_flatted_mX = flatted_mX + newX - np.floor(L/2)
        tmp_flatted_mY = flatted_mY + newY - np.floor(L/2)
        tmp_flatted_mX = tmp_flatted_mX.reshape((1, -1))
        tmp_flatted_mY = tmp_flatted_mY.reshape((1, -1))
        flatted_all = np.concatenate((tmp_flatted_mX,
                                      tmp_flatted_mY), axis=0)
        V_2 = interp2(grayimg2,
                      flatted_all[[0], :],
                      flatted_all[[1], :])
        Ip = (V_2 - V).reshape((-1, 1))
        b = np.dot(-I, Ip)
        inv_A = np.linalg.inv(A)
        multiply = np.dot(inv_A, b)
        newX = newX + multiply[0, 0]
        newY = newY + multiply[1, 0]
        loop = loop + 1

    return newX, newY
