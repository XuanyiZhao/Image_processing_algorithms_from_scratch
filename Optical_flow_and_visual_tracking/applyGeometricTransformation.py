
import cv2
import numpy as np
from skimage import transform 

def applyGeometricTransformation(stx_s, sty_s, newx_s, newy_s, bbox):
    n_object = bbox.shape[0]
    nwbox = np.zeros_like(bbox)
    x_s = newx_s.copy()
    y_s = newy_s.copy()
    for obj_idx in range(n_object):
        
        stxobj = stx_s[:,[obj_idx]]
        styobj = sty_s[:,[obj_idx]]

        newx_s_obj = newx_s[:,[obj_idx]]
        newy_s_obj = newy_s[:,[obj_idx]]
        desired_points = np.concatenate((stxobj, styobj), axis=1)
        actual_points = np.concatenate((newx_s_obj, newy_s_obj), axis=1)

        t = transform.SimilarityTransform()
        t.estimate(dst=actual_points, src=desired_points)
        mat = t.params


        inline_threshold = 1
        desired_points_one=np.ones([1,desired_points.shape[0]])
        stackmat=np.concatenate((desired_points.T.astype(float),
                                    desired_points_one),
                                    axis=0)
        PROJ = mat.dot(stackmat)
        
        inline_distance = np.square(PROJ[0:2,:].T - actual_points).sum(axis = 1)
        ACT_inline = actual_points[inline_distance < inline_threshold]
        DES_inline = desired_points[inline_distance < inline_threshold]
        # inline_num=5
        inline_num=4
        if np.shape(DES_inline)[0]<inline_num:
            
            ACT_inline = actual_points
            DES_inline = desired_points
        t.estimate(dst=ACT_inline, 
                    src=DES_inline)
        mat = t.params
        coords = np.vstack((bbox[obj_idx,:,:].T,
                            np.array([1,1,1,1])))
        new_coords = mat.dot(coords)
        nwbox[obj_idx,:,:] = new_coords[0:2,:].T
        x_s[inline_distance >= inline_threshold, obj_idx] = -1
        y_s[inline_distance >= inline_threshold, obj_idx] = -1
        Xs =x_s
        Ys =y_s
        newbbox =nwbox
    return Xs, Ys, newbbox

