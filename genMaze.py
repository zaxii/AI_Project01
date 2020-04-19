import random
import numpy as np
import json
import math
import sys

XSIZE = 10
YSIZE = 10


def gen_path(w=10, h=10, maze=np.zeros((XSIZE, YSIZE)), path=np.zeros((XSIZE, YSIZE))):
    pt = np.array([0, 0])

    path[0][0] = 1
    while pt[0] < w - 1 and pt[1] < h - 1:
        if random.randint(0, 1) == 1:
            # right
            pt[1] += 1
            path[pt[0]][pt[1]] = 1
        else:
            pt[0] += 1
            path[pt[0]][pt[1]] = 1
    while pt[0] < w - 1:
        pt[0] += 1
        path[pt[0]][pt[1]] = 1
    while pt[1] < h - 1:
        pt[1] += 1
        path[pt[0]][pt[1]] = 1


def gen_block(num=5, maze=np.zeros((XSIZE, YSIZE)), path=np.zeros((XSIZE, YSIZE))):
    if num > 0.4 * XSIZE * YSIZE:
        num = math.floor(0.4 * XSIZE * YSIZE)
    count = 0
    while count < num:
        x, y = random.randint(0, XSIZE - 1), random.randint(0, YSIZE - 1)
        if path[x][y] == 0 and maze[x][y] == 0:
            maze[x][y] = -1
            count += 1


def gen_trap(num=3, maze=np.zeros((XSIZE, YSIZE)), path=np.zeros((XSIZE, YSIZE))):
    if num > 0.4 * XSIZE * YSIZE:
        num = math.floor(0.4 * XSIZE * YSIZE)
    count = 0
    while count < num:
        x, y = random.randint(0, XSIZE - 1), random.randint(0, YSIZE - 1)
        if path[x][y] == 0 and maze[x][y] == 0:
            maze[x][y] = -2
            count += 1


def gen_maze(block=5, trap=3):
    maze = np.zeros((10, 10))
    path = np.zeros((10, 10))
    gen_path(XSIZE, YSIZE, maze, path)
    gen_trap(trap, maze, path)
    gen_block(block, maze, path)
    maze[XSIZE - 1][YSIZE - 1] = 1
    mazelist = maze.tolist()
    with open('input.txt', "w+") as outfile:
        json.dump(mazelist, outfile)


if __name__ == '__main__':
    block = 5
    trap = 3
    if len(sys.argv) == 3:
        block = int(sys.argv[1])
        trap = int(sys.argv[2])
    gen_maze(block, trap)
