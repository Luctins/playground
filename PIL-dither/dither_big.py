from PIL import Image

# from functools import reduce

import numpy as np


def pxmean(m, y0, x0, s):
    c = 0
    for _x in range(0, pxsize):
        for _y in range(0, pxsize):
            c += m[x0+_x, y_0+_y]

    return c/(s*2)


def set_blk(m, x0, y0, sq, val):
    for i in range(0, sq):
        for k in range(0, sq):
            px[x0+i, y0+k] = val


img = Image.open("grad.png")
px = img.load()
dm = [[0, 0, 7/16], [3/16, 5/16, 1/16]]

print(dm)
pxsize = 8

mat = np.matrix(
    [[np.matrix([[px[_x, _y][3] for _x in range(x, x+pxsize)]
                 for _y in range(y, y+pxsize)]).mean()
        for x in range(0, img.width, pxsize)]
               for y in range(0, img.height, pxsize)])

print('mat', mat.shape)

for x in range(1, mat.shape[1]-1):
    for y in range(1, mat.shape[0]-1):

        old = mat[y, x]
        new = 255 if old > 127 else 0
        mat[y, x] = new
        err = old - new

        for p in ((1, 0), (-1, 1), (0, 1), (1, 1)):
            mat[y+p[0], x+p[1]] += err * dm[p[1]][1+p[0]]

for x in range(1, mat.shape[1]-1):
    for y in range(0, mat.shape[0]-1):
        set_blk(px, (x)*pxsize, (y)*pxsize, pxsize,
                (21, 18, 36, int(mat[y, x])))

img.save("res.png")
