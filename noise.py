from talon import ctrl
from talon.audio import noise

def on_noise(noise):
    if noise == 'pop':
        ctrl.mouse_click(button=1, hold=16000)
    if noise == 'hiss_start':
        ctrl.mouse_click(button=0, down=True)
    elif noise == 'hiss_end':
        ctrl.mouse_click(button=0, up=True)

noise.register('noise', on_noise)
