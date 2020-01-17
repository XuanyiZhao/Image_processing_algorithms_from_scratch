% File Name: carv.m
% Author: Xuanyi Zhao
% Date: 10/23/2019

function [Ic, T] = carv(I, nr, nc)
% Input:
%   I is the image being resized
%   [nr, nc] is the numbers of rows and columns to remove.
% 
% Output: 
% Ic is the resized image
% T is the transport map

% Write Your Code Here
[I_r, I_c, I_t] = size(I);
T = zeros(nr + 1, nc + 1);
[T_r, T_c] = size(T);
Ic = I;
% Initializing the array of array using cell in order to conveniently 
% output the video file
C{1,1} = I;
Path = zeros(nr + 1, nc + 1);

for i = 2:T_c
    e = genEngMap(Ic(:, 1:I_c - i + 2, :));
    [Mx, Tbx] = cumMinEngVer(e);
    [Ix, E] = rmVerSeam(Ic(:, 1:I_c - i + 2, :), Mx, Tbx);
    T(1, i) = E;
    Ic(:, 1:I_c - i + 2, :) = Ix;
    C{1,i} = Ic;
end

% Re-initializing the Ic
Ic = I;

for j = 2:T_r
    e = genEngMap(Ic(1:I_r - j + 2, :, :));
    [My, Tby] = cumMinEngHor(e);
    [Iy, E] = rmHorSeam(Ic(1:I_r - j + 2, :, :), My, Tby);
    T(j, 1) = E; 
    Ic(1:I_r -  j + 2, :, :) = Iy;
    C{j, 1} = Ic;
    Path(j, 1) = 1;
end


for k = 2:T_r
    for l = 2:T_c
        Ic_x = C{k, l - 1};
        Ic_y = C{k - 1, l};
        
        e_x = genEngMap(C{k - 1, l}(1:I_r - k + 2, 1:I_c - l + 1, :));
        e_y = genEngMap(C{k, l - 1}(1:I_r - k + 1, 1:I_c - l + 2, :));
        
        % Calculate the cumulative minimum energy, the backtrack table, 
        % the removed image and the cost of seam removal
        [My, Tby] = cumMinEngHor(e_x);
        [Iy, E_y] = rmHorSeam(Ic_y(1:I_r - k + 2, 1:I_c - l + 1, :), My, Tby);
        [Mx, Tbx] = cumMinEngVer(e_y);
        [Ix, E_x] = rmVerSeam(Ic_x(1:I_r - k + 1, 1:I_c - l + 2, :), Mx, Tbx);
        
        T(k, l) = min([E_y,E_x]);
        % Compare the seam removal cost, choose the smaller one
        if E_x <= E_y
            Ic_x(1:I_r - k + 1, 1:I_c - l + 2, :) = Ix;
            % Put the removed image into the cell
            C{k, l} = Ic_x;
        elseif E_x > E_y
            Ic_y(1:I_r - k + 2, 1:I_c - l + 1, :) = Iy;
            % Put the removed image into the cell
            C{k, l} = Ic_y;
            % Set the path index which is convenient for back-tracking
            Path(k, l) = 1;
        end
    end
end
% Return the resized image
Ic = C{end, end};

% Return the output files in order to create the video file
r_idx = nr + 1;
c_idx = nc + 1;

writeObj = VideoWriter('output.mp4', 'MPEG-4');
open(writeObj);
for i = 1:nr + nc
    output{nr + nc - i + 1} = C{r_idx, c_idx};
    if Path(r_idx, c_idx) == 1
        r_idx = r_idx - 1;
    elseif Path(r_idx, c_idx) == 0
        c_idx = c_idx - 1; 
    end
end

for k = 1:nr + nc
    writeVideo(writeObj, output{k});
end
close(writeObj);

end