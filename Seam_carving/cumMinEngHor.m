% File Name: cumMinEngHor.m
% Author: Xuanyi Zhao
% Date: 10/23/2019

function [My, Tby] = cumMinEngHor(e)
% Input:
%   e is the energy map.

% Output:
%   My is the cumulative minimum energy map along horizontal direction.
%   Tby is the backtrack table along horizontal direction.

% Write Your Code Here
[e_r, e_c] = size(e);
My = zeros(e_r, e_c);

% Padding the cumulative minimum energy matrix in order to conveniently 
% calculate the minimum energy and the corresponding index, which I think is 
% more efficient than nested for-loop-calculation
My = padarray(My, [1,0], 50000, 'both');
My_r = size(My, 1);

Tby = zeros(e_r, e_c);
My(2:My_r - 1, 1) = e(:, 1);

% Calculate the minimum energy with moving-window
for i = 2:e_c
    [min_value, idx] = min([transpose(My(1:My_r - 2, i - 1));
                            transpose(My(2:My_r - 1, i - 1));
                            transpose(My(3:My_r, i - 1))]);
    My(2:My_r - 1, i) = e(:, i) + transpose(min_value);
    Tby(:, i) = transpose(idx - 2);
end

% Undo padding in order to keep the size unchanged
My = My(2:My_r - 1, :);
