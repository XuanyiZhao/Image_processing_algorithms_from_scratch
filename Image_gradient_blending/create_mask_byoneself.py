from getIndexes import getIndexes
from getCoefficientMatrix import getCoefficientMatrix
from getSolutionVect import getSolutionVect
from reconstructImg import reconstructImg
from seamlessCloningPoisson import seamlessCloningPoisson


from drawMask import draw_mask
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import maskImage
import scipy.sparse.linalg as scilinalg
import scipy
from PIL import Image
from skimage.io import imsave
import argparse
import pdb

# Choose the source file and the target file
'''
The given source file and target file are 1_source.jpg and 1_background.jpg.
The offset parameters of the given files are offsetX = 210, offsetY = 160

In addition, I also enclosed my own source images and background images. 
Their file names and corresponding offset parameters are as follows:
2_source.jpg | 2_background.jpg | offsetX = 100 | offsetY = 100
3_source.jpg | 3_background.jpg | offsetX = 200 | offsetY = 200
4_source.jpg | 4_background.jpg | offsetX = 100 | offsetY = 500
'''
source_file = '1_source.jpg'
target_file = '1_background.jpg'

# Create Mask
image_file = source_file
file_name = image_file.split('.')[0].split('_')[0]
img = Image.open(image_file).convert('RGB')
img = np.array(img)
output_name = file_name
mask = maskImage.maskImage(img, output_name)


sourceImg = np.array(Image.open(source_file).convert('RGB'), dtype='float64')
targetImg = np.array(Image.open(target_file).convert('RGB'), dtype='float64')

offsetX = input('Enter the X offset')
offsetY = input('Enter the Y offset')

resultImg = seamlessCloningPoisson(sourceImg, targetImg, mask, offsetX, offsetY)

resultImg = resultImg.astype('int')

plt.figure()
plt.imshow(resultImg)

plt.show()
