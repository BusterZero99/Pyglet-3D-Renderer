from src.imports import *
import sys


def get_requested_model(models_dir=None):
    if models_dir is None:
        models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    models_dir = os.path.abspath(models_dir)

    args = sys.argv
    for i, a in enumerate(args):
        if a in ("--model", "-m") and i + 1 < len(args):
            path = args[i + 1]
            break
    else:
        path = os.environ.get("PYTHON_3D_RENDERER_MODEL", "").strip()

    if not path:
        return None
    if not os.path.isabs(path):
        path = os.path.join(models_dir, path)
    return path if os.path.isfile(path) else None


def load_geometry():
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    models_dir = os.path.abspath(models_dir)
    obj_path = get_requested_model(models_dir)

    if obj_path:
        try:
            print("Loading requested model:", obj_path)
            return load_obj(obj_path)
        except Exception as e:
            print("Failed requested load:", e)

    try:
        for f in sorted(os.listdir(models_dir)):
            if f.lower().endswith(".obj"):
                path = os.path.join(models_dir, f)
                print("Loading default model:", path)
                return load_obj(path)
    except Exception as e:
        print("Model directory error:", e)

    print("Using built-in cube")
    return cube_vertices, cube_normals, cube_texcoords, cube_indices