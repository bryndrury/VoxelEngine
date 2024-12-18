import pygame as pg
import glm
import gc
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

import numpy as np
from numba import njit

CHUNK_SIZE = 32
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOLUME = CHUNK_AREA * CHUNK_SIZE

ROT_X = glm.rotate(glm.mat4(1), glm.radians(90), glm.vec3(1, 0, 0))
ROT_Y = glm.rotate(glm.mat4(1), glm.radians(90), glm.vec3(0, 1, 0))
ROT_Z = glm.rotate(glm.mat4(1), glm.radians(90), glm.vec3(0, 0, 1))

# bottom face quad vertices
BOTTOM_FACE = np.array([
    [0, 0, 0,],
    [1, 0, 0,],
    [1, 0, 1,],
    [0, 0, 1,],
], dtype=np.float32)
BOTTOM_FACE_EBO = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

TOP_FACE = np.array([
    [0, 1, 0,],
    [1, 1, 0,],
    [1, 1, 1,],
    [0, 1, 1,],
], dtype=np.float32)
TOP_FACE_EBO = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

FRONT_FACE = np.array([
    [0, 0, 0,],
    [1, 0, 0,],
    [1, 1, 0,],
    [0, 1, 0,],
], dtype=np.float32)
FRONT_FACE_EBO = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

BACK_FACE = np.array([
    [0, 0, 1,],
    [1, 0, 1,],
    [1, 1, 1,],
    [0, 1, 1,],
], dtype=np.float32)
BACK_FACE_EBO = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

LEFT_FACE = np.array([
    [0, 0, 0,],
    [0, 0, 1,],
    [0, 1, 1,],
    [0, 1, 0,],
], dtype=np.float32)
LEFT_FACE_EBO = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

RIGHT_FACE = np.array([
    [1, 0, 0,],
    [1, 0, 1,],
    [1, 1, 1,],
    [1, 1, 0,],
], dtype=np.float32)
RIGHT_FACE_EBO = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)