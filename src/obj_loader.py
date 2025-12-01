import numpy as np

def load_obj(path):
    verts, norms, texs, faces = [], [], [], []
    with open(path, "r") as f:
        for line in f:
            if line.startswith("v "):
                _, x, y, z = line.strip().split()
                verts.append([float(x), float(y), float(z)])
            elif line.startswith("vn "):
                _, x, y, z = line.strip().split()
                norms.append([float(x), float(y), float(z)])
            elif line.startswith("vt "):
                parts = line.strip().split()
                u, v = parts[1], parts[2]
                texs.append([float(u), float(v)])
            elif line.startswith("f "):
                parts = line.strip().split()[1:]
                idxs = []
                for p in parts:
                    vals = p.split("/")
                    try:
                        v_i = int(vals[0]) - 1 if vals[0] else None
                        t_i = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else None
                        n_i = int(vals[2]) - 1 if len(vals) > 2 and vals[2] else None
                        idxs.append((v_i, t_i, n_i))
                    except Exception:
                        # 👇 Debug print goes here
                        print("Bad face line:", line.strip())
                # triangulate faces
                for i in range(1, len(idxs) - 1):
                    faces.extend([idxs[0], idxs[i], idxs[i + 1]])

    pos, nrm, uv = [], [], []
    for v_i, t_i, n_i in faces:
        pos.extend(verts[v_i])
        if n_i is not None and n_i < len(norms):
            nrm.extend(norms[n_i])
        else:
            nrm.extend([0, 0, 1])
        if t_i is not None and t_i < len(texs):
            uv.extend(texs[t_i])
        else:
            uv.extend([0, 0])

    indices = np.arange(len(pos) // 3, dtype=np.uint32)
    return (
        np.array(pos, dtype=np.float32),
        np.array(nrm, dtype=np.float32),
        np.array(uv, dtype=np.float32),
        indices,
    )