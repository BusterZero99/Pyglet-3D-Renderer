import numpy as np

def perspective(fov, aspect, near, far):
    """Create a perspective projection matrix."""
    f = 1.0 / np.tan(fov / 2)
    return np.array([
        [f/aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
        [0, 0, -1, 0]
    ], dtype=np.float32)

def rotation_x(angle):
    """Rotation matrix around the X axis."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def rotation_y(angle):
    """Rotation matrix around the Y axis."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def rotation_z(angle):
    """Rotation matrix around the Z axis."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ], dtype=np.float32)

def translation_matrix(offset):
    """Translation matrix for a 3D offset (x,y,z)."""
    m = np.eye(4, dtype=np.float32)
    m[:3, 3] = offset
    return m
