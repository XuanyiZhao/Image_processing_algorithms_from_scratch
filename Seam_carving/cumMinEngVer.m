% File Name: cumMinEngVer.m
% Author: Xuanyi Zhao
% Date: 10/23/2019

function [Mx, Tbx] = cumMinEngVer(e)
% Input:
%   e is the energy map

% Output:
%   Mx is the cumulative minimum energy map along vertical direction.
%   Tbx is the backtrack table along vertical direction.

% Write Your Code Here
[e_r, e_c] = size(e);
Mx = zeros(e_r, e_c);

% Padding the cumulative minimum energy matrix in order to conveniently 
% calculate the minimum energy and the corresponding index, which I think is 
% more efficient than nested for-loop-calculation
Mx = padarray(Mx, [0,1], 50000, 'both');
Mx_c = size(Mx, 2);

Tbx = zeros(e_r, e_c);
Mx(1, 2:Mx_c - 1) = e(1, :);

% Calculate the minimum energy with moving-window
for i = 2:(e_r)
    [min_value, idx] = min([Mx(i - 1, 1:Mx_c - 2);
                            Mx(i - 1, 2:Mx_c - 1);
                            Mx(i - 1, 3:Mx_c)]);
    Mx(i, 2:Mx_c - 1) = e(i, :) + min_value;
    Tbx(i, :) = idx - 2;
end

% Undo padding in order to keep the size unchanged
Mx = Mx(:, 2:Mx_c - 1);
