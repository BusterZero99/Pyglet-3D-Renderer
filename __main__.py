from src.imports import *

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
RENDERER = os.path.join(BASE_DIR, "renderer.py")

picker_window = None

def launch(path):
    env = os.environ.copy(); env["PYTHON_3D_RENDERER_MODEL"] = path
    subprocess.Popen([sys.executable, RENDERER], env=env, cwd=BASE_DIR)
    if picker_window is not None:
        picker_window.close()
    pyglet.app.exit()

def draw_label(text, x, y, color=options.COLOR_WHITE):
    label = pyglet.text.Label(text, x=x, y=y, color=color)
    label.draw()

def run_picker():
    global picker_window
    obj_files = sorted([f for f in os.listdir(MODELS_DIR) if f.lower().endswith(".obj")]) if os.path.exists(MODELS_DIR) else []
    sel = 0
    input_mode = False
    input_text = ""
    file_browser = False
    current_dir = BASE_DIR
    file_list = []
    file_sel = 0

    def update_file_list():
        nonlocal file_list
        try:
            file_list = sorted(os.listdir(current_dir))
        except (OSError, PermissionError):
            file_list = []

    window = pyglet.window.Window(options.win_width, options.win_height, caption="Python 3D Renderer")
    picker_window = window
    label = pyglet.text.Label("OBJ picker (↑↓ select, Enter load, O browse files)", x=options.MARGIN, y=options.win_height-options.TEXT_OFFSET_Y, color=options.COLOR_WHITE)
    info = pyglet.text.Label("ESC exit | Browser: Backspace up, / root", x=options.MARGIN, y=options.MARGIN, color=options.COLOR_DIM)
    input_label = pyglet.text.Label("", x=options.MARGIN, y=options.win_height-60, color=options.COLOR_WHITE)

    @window.event
    def on_draw():
        window.clear(); label.draw(); info.draw()
        if file_browser:
            draw_label(f"Current dir: {current_dir}", options.MARGIN, options.win_height-60)
            for i, f in enumerate(file_list):
                y = options.win_height - 90 - i * options.BROWSER_ITEM_HEIGHT
                if y < 20:
                    break
                is_dir = os.path.isdir(os.path.join(current_dir, f))
                prefix = "[DIR]" if is_dir else "     "
                color = options.COLOR_HIGHLIGHT if i == file_sel else options.COLOR_WHITE
                marker = ">" if i == file_sel else " "
                draw_label(f"{marker} {prefix} {f}", 20, y, color)
        elif input_mode:
            input_label.text = f"Enter OBJ path: {input_text}_"
            input_label.draw()
        elif not obj_files:
            draw_label("No OBJ in models/ (press O)", 20, 320, options.COLOR_ERROR)
            return
        else:
            for i, f in enumerate(obj_files):
                y = options.win_height - 60 - i * 24
                color = options.COLOR_HIGHLIGHT if i == sel else options.COLOR_WHITE
                marker = ">" if i == sel else " "
                draw_label(f"{marker} {f}", 20, y, color)

    @window.event
    def on_key_press(symbol, modifiers):
        nonlocal sel, input_mode, input_text, file_browser, current_dir, file_list, file_sel
        if file_browser:
            if symbol == key.UP and file_list: file_sel = (file_sel - 1) % len(file_list)
            elif symbol == key.DOWN and file_list: file_sel = (file_sel + 1) % len(file_list)
            elif symbol == key.ENTER and file_list:
                selected = file_list[file_sel]
                full_path = os.path.join(current_dir, selected)
                if os.path.isdir(full_path):
                    current_dir = full_path
                    update_file_list()
                    file_sel = 0
                elif selected.lower().endswith('.obj'):
                    launch(full_path)
            elif symbol == key.BACKSPACE:
                parent = os.path.dirname(current_dir)
                if parent != current_dir:
                    current_dir = parent
                    update_file_list()
                    file_sel = 0
            elif symbol == key.SLASH:
                current_dir = os.path.abspath(os.sep)
                update_file_list()
                file_sel = 0
            elif symbol == key.ESCAPE:
                file_browser = False
        elif input_mode:
            if symbol == key.ENTER:
                p = input_text.strip()
                if p and os.path.isfile(p) and p.lower().endswith(".obj"):
                    launch(p)
                input_mode = False
                input_text = ""
            elif symbol == key.BACKSPACE:
                input_text = input_text[:-1]
            elif symbol == key.ESCAPE:
                input_mode = False
                input_text = ""
            elif symbol < 256 and chr(symbol).isprintable():
                input_text += chr(symbol)
        else:
            if symbol == key.UP and obj_files: sel = (sel - 1) % len(obj_files)
            elif symbol == key.DOWN and obj_files: sel = (sel + 1) % len(obj_files)
            elif symbol == key.ENTER and obj_files: launch(os.path.join(MODELS_DIR, obj_files[sel]))
            elif symbol == key.O:
                file_browser = True
                update_file_list()
            elif symbol == key.ESCAPE:
                window.close()

    pyglet.app.run()

if __name__ == '__main__':
    run_picker()
