% File Name: rmHorSeam.m
% Author: Xuanyi Zhao
% Date: 10/23/2019

function [Iy, E] = rmHorSeam(I, My, Tby)
% Input:
%   I is the image. Note that I could be color or grayscale image.
%   My is the cumulative minimum energy map along horizontal direction.
%   Tby is the backtrack table along horizontal direction.

% Output:
%   Iy is the image removed one row.
%   E is the cost of seam removal

% Write Your Code Here
[I_r, I_c, I_t] = size(I);
Iy = zeros(I_r, I_c, I_t);

col_value = My(:, I_c);
[E, idx] = min(col_value);

Iy(1:idx - 1, I_c, :) = I(1:idx - 1, I_c, :);
Iy(idx:I_r - 1, I_c, :) = I(idx + 1:I_r, I_c, :);

for i = 2:I_c
    idx = idx + Tby(idx, I_c - i + 2);
    Iy(1:idx - 1, I_c - i + 1, :) = I(1:idx - 1, I_c - i + 1, :);
    % Avoid the corner case
    if idx < I_r
        Iy(idx:I_r - 1, I_c - i + 1, :) = I(idx + 1:I_r, I_c - i + 1, :);
    end
end
end
