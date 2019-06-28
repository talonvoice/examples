from talon_plugins import eye_mouse, eye_zoom_mouse
from talon.voice import Context

ctx = Context('eye_control')
ctx.keymap({
    'zoom mouse':      lambda m: eye_zoom_mouse.active.toggle(),
    'debug overlay':   lambda m: eye_mouse.debug_overlay.toggle(),
    'control mouse':   lambda m: eye_mouse.control_mouse.toggle(),
    'camera overlay':  lambda m: eye_mouse.camera_overlay.toggle(),
    'run calibration': lambda m: eye_mouse.calib_start(),
})
