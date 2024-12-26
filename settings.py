import pygame as pg
import glm
import gc
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

import numpy as np
from numba import njit

# Window settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
ASP_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
NEAR = 0.1
FAR = 1000.0

CHUNK_SIZE = 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOLUME = CHUNK_AREA * CHUNK_SIZE

WORLD_WIDTH, WORLD_HEIGHT = 1, 1
WORLD_DEPTH = 2
WORLD_AREA = WORLD_WIDTH * WORLD_DEPTH
WORLD_VOLUME = WORLD_AREA * WORLD_HEIGHT 

CENTRE_XZ = (WORLD_WIDTH * CHUNK_SIZE)
CENTRE_Y = (WORLD_HEIGHT * CHUNK_SIZE)

# Player settings
PLAYER_POS = glm.vec3(WORLD_WIDTH * CHUNK_SIZE, WORLD_DEPTH * CHUNK_SIZE + 1, WORLD_HEIGHT * CHUNK_SIZE)
PLAYER_DIR = (-1, -1, -1)
PLAYER_SPEED = 0.005
PLAYER_SENSITIVITY = 0.5
PLAYER_FOV = 90

ROT_X = glm.rotate(glm.mat4(1), glm.radians(90), glm.vec3(1, 0, 0))
ROT_Y = glm.rotate(glm.mat4(1), glm.radians(90), glm.vec3(0, 1, 0))
ROT_Z = glm.rotate(glm.mat4(1), glm.radians(90), glm.vec3(0, 0, 1))

vertices = np.array([
    [-0.5, -0.5, 0.5,],
    [0.5, -0.5, 0.5,],
    [0.5, 0.5, 0.5,],
    [-0.5, 0.5, 0.5,],
], dtype=np.float32)
indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint8)