# get modules
import numpy as np

import random
import sys
sys.setrecursionlimit(15000)

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Circle, PathPatch
from matplotlib.path import Path

import seaborn as sns

import gif


np.random.seed(42)

# sns.set(style='dark')
sns.set(style='white')

N = 400

# (x = 0, y = range(0, N)), (x = N-1, y=range(0, N)), (x = range(0, N), y = 0), (x = range(0, N), y = N-1) 
# choose a cell randomly along any of the boundary
def choose_border_cells():
    bnd_cell = []
    
    bnd_cell.append((0, random.randint(0, N-1)))
    bnd_cell.append((N-1, random.randint(0, N-1)))
    bnd_cell.append((random.randint(0, N-1), 0))
    bnd_cell.append((random.randint(0, N-1), N-1))
    
    choose_i, choose_j = random.choice(bnd_cell)
    return choose_i, choose_j


# conditions - boundary limit
def conditions(x, y):
    return [x < 0, x > N-1, y < 0, y > N-1]


# choosing new coordinates from neighbor coordinates
def random_walk(current_i, current_j): 

    i, j = current_i, current_j
    coordinates = [(i-1, j-1), (i-1, j), (i-1, j+1), 
                   (i, j-1), (i, j+1),
                   (i+1, j-1), (i+1, j), (i+1, j+1)]

    res_coordinates = []

    for (x, y) in coordinates:
        condition = conditions(x, y)
        if any(condition):
            pass
        else:
            res_coordinates.append((x, y))
    #print(res_coordinates)
    new_i, new_j = random.choice(res_coordinates) 
    return new_i, new_j


# size of the simulator (total N^2 positions)
N = 400   # total pixels/positions = 160000

# zero to get a black background or one for white background and black point
x = np.zeros((N, N)) 

# starting point
x[int(N/2) - 1, int(N/2) - 1] = 1.0

# number of particles
K = 10000


# generate gif to visualize the progression 
@gif.frame
def plot(i):
    #choose_i, choose_j = choose_border_cells()
    prev_i, prev_j = choose_border_cells()
    # random walk returns new coordinates
    new_i, new_j = random_walk(prev_i, prev_j)
    #print(prev_i, prev_j)
    #print(new_i, new_j)
    
    while x[new_i, new_j] != 1.0:
        x[new_i, new_j] = 1.0
        x[prev_i, prev_j] = 0.0
        prev_i, prev_j = new_i, new_j
        new_i, new_j = random_walk(prev_i, prev_j)
    else:
        #print(prev_i, prev_j)
        x[prev_i, prev_j] = 1.0

    R = 20

    fig, ax = plt.subplots(figsize=(8, 8))
    circle = Circle((0, 0), R, facecolor='none', edgecolor=(0, 0, 0), linewidth=1, alpha=0.1)
    ax.add_patch(circle)

    im = plt.imshow(x,
                    origin='lower',
                    interpolation='none',
                    extent=([-1 * R, R, -1 * R, R]))

    im.set_clip_path(circle)
    ax.axis('off')
    plt.plot()
    
    #return x, count

# save frames
frames = []

for i in range(K):
    frame = plot(i)
    frames.append(frame)

gif.save(frames, 'temp.gif', duration=0.001)  # duration is in millisecond