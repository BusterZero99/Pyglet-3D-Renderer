from src.imports import *

# --- Load geometry from models/ or fallback to cube ---
def load_geometry():
    path = os.path.join(os.path.dirname(__file__), "models")
    try:
        files = os.listdir(path)
        obj_file = next((f for f in files if re.search(r"\.obj$", f, re.IGNORECASE)), None)
        if obj_file:
            full_path = os.path.join(path, obj_file)
            v, n, t, i = load_obj(full_path)
            print("Loaded OBJ:", full_path)
            return v, n, t, i
    except Exception as e:
        print("Failed to load OBJ:", e)
    print("Using default cube geometry.")
    return cube_vertices, cube_normals, cube_texcoords, cube_indices

# --- Geometry + center + scale ---
vertices, normals, texcoords, indices = load_geometry()
verts3d = vertices.reshape(-1, 3)
min_corner = verts3d.min(axis=0)
max_corner = verts3d.max(axis=0)
center = (min_corner + max_corner) / 2.0
size = max_corner - min_corner
max_dim = np.max(size)

target_ndc_size = 5.0
scale = target_ndc_size / max_dim

def scale_matrix(s):
    return np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


# --- Window + GL setup ---
win = pyglet.window.Window(options.win_width, options.win_height, options.window_name, resizable=True)
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glClearColor(0.1, 0.1, 0.1, 1.0)

prog_rainbow = ShaderProgram(Shader(VERT_SRC, "vertex"), Shader(FRAG_SRC_RAINBOW, "fragment"))
prog_fill = ShaderProgram(Shader(VERT_SRC, "vertex"), Shader(FRAG_SRC_FILL, "fragment"))

vao = gl.GLuint(0)
gl.glGenVertexArrays(1, vao)
vao_id = vao.value
gl.glBindVertexArray(vao_id)

def make_vbo(data, index, size):
    buf = gl.GLuint(0)
    gl.glGenBuffers(1, buf)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buf)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data.ctypes.data, gl.GL_STATIC_DRAW)
    gl.glVertexAttribPointer(index, size, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
    gl.glEnableVertexAttribArray(index)

make_vbo(vertices, 0, 3)
make_vbo(normals, 1, 3)
make_vbo(texcoords, 2, 2)

ebo = gl.GLuint(0)
gl.glGenBuffers(1, ebo)
gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices.ctypes.data, gl.GL_STATIC_DRAW)

# --- Rotation state ---
rot = 180.0

@win.event
def on_draw():
    global rot
    win.clear()
    
    # Projection and view
    proj = perspective(np.radians(30), win.width / win.height, 0.1, 100.0)
    view = np.eye(4, dtype=np.float32)
    view[2][3] = -1    # back away
    view[1][3] = -13.0  # lower the camera a bit
    view = rotation_x(np.radians(20)) @ view

    # Model transform: center + scale + rotation
    model = (
        translation_matrix(-center)
        @ scale_matrix(scale*options.zoom)
        @ rotation_x(np.radians(270))
        @ rotation_z(rot)
    )

    mvp = proj @ view @ model

    gl.glBindVertexArray(vao_id)
    
    if options.shaderMode == 1:
        # Rainbow
        prog_rainbow.use()
        prog_rainbow["mvp"] = mvp.T.astype(np.float32).flatten()
        prog_rainbow["time"] = np.float32(rot)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

    elif options.shaderMode == 2:
        # Fill (light gray)
        prog_fill.use()
        prog_fill["mvp"] = mvp.T.astype(np.float32).flatten()
        prog_fill["color"] = (0.5, 0.5, 0.5)  # grey
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)
        
    elif options.shaderMode == 3:
        # Fill (grey)
        prog_fill.use()
        prog_fill["mvp"] = mvp.T.astype(np.float32).flatten()
        prog_fill["color"] = (0.5, 0.5, 0.5)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

        # Wireframe overlay (blue)
        gl.glEnable(gl.GL_POLYGON_OFFSET_LINE)
        gl.glPolygonOffset(-1, -1)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        gl.glLineWidth(0.1)
        prog_fill.use()
        prog_fill["mvp"] = mvp.T.astype(np.float32).flatten()
        prog_fill["color"] = (0.1, 0.3, 1.0)  # blue
        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glDisable(gl.GL_POLYGON_OFFSET_LINE)

@win.event
def on_key_press(symbol, modifiers):
    global ctrl_held
    if symbol == key.T:
        options.shaderMode = options.shaderMode % 3 + 1
        print("Shader mode:", options.shaderMode)
    if symbol in (pyglet.window.key.LCTRL, pyglet.window.key.RCTRL):
        ctrl_held = True

@win.event
def on_key_release(symbol, modifiers):
    global ctrl_held
    if symbol in (pyglet.window.key.LCTRL, pyglet.window.key.RCTRL):
        ctrl_held = False

@win.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if ctrl_held:
        factor = 1.1 if scroll_y > 0 else 0.9
        options.zoom *= factor
        options.zoom = max(0.1, min(options.zoom, 10.0))
    else:
        factor = 0.9 if scroll_y > 0 else 1.1
        options.zoom *= factor
        options.zoom = max(0.1, min(options.zoom, 10.0))

def update(dt):
    global rot
    rot += dt

pyglet.clock.schedule(update)
pyglet.app.run()
