%% Test_Script
test_im1 = ones([50, 50, 3]);
test_im2 = zeros([50, 50, 3]);

test_im1_pts = [1, 1; 1, 50; 50, 1; 50, 50; 25, 25];
test_im2_pts = [1, 1; 1, 50; 50, 1; 50, 50; 20, 20]; 

test_morphed_ims = morph_tri(test_im1, test_im2, test_im1_pts, test_im2_pts, .3, .3);
if size(test_morphed_ims, 1) ~= 1
	fprintf('Only outputs one image.\n');
end

test_morphed_im = test_morphed_ims{1};

if size(test_morphed_im, 3) ~= 3
	fprintf('What happened to color?\n');
end

if ~isequal(size(test_morphed_im), [50, 50, 3])
	fprintf('Something Wrong about the size of output image\n');
end


%% Image morphing and create the video
im1 = im2double(imread('p_source.jpg'));
im2 = im2double(imread('p_target.jpg'));
warp_frac = 0:1/59:1;
dissolve_frac = 0:1/59:1;

[im1_pts, im2_pts] = click_correspondences(im1, im2);

morphed_ims = morph_tri(im1, im2, im1_pts, im2_pts, warp_frac, dissolve_frac);

writerObj = VideoWriter('p_movie.avi');
open(writerObj);
for i= 1:size(warp_frac,2)
    writeVideo(writerObj, morphed_ims{i});
end
close(writerObj);
