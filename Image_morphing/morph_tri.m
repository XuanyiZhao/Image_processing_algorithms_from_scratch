function [morphed_im] = morph_tri(im1, im2, im1_pts, im2_pts, warp_frac, dissolve_frac)
%MORPH_TRI Image morphing via Triangulation
%	Input im1: target image
%	Input im2: source image
%	Input im1_pts: correspondences coordiantes in the target image
%	Input im2_pts: correspondences coordiantes in the source image
%	Input warp_t_frac: a vector contains warp_ting parameters
%	Input dissolve_t_frac: a vector contains cross dissolve_t parameters
% 
%	Output morphed_im: a set of morphed images obtained from different warp_t and dissolve_t parameters

% Helpful functions: delaunay, tsearchn

[im1_s1, im1_s2] = size(im1);
[im2_s1, im2_s2] = size(im2);

if (im1_s2 > im2_s2)
    im2 = padarray(im2, [0, im1_s2 - im2_s2, 0], 1, 'post'); 
end
if (im1_s2 < im2_s2)
    im1 = padarray(im1, [0, im2_s2 - im1_s2, 0], 1, 'post'); 
end
if (im1_s1 > im2_s1)
    im2 = padarray(im2, [im1_s1 - im2_s1, 0, 0], 1, 'post'); 
end
if (im1_s1 < im2_s1)
    im1 = padarray(im1, [im2_s1 - im1_s1, 0, 0], 1, 'post'); 
end

warp_frac = 1 - warp_frac;
dissolve_frac = 1 - dissolve_frac;
tri = delaunay(im1_pts(:,1),im1_pts(:,2));

for i = 1:size(tri,1)
    for j = 1:3
        for k = 1:2
            tri1{k}(i,j) = im1_pts(tri(i,j), k);
        end
    end
end

for i = 1:size(tri,1)
    for j = 1:3
        for k = 1:2
            tri2{k}(i,j) = im2_pts(tri(i,j), k);
        end
    end
end

for i = 1:size(warp_frac,2)
    warp_t = warp_frac(i);
    dissolve_t = dissolve_frac(i);
    dissolved = dissolve_t * im1 + (1 - dissolve_t) * im2;
    x = warp_t * im1_pts(:,1) + (1 - warp_t) * im2_pts(:,1);
    y = warp_t * im1_pts(:,2) + (1 - warp_t) * im2_pts(:,2);

    for j = 1:size(tri,1)
        tmp_x = [x(tri(j,1)), x(tri(j,2)), x(tri(j,3))];
        tmp_y = [y(tri(j,1)), y(tri(j,2)), y(tri(j,3))];
        minx = floor(min(tmp_x));
        maxx = ceil(max(tmp_x));
        miny = floor(min(tmp_y));
        maxy = ceil(max(tmp_y));

        for ii = minx:maxx
            for jj = miny:maxy
                cord = [ii,jj];
                [t, p] = tsearchn([x,y], tri(j,:), cord);
                p = p';
                if t == 1
                    xs1 = round(tri1{1}(j,:) * p);
                    ys1 = round(tri1{2}(j,:) * p);
                    xs2 = round(tri2{1}(j,:) * p);
                    ys2 = round(tri2{2}(j,:) * p);

                    dissolved(jj,ii,:) = dissolve_t * im1(ys1,xs1,:) + (1 - dissolve_t) * im2(ys2,xs2,:);
                end
            end
        end
    end
    morphed_im{i} = dissolved;
end
end