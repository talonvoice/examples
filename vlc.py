from talon.api import ffi
from talon.voice import Context
from talon import applescript, ui

BUNDLE = 'org.videolan.vlc'

def app():
    for app in ui.apps():
        if app.bundle == BUNDLE:
            return app

class VLC:
    commands = {
        'full screen': 'fullscreen',
        'last': 'last',
        'mute': 'mute',
        'next': 'next',
        'play': 'play',
        'pause': 'play',
        'stop': 'stop',
        'quieter': 'volumeDown\n' * 2,
        'louder': 'volumeUp\n' * 2,
        'way quieter': 'volumeDown\n' * 6,
        'way louder': 'volumeUp\n' * 6,
        'focus': lambda: app().focus(),
    }

    def cmd(self, cmd):
        ret = applescript.run(f'tell application "VLC"\n{cmd}\nend tell')
        if ret:
            return ffi.string(ret).decode('utf8')

    def __call__(self, m):
        cmd = str(m['vlc.commands'][0])
        action = self.commands[cmd]
        if isinstance(action, str):
            self.cmd(action)
        else:
            action()

vlc = VLC()
ctx = Context('vlc') #, bundle=BUNDLE)
ctx.keymap({
    'video {vlc.commands}': vlc,
})
ctx.set_list('commands', vlc.commands.keys())
