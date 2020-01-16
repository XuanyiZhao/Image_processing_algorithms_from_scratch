1. For the given testing source image, mask and background image, just run demo.py. It will complete the blending process and show the blended image.

2. For my own source images and background images:

1) Open demo.py

2) Change the location of source image and target image.

The given source file and target file are 1_source.jpg and 1_background.jpg. The mask of this source file is 1_mask.png.
The offset parameters of the given files are offsetX = 210, offsetY = 160

In addition, I also enclosed my own source images and background images. 
Their file names and corresponding offset parameters are as follows:
2_source.jpg | 2_background.jpg | 2_mask.png | offsetX = 100 | offsetY = 100
3_source.jpg | 3_background.jpg | 3_mask.png | offsetX = 200 | offsetY = 200
4_source.jpg | 4_background.jpg | 4_mask.png | offsetX = 100 | offsetY = 500

* Also, create_mask_byoneself.py can help to draw a mask for any images (point by point to draw the outline of source items).