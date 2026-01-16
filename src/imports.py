import os, re
import pyglet
from pyglet.window import key
from pyglet import gl
import numpy as np
from pyglet.graphics.shader import Shader, ShaderProgram

import src.options as options
from src.shaders import VERT_SRC, FRAG_SRC_RAINBOW, FRAG_SRC_FILL
from src.math_utils import perspective, rotation_y, rotation_x, rotation_z, translation_matrix
from src.obj_loader import load_obj
from src.geometry import cube_vertices, cube_normals, cube_texcoords, cube_indices
