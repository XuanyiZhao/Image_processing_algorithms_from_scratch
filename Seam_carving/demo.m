% File Name: demo.m
% Author: Xuanyi Zhao
% Date: 10/23/2019

% Load the source image
I = imread('Philly.jpg');

nr = 66;
nc = 66;

[Ic, T] = carv(I, nr, nc);
