%% Image Morphing
im1 = ones([50, 50, 3]);
im2 = zeros([50, 50, 3]);

im1_pts = [1, 1; 1, 50; 50, 1; 50, 50; 25, 25];
im2_pts = [1, 1; 1, 50; 50, 1; 50, 50; 20, 20]; 

morphed_ims = morph_tri(im1, im2, im1_pts, im2_pts, .3, .3);
if size(morphed_ims, 1) ~= 1
	fprintf('Only outputs one image.\n');
end

morphed_im = morphed_ims{1};

if size(morphed_im, 3) ~= 3
	fprintf('What happened to color?\n');
end

if ~isequal(size(morphed_im), [50, 50, 3])
	fprintf('Something Wrong about the size of output image\n');
end
