import numpy as np

def perspective(fov, aspect, near, far):
    f = 1.0 / np.tan(fov / 2)
    nf = 1 / (near - far)
    return np.array([
        [f/aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) * nf, 2 * far * near * nf],
        [0, 0, -1, 0]
    ], dtype=np.float32)

def rotation_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def rotation_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def rotation_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ], dtype=np.float32)

def translation_matrix(offset):
    m = np.eye(4, dtype=np.float32)
    m[:3, 3] = offset
    return m


def look_at(eye, target, up=np.array([0.0, 1.0, 0.0], dtype=np.float32)):
    eye = np.array(eye, dtype=np.float32)
    target = np.array(target, dtype=np.float32)
    up = np.array(up, dtype=np.float32)

    forward = target - eye
    forward_norm = np.linalg.norm(forward)
    if forward_norm > 1e-8:
        forward /= forward_norm

    right = np.cross(forward, up)
    right_norm = np.linalg.norm(right)
    if right_norm > 1e-8:
        right /= right_norm

    up_dir = np.cross(right, forward)

    m = np.eye(4, dtype=np.float32)
    m[0, 0:3] = right
    m[1, 0:3] = up_dir
    m[2, 0:3] = -forward
    m[0:3, 3] = -m[0:3, 0:3] @ eye
    return m
