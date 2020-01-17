function [im1_pts, im2_pts] = click_correspondences(im1, im2)
%CLICK_CORRESPONDENCES Find and return point correspondences between images
%   Input im1: target image
%	Input im2: source image
%	Output im1_pts: correspondence-coordiantes in the target image
%	Output im2_pts: correspondence-coordiantes in the source image

%% Your code goes here
% You can use built-in functions such as cpselect to manually select the
% correspondences
% Padding the pictures to be the same size
if (size(im1, 2) > size(im2, 2))
    im2 = padarray(im2, [0, size(im1, 2) - size(im2, 2), 0], 1, 'post'); 
end
if (size(im1, 2) < size(im2, 2))
    im1 = padarray(im1, [0, size(im2, 2) - size(im1, 2), 0], 1, 'post'); 
end
if (size(im1, 1) > size(im2, 1))
    im2 = padarray(im2, [size(im1, 1) - size(im2, 1), 0, 0], 1, 'post'); 
end
if (size(im1, 1) < size(im2, 1))
    im1 = padarray(im1, [size(im2, 1) - size(im1, 1), 0, 0], 1, 'post'); 
end

[im1_pts,im2_pts] = cpselect(im1, im2, 'Wait', true);
end