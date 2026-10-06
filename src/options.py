import pyglet

pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False
pyglet.options["search_local_libs"] = True
window_name = "Python Renderer"
win_width = 854
win_height = 480
shaderMode = 1
zoom = 1.5

# UI Constants
COLOR_WHITE = (255, 255, 255, 255)
COLOR_HIGHLIGHT = (255, 235, 140, 255)
COLOR_DIM = (180, 180, 180, 255)
COLOR_ERROR = (255, 120, 120, 255)
LABEL_HEIGHT = 20
FILE_ITEM_HEIGHT = 20
MARGIN = 10
TEXT_OFFSET_Y = 30
BROWSER_ITEM_HEIGHT = 20
