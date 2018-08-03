from talon.voice import Word, Context, Key, Rep, Str, press
from talon import ui
import time

apps = {}

def switch_app(m):
    name = str(m._words[1])
    full = apps.get(name)
    if not full: return
    for app in ui.apps():
        if app.name == full:
            app.focus()
            # TODO: replace sleep with a check to see when it is in foreground
            time.sleep(0.25)
            break

ctx = Context('switcher')
keymap = {
    'focus {switcher.apps}': switch_app,
}
ctx.keymap(keymap)

def update_lists():
    global apps
    new = {}
    for app in ui.apps():
        if app.background and not app.windows():
            continue
        words = app.name.split(' ')
        for word in words:
            if word and not word in new:
                new[word] = app.name
        new[app.name] = app.name
    if set(new.keys()) == set(apps.keys()):
        return
    ctx.set_list('apps', new.keys())
    apps = new

def ui_event(event, arg):
    update_lists()

ui.register('', ui_event)
update_lists()
