from mymosaic import seamblend
from mymosaic import plot_fea_mat_for_sets_of_pictures
from mymosaic import mosaicing_left_middle
from mymosaic import mosaicing_right_middle
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image

l = 200
r = 200

print("Start Image Stitching 1: Picture set 1")
img1 = np.array(Image.open('given/left.jpg').convert('RGB'))
img2 = np.array(Image.open('given/middle.jpg').convert('RGB'))
img3 = np.array(Image.open('given/right.jpg').convert('RGB'))

seamed_pictures1 = seamblend(img2, l, 1)
seamed_pictures2 = seamblend(seamed_pictures1, r, 2)
mapping1, mapping2 = mosaicing_left_middle(img2, img1, seamed_pictures2)
stitched1 = mosaicing_right_middle(mapping2, img3, mapping1)

plt.imshow(stitched1)
# plt.savefig('stitched1.jpg')
# flip the array to change the BRG to RGB in order to use cv2.imwrite to save the picture
cv2.imwrite('stitched1.jpg', np.flip(stitched1, 2))
plt.show()

print("Start Image Stitching 2: Picture set 2")
img1 = np.array(Image.open('my/left.jpg').convert('RGB'))
img2 = np.array(Image.open('my/middle.jpg').convert('RGB'))
img3 = np.array(Image.open('my/right.jpg').convert('RGB'))

seamed_pictures1 = seamblend(img2, l, 1)
seamed_pictures2 = seamblend(seamed_pictures1, r, 2)
mapping1, mapping2 = mosaicing_left_middle(img2, img1, seamed_pictures2)
stitched2 = mosaicing_right_middle(mapping2, img3, mapping1)

plt.imshow(stitched2)
# plt.savefig('stitched2.jpg')
# flip the array to change the BRG to RGB in order to use cv2.imwrite to save the picture
cv2.imwrite('stitched2.jpg', np.flip(stitched2, 2))
plt.show()

print("Start plotting feature matching of distinct frames")
path = 'pic_sets/'
value = plot_fea_mat_for_sets_of_pictures(path, 10)
