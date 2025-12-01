import numpy as np

cube_vertices = np.array([
    -1,-1,-1,  1,-1,-1,  1, 1,-1, -1, 1,-1,
    -1,-1, 1,  1,-1, 1,  1, 1, 1, -1, 1, 1
],dtype=np.float32)

cube_normals = np.tile([0,0,1], 8).astype(np.float32)
cube_texcoords = np.tile([0,0], 8).astype(np.float32)

cube_indices = np.array([
    0,1,2,2,3,0, 4,5,6,6,7,4,
    0,4,7,7,3,0, 1,5,6,6,2,1,
    3,2,6,6,7,3, 0,1,5,5,4,0
],dtype=np.uint32)
