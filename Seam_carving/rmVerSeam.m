% File Name: rmVerSeam.m
% Author: Xuanyi Zhao
% Date: 10/23/2019

function [Ix, E] = rmVerSeam(I, Mx, Tbx)
% Input:
%   I is the image. Note that I could be color or grayscale image.
%   Mx is the cumulative minimum energy map along vertical direction.
%   Tbx is the backtrack table along vertical direction.

% Output:
%   Ix is the image removed one column.
%   E is the cost of seam removal

% Write Your Code Here
[I_r, I_c, I_t] = size(I);
Ix = zeros(I_r, I_c, I_t);

row_value = Mx(I_r, :);
% [E, idx] = min(row_value);
% Process the multiple maximum values
E = min(row_value);
idx_array = find(row_value == E);
idx = idx_array(1);

Ix(I_r, 1:(idx - 1), :) = I(I_r, 1:(idx - 1), :);
Ix(I_r, idx:I_c - 1, :) = I(I_r, idx + 1:I_c, :);

for i = 2:I_r
    idx = idx + Tbx(I_r - i + 2,idx);
    Ix(I_r - i + 1, 1:idx - 1, :) = I(I_r - i + 1, 1:idx - 1,:);
    Ix(I_r - i + 1, idx:I_c - 1, :) = I(I_r - i + 1, idx + 1:I_c, :);
end
end


