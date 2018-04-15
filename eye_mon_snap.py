from talon import ctrl, tap, ui, eye
from eye_mouse import tracker, mouse
from talon.track.geom import Point2d, Point3d, EyeFrame

main = ui.main_screen()

def is_on_main(p):
    return (main.x <= p.x < main.x + main.width and
            main.y <= p.y < main.y + main.height)

class MonSnap:
    def __init__(self):
        tap.register(tap.MMOVE, self.on_move)
        tracker.register('', self.on_stream)

        self.saved_mouse = None
        self.main_mouse = False
        self.main_gaze = False
        self.restore_counter = 0

    def on_stream(self, topic, b):
        if b['cmd'] != eye.SUB_GAZE:
            return
        l, r = EyeFrame(b, 'Left'), EyeFrame(b, 'Right')
        p = (l.gaze + r.gaze) / 2
        main_gaze = -0.02 < p.x < 1.02 and -0.02 < p.y < 1.02 and bool(l or r)
        if self.main_gaze and self.main_mouse and not main_gaze:
            self.restore_counter += 1
            if self.restore_counter > 5:
                self.restore()
        else:
            self.restore_counter = 0
            self.main_gaze = main_gaze

    def restore(self):
        if self.saved_mouse:
            mouse.last_ctrl = self.saved_mouse
            ctrl.mouse(self.saved_mouse.x, self.saved_mouse.y)
            self.saved_mouse = None
            self.main_gaze = False

    def on_move(self, typ, e):
        if typ != tap.MMOVE: return
        p = Point2d(e.x, e.y)
        on_main = is_on_main(p)
        if not on_main:
            self.saved_mouse = p
        self.main_mouse = on_main

snap = MonSnap()
